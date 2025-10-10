import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///finance_mentor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
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