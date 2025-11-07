import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration - use PostgreSQL for production, SQLite for development
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # For Vercel, use /tmp directory for SQLite (serverless limitation)
    if not database_url:
        database_url = 'sqlite:////tmp/finance_mentor.db'
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Plaid Configuration
    PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
    PLAID_SECRET = os.environ.get('PLAID_SECRET')
    PLAID_ENV = os.environ.get('PLAID_ENV', 'sandbox')  # sandbox, development, production
    
    # Security
    BCRYPT_LOG_ROUNDS = 12
    
    # ML Model Settings
    FORECAST_DAYS = 90
    MIN_TRANSACTIONS_FOR_FORECAST = 30
    
    # NLP Settings
    NLP_MODEL_PATH = 'models/nlp_model'
    INTENT_CONFIDENCE_THRESHOLD = 0.7