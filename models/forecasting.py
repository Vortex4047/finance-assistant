import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
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
        
        # Convert to DataFrame
        data = []
        for trans in transactions:
            data.append({
                'ds': trans.date,
                'y': trans.amount,
                'category': trans.category
            })
        
        df = pd.DataFrame(data)
        
        # Aggregate daily cash flow
        daily_flow = df.groupby('ds')['y'].sum().reset_index()
        
        # Calculate cumulative balance (assuming starting balance from accounts)
        accounts = Account.query.filter_by(user_id=user_id).all()
        current_balance = sum(account.balance for account in accounts)
        
        # Calculate historical balance by working backwards
        total_transactions = daily_flow['y'].sum()
        starting_balance = current_balance - total_transactions
        
        daily_flow['balance'] = starting_balance + daily_flow['y'].cumsum()
        
        return daily_flow
    
    def train_model(self, user_id):
        """Train Prophet model on user's transaction history"""
        data = self.prepare_data(user_id)
        
        if data is None or len(data) < 30:
            return False
        
        # Prepare data for Prophet (daily balance)
        prophet_data = data[['ds', 'balance']].copy()
        prophet_data.columns = ['ds', 'y']
        
        # Initialize and train Prophet model
        self.model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05
        )
        
        # Add custom seasonalities
        self.model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        
        self.model.fit(prophet_data)
        self.is_trained = True
        
        return True
    
    def predict_cash_flow(self, user_id, days_ahead=30):
        """Predict cash flow for specified days ahead"""
        if not self.is_trained:
            if not self.train_model(user_id):
                return None
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=days_ahead)
        forecast = self.model.predict(future)
        
        # Get current and predicted balance
        current_balance = forecast['yhat'].iloc[-days_ahead-1]
        predicted_balance = forecast['yhat'].iloc[-1]
        
        # Calculate confidence intervals
        lower_bound = forecast['yhat_lower'].iloc[-1]
        upper_bound = forecast['yhat_upper'].iloc[-1]
        
        # Analyze spending trends
        recent_trend = self._analyze_spending_trend(user_id)
        
        return {
            'current_balance': current_balance,
            'predicted_balance': predicted_balance,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'days_ahead': days_ahead,
            'confidence': self._calculate_confidence(forecast),
            'trend': recent_trend,
            'forecast_data': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(days_ahead).to_dict('records')
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
        
        if not transactions:
            return 'stable'
        
        # Group by week and calculate average spending
        df = pd.DataFrame([{
            'date': t.date,
            'amount': abs(t.amount)
        } for t in transactions])
        
        df['week'] = pd.to_datetime(df['date']).dt.isocalendar().week
        weekly_spending = df.groupby('week')['amount'].sum()
        
        if len(weekly_spending) < 2:
            return 'stable'
        
        # Calculate trend
        trend_slope = np.polyfit(range(len(weekly_spending)), weekly_spending.values, 1)[0]
        
        if trend_slope > 50:  # Spending increasing by more than $50/week
            return 'increasing'
        elif trend_slope < -50:  # Spending decreasing by more than $50/week
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_confidence(self, forecast):
        """Calculate confidence score based on prediction intervals"""
        recent_predictions = forecast.tail(30)
        avg_interval = (recent_predictions['yhat_upper'] - recent_predictions['yhat_lower']).mean()
        avg_prediction = recent_predictions['yhat'].mean()
        
        # Confidence inversely related to interval width
        confidence = max(0, min(1, 1 - (avg_interval / abs(avg_prediction))))
        return round(confidence, 2)
    
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
        
        # Analyze by category
        df = pd.DataFrame([{
            'category': t.category,
            'amount': abs(t.amount),
            'date': t.date
        } for t in transactions])
        
        category_spending = df.groupby('category')['amount'].agg(['sum', 'mean', 'count']).round(2)
        
        # Find highest spending categories
        top_categories = category_spending.sort_values('sum', ascending=False).head(5)
        
        # Analyze spending frequency
        daily_spending = df.groupby('date')['amount'].sum()
        avg_daily_spending = daily_spending.mean()
        
        return {
            'top_categories': top_categories.to_dict('index'),
            'avg_daily_spending': round(avg_daily_spending, 2),
            'total_expenses_90d': round(df['amount'].sum(), 2),
            'transaction_count': len(transactions)
        }