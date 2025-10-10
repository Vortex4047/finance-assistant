import re
from datetime import datetime, timedelta

def format_currency(amount):
    """Format amount as currency"""
    if amount is None:
        return "$0.00"
    return f"${amount:,.2f}"

def categorize_transaction(transaction_data):
    """Categorize transaction based on Plaid category or merchant"""
    # Use Plaid's category if available
    if transaction_data.get('category') and len(transaction_data['category']) > 0:
        return transaction_data['category'][0]
    
    # Fallback categorization based on merchant name or description
    name = transaction_data.get('name', '').lower()
    merchant = transaction_data.get('merchant_name', '').lower()
    
    # Food & Dining
    food_keywords = ['restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'food', 'dining', 'starbucks', 'mcdonalds']
    if any(keyword in name or keyword in merchant for keyword in food_keywords):
        return 'Food and Drink'
    
    # Gas & Transportation
    gas_keywords = ['gas', 'fuel', 'shell', 'exxon', 'chevron', 'bp', 'uber', 'lyft', 'taxi']
    if any(keyword in name or keyword in merchant for keyword in gas_keywords):
        return 'Transportation'
    
    # Shopping
    shopping_keywords = ['amazon', 'walmart', 'target', 'store', 'shop', 'retail', 'mall']
    if any(keyword in name or keyword in merchant for keyword in shopping_keywords):
        return 'Shops'
    
    # Bills & Utilities
    bills_keywords = ['electric', 'water', 'internet', 'phone', 'cable', 'utility', 'bill', 'payment']
    if any(keyword in name or keyword in merchant for keyword in bills_keywords):
        return 'Bills'
    
    # Entertainment
    entertainment_keywords = ['movie', 'theater', 'netflix', 'spotify', 'game', 'entertainment']
    if any(keyword in name or keyword in merchant for keyword in entertainment_keywords):
        return 'Entertainment'
    
    return 'Other'

def parse_amount_from_text(text):
    """Extract monetary amount from text"""
    # Look for patterns like $100, 100.50, $1,000.00
    pattern = r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    match = re.search(pattern, text)
    
    if match:
        amount_str = match.group(1).replace(',', '')
        return float(amount_str)
    
    return None

def get_date_range(period):
    """Get start and end dates for a given period"""
    end_date = datetime.now().date()
    
    if period == 'week':
        start_date = end_date - timedelta(days=7)
    elif period == 'month':
        start_date = end_date.replace(day=1)
    elif period == 'year':
        start_date = end_date.replace(month=1, day=1)
    elif period == 'quarter':
        current_quarter = (end_date.month - 1) // 3 + 1
        quarter_start_month = (current_quarter - 1) * 3 + 1
        start_date = end_date.replace(month=quarter_start_month, day=1)
    else:
        # Default to current month
        start_date = end_date.replace(day=1)
    
    return start_date, end_date

def calculate_spending_velocity(transactions):
    """Calculate how fast user is spending money"""
    if not transactions or len(transactions) < 2:
        return 0
    
    # Sort transactions by date
    sorted_transactions = sorted(transactions, key=lambda x: x.date)
    
    # Calculate daily spending rate
    total_days = (sorted_transactions[-1].date - sorted_transactions[0].date).days
    if total_days == 0:
        return 0
    
    total_spending = sum(abs(t.amount) for t in transactions if t.amount < 0)
    daily_rate = total_spending / total_days
    
    return daily_rate

def get_financial_advice(spending_category, amount, user_avg):
    """Generate contextual financial advice"""
    advice = []
    
    if amount > user_avg * 1.5:
        advice.append(f"Your {spending_category} spending is 50% higher than usual.")
        
        if spending_category.lower() in ['food and drink', 'dining']:
            advice.append("Consider meal planning and cooking at home more often.")
        elif spending_category.lower() in ['entertainment']:
            advice.append("Look for free or low-cost entertainment alternatives.")
        elif spending_category.lower() in ['shops', 'shopping']:
            advice.append("Try waiting 24 hours before making non-essential purchases.")
    
    elif amount < user_avg * 0.7:
        advice.append(f"Great job! Your {spending_category} spending is below average.")
    
    return advice

def validate_financial_goal(goal_amount, current_balance, monthly_income):
    """Validate if a financial goal is realistic"""
    if goal_amount <= 0:
        return False, "Goal amount must be positive"
    
    if goal_amount > monthly_income * 12:
        return False, "Goal seems unrealistic based on your income"
    
    if goal_amount > current_balance * 10:
        return False, "Goal might be too ambitious for your current financial situation"
    
    return True, "Goal looks achievable"

def format_time_ago(date):
    """Format date as time ago (e.g., '2 days ago')"""
    now = datetime.now().date()
    diff = now - date
    
    if diff.days == 0:
        return "Today"
    elif diff.days == 1:
        return "Yesterday"
    elif diff.days < 7:
        return f"{diff.days} days ago"
    elif diff.days < 30:
        weeks = diff.days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    else:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"