from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import json

from config import Config
from models.database import db, User, Account, Transaction
from nlp.intent_classifier import IntentClassifier
from models.forecasting import CashFlowForecaster
from api.plaid_client import PlaidClient
from utils.helpers import format_currency, categorize_transaction

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize components
intent_classifier = IntentClassifier()
forecaster = CashFlowForecaster()
plaid_client = PlaidClient()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            email=email,
            name=name,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'redirect': url_for('dashboard')})
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's accounts and recent transactions
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    
    # Auto-create demo data for new users (first time visiting dashboard)
    if not accounts:
        try:
            create_demo_accounts_and_transactions(current_user.id)
            accounts = Account.query.filter_by(user_id=current_user.id).all()
        except Exception as e:
            print(f"Error creating demo data: {e}")
    
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).limit(10).all()
    
    # Calculate total balance
    total_balance = sum(account.balance for account in accounts)
    
    # Get spending by category for current month
    current_month = datetime.now().replace(day=1)
    monthly_spending = db.session.query(
        Transaction.category, 
        db.func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= current_month,
        Transaction.amount < 0  # Only expenses
    ).group_by(Transaction.category).all()
    
    return render_template('dashboard.html', 
                         accounts=accounts,
                         recent_transactions=recent_transactions,
                         total_balance=total_balance,
                         monthly_spending=monthly_spending)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    user_message = request.json.get('message', '')
    
    # Debug logging
    print(f"User message: {user_message}")
    
    # Process message through NLP
    try:
        intent, confidence = intent_classifier.classify_intent(user_message)
        print(f"Intent: {intent}, Confidence: {confidence}")
    except Exception as e:
        print(f"Intent classification error: {e}")
        intent, confidence = 'general_help', 0.5
    
    # Lower confidence threshold for better responses
    if confidence < 0.3:
        response = "I'm not sure I understand. Could you rephrase your question about your finances?"
    else:
        response = process_financial_query(intent, user_message)
    
    return jsonify({
        'response': response,
        'intent': intent,
        'confidence': confidence
    })

def process_financial_query(intent, message):
    """Process different types of financial queries"""
    print(f"Processing intent: {intent} for message: {message}")
    
    if intent == 'greeting':
        return f"Hello {current_user.name}! 👋 I'm your Finance Mentor AI. I can help you with your balance, spending analysis, financial forecasts, savings advice, and more. What would you like to know about your finances today?"
    
    elif intent == 'general_help':
        return """I can help you with several financial tasks:
        
💰 **Balance Inquiries** - Check your current account balances
📊 **Spending Analysis** - Review your monthly expenses and spending patterns  
🔮 **Financial Forecasting** - Predict your future cash flow
💡 **Savings Advice** - Get personalized tips to save money
✅ **Affordability Checks** - See if you can afford a purchase
📈 **Investment Guidance** - Basic investment and financial planning advice

Just ask me questions like "What's my balance?" or "How much did I spend this month?" and I'll help you out!"""
    
    elif intent == 'balance_inquiry':
        accounts = Account.query.filter_by(user_id=current_user.id).all()
        if not accounts:
            return "You don't have any connected accounts yet. I've created some demo accounts for you to explore the features! Refresh the page to see your demo financial data."
        
        total_balance = sum(account.balance for account in accounts)
        account_details = []
        for account in accounts:
            account_details.append(f"• {account.name}: {format_currency(account.balance)}")
        
        response = f"💰 **Your Account Balances:**\n\n"
        response += "\n".join(account_details)
        response += f"\n\n**Total Balance: {format_currency(total_balance)}**"
        
        # Add some context if these are demo accounts
        if any('demo' in account.name.lower() for account in accounts):
            response += "\n\n*Note: This is demo data. Connect real accounts for actual financial tracking.*"
        
        return response
    
    elif intent == 'spending_analysis':
        # Analyze spending patterns
        current_month = datetime.now().replace(day=1)
        monthly_expenses = Transaction.query.filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= current_month,
            Transaction.amount < 0
        ).all()
        
        if not monthly_expenses:
            return "I don't see any spending data for this month yet. Connect your bank accounts to start tracking your expenses!"
        
        total_spent = sum(abs(t.amount) for t in monthly_expenses)
        
        # Get top spending categories
        from collections import defaultdict
        category_spending = defaultdict(float)
        for expense in monthly_expenses:
            category_spending[expense.category] += abs(expense.amount)
        
        top_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:3]
        
        response = f"📊 **This Month's Spending Analysis:**\n\n"
        response += f"**Total Spent: {format_currency(total_spent)}**\n\n"
        response += "**Top Categories:**\n"
        for category, amount in top_categories:
            response += f"• {category}: {format_currency(amount)}\n"
        
        return response
    
    elif intent == 'forecast_inquiry':
        # Generate cash flow forecast
        forecast = forecaster.predict_cash_flow(current_user.id)
        if forecast:
            confidence_emoji = "🟢" if forecast.get('confidence', 0) > 0.8 else "🟡" if forecast.get('confidence', 0) > 0.6 else "🔴"
            return f"🔮 **30-Day Financial Forecast:**\n\n{confidence_emoji} Based on your spending patterns, I predict you'll have **{format_currency(forecast['predicted_balance'])}** in 30 days.\n\nConfidence Level: {int(forecast.get('confidence', 0) * 100)}%"
        else:
            return "🔮 I need more transaction history to make accurate predictions. Connect your accounts and let me analyze your spending patterns for a few weeks to provide better forecasts!"
    
    elif intent == 'savings_advice':
        return generate_savings_advice()
    
    elif intent == 'affordability_check':
        # Extract amount from message if possible
        try:
            from utils.helpers import parse_amount_from_text
            amount = parse_amount_from_text(message)
        except:
            amount = None
        
        if amount:
            accounts = Account.query.filter_by(user_id=current_user.id).all()
            total_balance = sum(account.balance for account in accounts)
            
            if total_balance >= amount:
                remaining = total_balance - amount
                return f"✅ **Affordability Check:**\n\nYes, you can afford {format_currency(amount)}!\n\nAfter this purchase, you'd have {format_currency(remaining)} remaining.\n\n💡 Just make sure this fits within your monthly budget!"
            else:
                shortfall = amount - total_balance
                return f"❌ **Affordability Check:**\n\nYou currently don't have enough for {format_currency(amount)}.\n\nYou're short by {format_currency(shortfall)}.\n\n💡 Consider saving up or looking for a less expensive alternative!"
        else:
            return "💰 To check affordability, please specify an amount. For example: 'Can I afford $200?' or 'Should I buy something that costs $50?'"
    
    elif intent == 'investment_advice':
        return """📈 **Investment & Financial Planning Guidance:**

While I can't provide specific investment advice, here are some general principles:

🎯 **Start with the basics:**
• Build an emergency fund (3-6 months expenses)
• Pay off high-interest debt first
• Consider low-cost index funds for beginners

📚 **Learn before you invest:**
• Understand your risk tolerance
• Diversify your portfolio
• Think long-term

⚠️ **Important:** Always consult with a qualified financial advisor for personalized investment advice. I can help you track your spending and savings to free up money for investing!"""
    
    else:
        return "🤔 I'm not sure I understand that question. I can help you with:\n\n• Balance inquiries\n• Spending analysis\n• Financial forecasts\n• Savings advice\n• Affordability checks\n• General financial guidance\n\nTry asking something like 'What's my balance?' or 'How can I save money?'"

def generate_savings_advice():
    """Generate personalized savings advice"""
    # Analyze user's spending patterns
    current_month = datetime.now().replace(day=1)
    category_spending = db.session.query(
        Transaction.category,
        db.func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= current_month,
        Transaction.amount < 0
    ).group_by(Transaction.category).order_by(db.func.sum(Transaction.amount)).all()
    
    if not category_spending:
        return """💡 **Savings Tips to Get Started:**

Since you haven't connected your accounts yet, here are some universal money-saving strategies:

🏠 **Housing & Utilities:**
• Review your subscriptions and cancel unused ones
• Use energy-efficient appliances
• Consider refinancing if you have a mortgage

🍽️ **Food & Dining:**
• Meal plan and cook at home more often
• Buy generic brands
• Use coupons and cashback apps

🚗 **Transportation:**
• Walk, bike, or use public transport when possible
• Combine errands into one trip
• Keep up with car maintenance

Connect your accounts for personalized advice based on your actual spending patterns!"""
    
    highest_category = category_spending[0]
    amount = abs(highest_category.total)
    
    # Generate category-specific advice
    advice_map = {
        'Food and Drink': [
            "Try meal planning and cooking at home more often",
            "Consider bringing lunch to work instead of buying",
            "Look for grocery store sales and use coupons",
            "Limit dining out to special occasions"
        ],
        'Transportation': [
            "Consider carpooling or using public transportation",
            "Walk or bike for short distances",
            "Keep up with car maintenance to improve fuel efficiency",
            "Compare gas prices and use apps to find cheaper stations"
        ],
        'Entertainment': [
            "Look for free community events and activities",
            "Use streaming services instead of cable",
            "Take advantage of happy hours and matinee prices",
            "Host game nights instead of going out"
        ],
        'Shopping': [
            "Wait 24 hours before making non-essential purchases",
            "Compare prices online before buying",
            "Use cashback apps and browser extensions",
            "Buy generic brands when possible"
        ],
        'Bills': [
            "Review and negotiate your monthly bills",
            "Switch to energy-efficient appliances",
            "Bundle services for discounts",
            "Set up automatic payments to avoid late fees"
        ]
    }
    
    category_advice = advice_map.get(highest_category.category, [
        "Set a monthly budget limit for this category",
        "Track your spending to identify patterns",
        "Look for alternatives or substitutes",
        "Consider if each purchase is a need or want"
    ])
    
    response = f"💡 **Personalized Savings Advice:**\n\n"
    response += f"Your highest spending category this month is **{highest_category.category}** at {format_currency(amount)}.\n\n"
    response += f"**Here are some tips to reduce {highest_category.category} expenses:**\n"
    
    for i, tip in enumerate(category_advice, 1):
        response += f"{i}. {tip}\n"
    
    # Calculate potential savings
    potential_savings = amount * 0.2  # Assume 20% reduction is achievable
    response += f"\n💰 **Potential Monthly Savings:** {format_currency(potential_savings)}"
    response += f"\n📅 **Annual Impact:** {format_currency(potential_savings * 12)}"
    
    return response

@app.route('/api/forecast')
@login_required
def api_forecast():
    """API endpoint for cash flow forecast"""
    try:
        forecast = forecaster.predict_cash_flow(current_user.id)
        if forecast:
            return jsonify(forecast)
        else:
            return jsonify({'error': 'Insufficient data for forecast'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/insights')
@login_required
def api_insights():
    """API endpoint for spending insights"""
    try:
        insights = forecaster.get_spending_insights(current_user.id)
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_chat')
@login_required
def test_chat():
    """Test the chatbot functionality"""
    test_messages = [
        "hi",
        "what is my balance",
        "how much did I spend this month",
        "give me savings advice",
        "can I afford $100"
    ]
    
    results = []
    for message in test_messages:
        intent, confidence = intent_classifier.classify_intent(message)
        response = process_financial_query(intent, message)
        results.append({
            'message': message,
            'intent': intent,
            'confidence': confidence,
            'response': response
        })
    
    return jsonify(results)

@app.route('/create_demo_data', methods=['POST'])
@login_required
def create_demo_data():
    """Create demo financial data for testing"""
    try:
        # Create demo accounts
        demo_accounts = [
            {'name': 'Demo Checking Account', 'type': 'depository', 'balance': 2500.00},
            {'name': 'Demo Savings Account', 'type': 'depository', 'balance': 8750.00},
        ]
        
        for account_data in demo_accounts:
            # Check if account already exists
            existing = Account.query.filter_by(
                user_id=current_user.id,
                name=account_data['name']
            ).first()
            
            if not existing:
                account = Account(
                    user_id=current_user.id,
                    plaid_account_id=f"demo_{account_data['name'].lower().replace(' ', '_')}",
                    access_token='demo_token',
                    name=account_data['name'],
                    account_type=account_data['type'],
                    balance=account_data['balance']
                )
                db.session.add(account)
        
        db.session.commit()
        
        # Create demo transactions
        create_demo_transactions(current_user.id)
        
        return jsonify({'success': True, 'message': 'Demo data created successfully!'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/connect_account', methods=['POST'])
@login_required
def connect_account():
    """Handle Plaid Link token exchange"""
    public_token = request.json.get('public_token')
    
    try:
        # Exchange public token for access token
        access_token = plaid_client.exchange_public_token(public_token)
        
        # Get account information
        accounts_data = plaid_client.get_accounts(access_token)
        
        # Store accounts in database
        for account_data in accounts_data:
            account = Account(
                user_id=current_user.id,
                plaid_account_id=account_data['account_id'],
                access_token=access_token,
                name=account_data['name'],
                account_type=account_data['type'],
                balance=account_data['balances']['current']
            )
            db.session.add(account)
        
        db.session.commit()
        
        # Fetch initial transactions
        fetch_transactions_for_user(current_user.id)
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def fetch_transactions_for_user(user_id):
    """Fetch and store transactions for a user"""
    accounts = Account.query.filter_by(user_id=user_id).all()
    
    for account in accounts:
        try:
            transactions_data = plaid_client.get_transactions(
                account.access_token,
                start_date=datetime.now() - timedelta(days=365)
            )
            
            for trans_data in transactions_data:
                # Check if transaction already exists
                existing = Transaction.query.filter_by(
                    plaid_transaction_id=trans_data['transaction_id']
                ).first()
                
                if not existing:
                    transaction = Transaction(
                        user_id=user_id,
                        account_id=account.id,
                        plaid_transaction_id=trans_data['transaction_id'],
                        amount=trans_data['amount'],
                        date=datetime.strptime(trans_data['date'], '%Y-%m-%d').date(),
                        description=trans_data['name'],
                        category=categorize_transaction(trans_data)
                    )
                    db.session.add(transaction)
            
            db.session.commit()
            
        except Exception as e:
            print(f"Error fetching transactions for account {account.id}: {e}")

def create_demo_accounts_and_transactions(user_id):
    """Create demo accounts and transactions for new users"""
    # Create demo accounts
    demo_accounts = [
        {'name': 'Demo Checking Account', 'type': 'depository', 'balance': 2500.00},
        {'name': 'Demo Savings Account', 'type': 'depository', 'balance': 8750.00},
    ]
    
    for account_data in demo_accounts:
        account = Account(
            user_id=user_id,
            plaid_account_id=f"demo_{account_data['name'].lower().replace(' ', '_')}",
            access_token='demo_token',
            name=account_data['name'],
            account_type=account_data['type'],
            balance=account_data['balance']
        )
        db.session.add(account)
    
    db.session.commit()
    
    # Create demo transactions
    create_demo_transactions(user_id)

def create_demo_transactions(user_id):
    """Create demo transactions for testing"""
    import random
    from datetime import date, timedelta
    
    # Get user's accounts
    accounts = Account.query.filter_by(user_id=user_id).all()
    if not accounts:
        return
    
    checking_account = accounts[0]  # Use first account for transactions
    
    # Demo transaction templates
    demo_transactions = [
        {'description': 'Starbucks Coffee', 'category': 'Food and Drink', 'amount_range': (-5, -15)},
        {'description': 'Grocery Store', 'category': 'Food and Drink', 'amount_range': (-50, -120)},
        {'description': 'Gas Station', 'category': 'Transportation', 'amount_range': (-30, -60)},
        {'description': 'Netflix Subscription', 'category': 'Entertainment', 'amount_range': (-15, -20)},
        {'description': 'Amazon Purchase', 'category': 'Shopping', 'amount_range': (-25, -100)},
        {'description': 'Electric Bill', 'category': 'Bills', 'amount_range': (-80, -150)},
        {'description': 'Salary Deposit', 'category': 'Income', 'amount_range': (2000, 3000)},
        {'description': 'Restaurant Dinner', 'category': 'Food and Drink', 'amount_range': (-40, -80)},
        {'description': 'Uber Ride', 'category': 'Transportation', 'amount_range': (-15, -35)},
        {'description': 'Gym Membership', 'category': 'Health', 'amount_range': (-30, -50)},
    ]
    
    # Create transactions for the last 60 days
    start_date = date.today() - timedelta(days=60)
    
    for i in range(45):  # Create 45 transactions
        transaction_template = random.choice(demo_transactions)
        transaction_date = start_date + timedelta(days=random.randint(0, 60))
        amount = random.uniform(*transaction_template['amount_range'])
        
        # Check if transaction already exists (avoid duplicates)
        existing = Transaction.query.filter_by(
            user_id=user_id,
            description=transaction_template['description'],
            date=transaction_date
        ).first()
        
        if not existing:
            transaction = Transaction(
                user_id=user_id,
                account_id=checking_account.id,
                plaid_transaction_id=f"demo_trans_{i}_{user_id}",
                amount=amount,
                date=transaction_date,
                description=transaction_template['description'],
                category=transaction_template['category']
            )
            db.session.add(transaction)
    
    db.session.commit()

# Additional routes for new pages
@app.route('/analytics')
@login_required
def analytics():
    """Advanced analytics and insights page"""
    # Get comprehensive financial data
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).limit(100).all()
    
    # Calculate analytics
    analytics_data = calculate_analytics(current_user.id)
    
    return render_template('analytics.html', 
                         accounts=accounts,
                         transactions=transactions,
                         analytics=analytics_data)

@app.route('/budgets')
@login_required
def budgets():
    """Budget management page"""
    from models.database import Budget
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    
    # Calculate budget vs actual spending
    budget_analysis = analyze_budgets(current_user.id)
    
    return render_template('budgets.html', 
                         budgets=budgets,
                         analysis=budget_analysis)

@app.route('/goals')
@login_required
def goals():
    """Financial goals tracking page"""
    from models.database import Goal
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    
    return render_template('goals.html', goals=goals)

@app.route('/investments')
@login_required
def investments():
    """Investment portfolio page"""
    from models.database import Investment
    investments = Investment.query.filter_by(user_id=current_user.id).all()
    
    # Calculate portfolio performance
    portfolio_data = calculate_portfolio_performance(investments)
    
    return render_template('investments.html', 
                         investments=investments,
                         portfolio=portfolio_data)

@app.route('/api/investment', methods=['POST'])
@login_required
def add_investment_api():
    """Add a new investment"""
    try:
        from models.database import Investment
        from datetime import datetime
        
        data = request.get_json()
        
        investment = Investment(
            user_id=current_user.id,
            symbol=data.get('symbol').upper(),
            name=data.get('name'),
            shares=float(data.get('shares')),
            purchase_price=float(data.get('purchase_price')),
            current_price=float(data.get('purchase_price')),  # Initially same as purchase price
            purchase_date=datetime.strptime(data.get('purchase_date'), '%Y-%m-%d').date()
        )
        
        db.session.add(investment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Investment added successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/refresh-prices')
@login_required
def refresh_investment_prices():
    """Refresh investment prices (demo functionality)"""
    try:
        from models.database import Investment
        import random
        
        investments = Investment.query.filter_by(user_id=current_user.id).all()
        
        for investment in investments:
            # Simulate price changes (in real app, you'd call a stock API)
            change_percent = random.uniform(-0.05, 0.05)  # ±5% change
            investment.current_price = investment.purchase_price * (1 + change_percent)
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Refreshed prices for {len(investments)} investments'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/reports')
@login_required
def reports():
    """Financial reports page"""
    from models.database import Report
    reports = Report.query.filter_by(user_id=current_user.id)\
        .order_by(Report.generated_at.desc()).all()
    
    return render_template('reports.html', reports=reports)

@app.route('/api/generate-report/<report_type>')
@login_required
def generate_report_api(report_type):
    """Generate a financial report"""
    try:
        # Generate report data
        report_data = generate_report_data(current_user.id, report_type)
        
        return jsonify({
            'success': True,
            'message': f'{report_type.title()} report generated successfully',
            'data': report_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-report/<report_type>')
@login_required
def download_report(report_type):
    """Download report as PDF"""
    try:
        from flask import make_response
        import json
        from datetime import datetime
        
        # Generate report data
        report_data = generate_report_data(current_user.id, report_type)
        
        # Create a simple text-based report (in a real app, you'd use a PDF library)
        report_content = f"""
FINANCE MENTOR AI - {report_type.upper()} REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User: {current_user.name}

FINANCIAL SUMMARY:
- Total Income: ${report_data.get('total_income', 0):,.2f}
- Total Expenses: ${report_data.get('total_expenses', 0):,.2f}
- Net Savings: ${report_data.get('net_savings', 0):,.2f}
- Savings Rate: {report_data.get('savings_rate', 0):.1f}%

TOP EXPENSE CATEGORIES:
"""
        
        for category, amount in report_data.get('top_categories', []):
            report_content += f"- {category}: ${amount:,.2f}\n"
        
        response = make_response(report_content)
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = f'attachment; filename="{report_type}_report_{datetime.now().strftime("%Y%m%d")}.txt"'
        
        return response
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def generate_report_data(user_id, report_type):
    """Generate report data based on type"""
    from datetime import datetime, timedelta
    
    # Calculate date range based on report type
    end_date = datetime.now()
    if report_type == 'monthly':
        start_date = end_date.replace(day=1)
    elif report_type == 'quarterly':
        start_date = end_date - timedelta(days=90)
    else:  # yearly
        start_date = end_date.replace(month=1, day=1)
    
    # Get transactions for the period
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date.date(),
        Transaction.date <= end_date.date()
    ).all()
    
    # Calculate metrics
    income_transactions = [t for t in transactions if t.amount > 0]
    expense_transactions = [t for t in transactions if t.amount < 0]
    
    total_income = sum(t.amount for t in income_transactions)
    total_expenses = sum(abs(t.amount) for t in expense_transactions)
    net_savings = total_income - total_expenses
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0
    
    # Top categories
    from collections import defaultdict
    category_spending = defaultdict(float)
    for t in expense_transactions:
        category_spending[t.category] += abs(t.amount)
    
    top_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_savings': net_savings,
        'savings_rate': savings_rate,
        'top_categories': top_categories,
        'transaction_count': len(transactions)
    }

@app.route('/settings')
@login_required
def settings():
    """User settings and preferences page"""
    from models.database import UserPreference, Notification
    preferences = UserPreference.query.filter_by(user_id=current_user.id).all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    
    return render_template('settings.html', 
                         preferences=preferences,
                         notifications=notifications)

# API routes for new features
@app.route('/api/budget', methods=['POST'])
@login_required
def create_budget():
    """Create a new budget"""
    from models.database import Budget
    data = request.get_json()
    
    budget = Budget(
        user_id=current_user.id,
        category=data.get('category'),
        monthly_limit=float(data.get('monthly_limit'))
    )
    db.session.add(budget)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Budget created successfully'})

@app.route('/api/goal', methods=['POST'])
@login_required
def create_goal():
    """Create a new financial goal"""
    from models.database import Goal
    data = request.get_json()
    
    goal = Goal(
        user_id=current_user.id,
        title=data.get('title'),
        description=data.get('description'),
        target_amount=float(data.get('target_amount')),
        target_date=datetime.strptime(data.get('target_date'), '%Y-%m-%d').date(),
        category=data.get('category', 'General')
    )
    db.session.add(goal)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Goal created successfully'})

@app.route('/api/analytics/spending-trends')
@login_required
def spending_trends():
    """Get spending trends data for charts"""
    trends = get_spending_trends(current_user.id)
    return jsonify(trends)

@app.route('/api/analytics/income-vs-expenses')
@login_required
def income_vs_expenses():
    """Get income vs expenses data"""
    data = get_income_vs_expenses(current_user.id)
    return jsonify(data)

# Helper functions
def calculate_analytics(user_id):
    """Calculate comprehensive analytics"""
    current_month = datetime.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    # Current month data
    current_expenses = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= current_month,
        Transaction.amount < 0
    ).all()
    
    # Last month data
    last_month_expenses = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= last_month,
        Transaction.date < current_month,
        Transaction.amount < 0
    ).all()
    
    current_total = sum(abs(t.amount) for t in current_expenses)
    last_month_total = sum(abs(t.amount) for t in last_month_expenses)
    
    change_percent = ((current_total - last_month_total) / last_month_total * 100) if last_month_total > 0 else 0
    
    return {
        'current_month_spending': current_total,
        'last_month_spending': last_month_total,
        'change_percent': round(change_percent, 1),
        'top_categories': get_top_spending_categories(user_id),
        'daily_average': current_total / datetime.now().day if datetime.now().day > 0 else 0
    }

def analyze_budgets(user_id):
    """Analyze budget vs actual spending"""
    from models.database import Budget
    budgets = Budget.query.filter_by(user_id=user_id).all()
    current_month = datetime.now().replace(day=1)
    
    analysis = []
    for budget in budgets:
        spent = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == budget.category,
            Transaction.date >= current_month,
            Transaction.amount < 0
        ).scalar() or 0
        
        spent = abs(spent)
        remaining = budget.monthly_limit - spent
        percent_used = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
        
        analysis.append({
            'budget': budget,
            'spent': spent,
            'remaining': remaining,
            'percent_used': round(percent_used, 1),
            'status': 'over' if spent > budget.monthly_limit else 'warning' if percent_used > 80 else 'good'
        })
    
    return analysis

def calculate_portfolio_performance(investments):
    """Calculate investment portfolio performance"""
    if not investments:
        return {'total_value': 0, 'total_gain_loss': 0, 'gain_loss_percent': 0}
    
    total_invested = sum(inv.shares * inv.purchase_price for inv in investments)
    total_current = sum(inv.shares * (inv.current_price or inv.purchase_price) for inv in investments)
    
    gain_loss = total_current - total_invested
    gain_loss_percent = (gain_loss / total_invested * 100) if total_invested > 0 else 0
    
    return {
        'total_value': total_current,
        'total_invested': total_invested,
        'total_gain_loss': gain_loss,
        'gain_loss_percent': round(gain_loss_percent, 2)
    }

def get_top_spending_categories(user_id, limit=5):
    """Get top spending categories"""
    current_month = datetime.now().replace(day=1)
    
    categories = db.session.query(
        Transaction.category,
        db.func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == user_id,
        Transaction.date >= current_month,
        Transaction.amount < 0
    ).group_by(Transaction.category).order_by(db.func.sum(Transaction.amount)).limit(limit).all()
    
    return [{'category': cat.category, 'amount': abs(cat.total)} for cat in categories]

def get_spending_trends(user_id, days=30):
    """Get spending trends for the last N days"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    daily_spending = db.session.query(
        Transaction.date,
        db.func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.amount < 0
    ).group_by(Transaction.date).all()
    
    return [{'date': str(day.date), 'amount': abs(day.total)} for day in daily_spending]

def get_income_vs_expenses(user_id, months=6):
    """Get income vs expenses for the last N months"""
    data = []
    for i in range(months):
        month_start = (datetime.now().replace(day=1) - timedelta(days=i*30)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        income = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.date >= month_start,
            Transaction.date <= month_end,
            Transaction.amount > 0
        ).scalar() or 0
        
        expenses = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.date >= month_start,
            Transaction.date <= month_end,
            Transaction.amount < 0
        ).scalar() or 0
        
        data.append({
            'month': month_start.strftime('%B %Y'),
            'income': income,
            'expenses': abs(expenses)
        })
    
    return list(reversed(data))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)