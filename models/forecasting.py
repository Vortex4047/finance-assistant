from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from models.database import Transaction, Account

class CashFlowForecaster:
    def __init__(self):
        self.model = None
        self.is_trained = False
    
    def prepare_data(self, user_id, days_back=365):
        """Prepare transaction data for forecasting"""
        # Get user's transactions
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).order_by(Transaction.date).all()
        
        if len(transactions) < 30:  # Need minimum data for forecasting
            return None
        
        # Simple data preparation without pandas
        data = {}
        for trans in transactions:
            date_str = trans.date.strftime('%Y-%m-%d')
            if date_str not in data:
                data[date_str] = 0
            data[date_str] += trans.amount
        
        # Calculate current balance
        accounts = Account.query.filter_by(user_id=user_id).all()
        current_balance = sum(account.balance for account in accounts)
        
        return {
            'daily_flow': data,
            'current_balance': current_balance,
            'transactions': transactions
        }
    
    def train_model(self, user_id):
        """Train forecasting model on user's transaction history"""
        data = self.prepare_data(user_id)
        
        if data is None or len(data.get('daily_flow', {})) < 30:
            return False
        
        # Simple model - just store the data for prediction
        self.model = data
        self.is_trained = True
        return True
    
    def predict_cash_flow(self, user_id, days_ahead=30):
        """Predict cash flow for specified days ahead"""
        data = self.prepare_data(user_id)
        if data is None:
            return None
        
        # Simple average-based prediction
        daily_amounts = list(data['daily_flow'].values())
        avg_daily_change = sum(daily_amounts) / len(daily_amounts) if daily_amounts else 0
        
        current_balance = data['current_balance']
        predicted_balance = current_balance + (avg_daily_change * days_ahead)
        
        # Simple confidence intervals
        margin = abs(predicted_balance) * 0.15
        lower_bound = predicted_balance - margin
        upper_bound = predicted_balance + margin
        confidence = 0.6
        
        # Analyze spending trends
        recent_trend = self._analyze_spending_trend(user_id)
        
        return {
            'current_balance': current_balance,
            'predicted_balance': predicted_balance,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'days_ahead': days_ahead,
            'confidence': confidence,
            'trend': recent_trend
        }
    
    def _analyze_spending_trend(self, user_id, days_back=30):
        """Analyze recent spending trends"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.amount < 0  # Only expenses
        ).all()
        
        if not transactions or len(transactions) < 10:
            return 'stable'
        
        # Simple trend analysis - split transactions into two halves and compare
        mid_point = len(transactions) // 2
        first_half = transactions[:mid_point]
        second_half = transactions[mid_point:]
        
        first_half_avg = sum(abs(t.amount) for t in first_half) / len(first_half)
        second_half_avg = sum(abs(t.amount) for t in second_half) / len(second_half)
        
        change_percent = ((second_half_avg - first_half_avg) / first_half_avg) * 100 if first_half_avg > 0 else 0
        
        if change_percent > 20:  # Spending increased by more than 20%
            return 'increasing'
        elif change_percent < -20:  # Spending decreased by more than 20%
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_confidence(self, forecast=None):
        """Calculate confidence score"""
        return 0.6  # Fixed confidence for simple model
    
    def get_spending_insights(self, user_id):
        """Generate insights about spending patterns"""
        # Get last 90 days of transactions
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.amount < 0  # Only expenses
        ).all()
        
        if not transactions:
            return {}
        
        # Simple analysis without pandas
        category_spending = {}
        total_expenses = 0
        
        for t in transactions:
            category = t.category
            amount = abs(t.amount)
            total_expenses += amount
            
            if category not in category_spending:
                category_spending[category] = {'sum': 0, 'count': 0}
            
            category_spending[category]['sum'] += amount
            category_spending[category]['count'] += 1
        
        # Calculate averages and sort
        for category in category_spending:
            category_spending[category]['mean'] = category_spending[category]['sum'] / category_spending[category]['count']
        
        # Get top 5 categories by spending
        top_categories = dict(sorted(category_spending.items(), key=lambda x: x[1]['sum'], reverse=True)[:5])
        
        avg_daily_spending = total_expenses / 90 if total_expenses > 0 else 0
        
        return {
            'top_categories': top_categories,
            'avg_daily_spending': round(avg_daily_spending, 2),
            'total_expenses_90d': round(total_expenses, 2),
            'transaction_count': len(transactions)
        }