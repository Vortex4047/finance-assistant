# Finance Mentor AI - Development Guide

## Overview

Finance Mentor AI is an intelligent personal finance coaching system that provides:
- Natural language processing for financial queries
- Predictive cash flow forecasting using machine learning
- Personalized financial advice and recommendations
- Secure bank account integration via Plaid API
- Web-based responsive interface

## Quick Start

### 1. Setup Environment

```bash
# Clone or download the project
# Navigate to project directory

# Run setup script
python setup.py

# Or manual setup:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Required environment variables:
- `SECRET_KEY`: Flask secret key for sessions
- `PLAID_CLIENT_ID`: Your Plaid client ID
- `PLAID_SECRET`: Your Plaid secret key
- `PLAID_ENV`: Environment (sandbox/development/production)

### 3. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### 4. Test Setup

```bash
python test_setup.py
```

## Architecture

### Backend Components

#### 1. Flask Application (`app.py`)
- Main web application with routes
- User authentication and session management
- API endpoints for chat and financial data
- Database operations

#### 2. Database Models (`models/database.py`)
- User management
- Account and transaction storage
- Budget and preference tracking
- SQLAlchemy ORM models

#### 3. Machine Learning (`models/forecasting.py`)
- Cash flow prediction using Facebook Prophet
- Spending pattern analysis
- Financial insights generation
- Time series forecasting

#### 4. Natural Language Processing (`nlp/intent_classifier.py`)
- Intent classification for user queries
- Entity extraction from financial questions
- Response generation
- Custom training data and models

#### 5. API Integration (`api/plaid_client.py`)
- Plaid API wrapper for bank connections
- Transaction fetching and normalization
- Account balance retrieval
- Secure token management

#### 6. Utilities (`utils/helpers.py`)
- Currency formatting
- Transaction categorization
- Date handling
- Financial calculations

### Frontend Components

#### 1. Templates
- `base.html`: Base template with navigation
- `index.html`: Landing page
- `dashboard.html`: Main user interface
- `auth/`: Login and registration pages

#### 2. Static Assets
- `static/css/style.css`: Custom styling
- `static/js/app.js`: JavaScript functionality
- Bootstrap 5 for responsive design
- Chart.js for data visualization

## Key Features Implementation

### 1. Natural Language Processing

The NLP system uses a combination of:
- Rule-based intent classification
- TF-IDF vectorization with Naive Bayes
- spaCy for text preprocessing
- Custom training data for financial intents

**Supported Intents:**
- Balance inquiries
- Spending analysis
- Cash flow forecasting
- Savings advice
- Affordability checks

### 2. Cash Flow Forecasting

Uses Facebook Prophet for time series forecasting:
- Analyzes historical transaction patterns
- Accounts for seasonality and trends
- Provides confidence intervals
- Generates 30-90 day predictions

**Features:**
- Daily balance predictions
- Spending velocity analysis
- Trend identification
- Confidence scoring

### 3. Personalized Recommendations

Machine learning-driven advice system:
- Category-based spending analysis
- Comparative benchmarking
- Contextual financial tips
- Budget optimization suggestions

### 4. Security Implementation

- Password hashing with bcrypt
- Session-based authentication
- CSRF protection with Flask-WTF
- Encrypted database storage
- Secure API token handling

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - Main dashboard view
- `POST /chat` - AI chat interface
- `POST /connect_account` - Plaid account connection

### API Routes
- `GET /api/forecast` - Cash flow predictions
- `GET /api/insights` - Spending insights

## Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique user email
- `name`: User's full name
- `password_hash`: Encrypted password
- `created_at`: Registration timestamp

### Accounts Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `plaid_account_id`: Plaid account identifier
- `access_token`: Encrypted Plaid access token
- `name`: Account name
- `account_type`: Account type (checking, savings, etc.)
- `balance`: Current balance

### Transactions Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `account_id`: Foreign key to accounts
- `plaid_transaction_id`: Plaid transaction identifier
- `amount`: Transaction amount (negative for expenses)
- `date`: Transaction date
- `description`: Transaction description
- `category`: Categorized transaction type

## Development Workflow

### 1. Adding New Features

1. Create feature branch
2. Implement backend logic
3. Add database migrations if needed
4. Create/update templates
5. Add JavaScript functionality
6. Write tests
7. Update documentation

### 2. Testing

```bash
# Run setup verification
python test_setup.py

# Test individual components
python -c "from nlp.intent_classifier import IntentClassifier; c = IntentClassifier(); print(c.classify_intent('what is my balance'))"

# Test database models
python -c "from models.database import User; print('Models imported successfully')"
```

### 3. Deployment Considerations

#### Production Setup
- Use PostgreSQL instead of SQLite
- Set up proper environment variables
- Configure HTTPS/SSL
- Set up monitoring and logging
- Use production WSGI server (Gunicorn)

#### Environment Variables for Production
```bash
DATABASE_URL=postgresql://user:pass@localhost/finance_mentor
PLAID_ENV=production
SECRET_KEY=your-production-secret-key
```

## Plaid Integration

### Setup Steps

1. Sign up at [Plaid Dashboard](https://dashboard.plaid.com/)
2. Get your Client ID and Secret Key
3. Choose environment (sandbox for development)
4. Add credentials to `.env` file

### Plaid Link Flow

1. Frontend requests link token
2. User completes Plaid Link flow
3. Frontend receives public token
4. Backend exchanges for access token
5. Fetch and store account/transaction data

### Sandbox Testing

Plaid sandbox provides test credentials:
- Username: `user_good`
- Password: `pass_good`

## Machine Learning Models

### Intent Classification

**Training Data Structure:**
```python
intents = {
    'balance_inquiry': [
        'what is my balance',
        'how much money do i have',
        'current balance'
    ],
    # ... more intents
}
```

**Model Pipeline:**
1. Text preprocessing with spaCy
2. TF-IDF vectorization
3. Multinomial Naive Bayes classification
4. Confidence scoring

### Cash Flow Forecasting

**Prophet Model Configuration:**
```python
model = Prophet(
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=True,
    changepoint_prior_scale=0.05
)
model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
```

**Features Used:**
- Historical daily balances
- Transaction patterns
- Seasonal trends
- Income/expense cycles

## Troubleshooting

### Common Issues

1. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Database Connection Error**
   - Check DATABASE_URL in .env
   - Ensure database exists
   - Run `flask db upgrade` if using migrations

3. **Plaid API Errors**
   - Verify credentials in .env
   - Check environment setting (sandbox/development/production)
   - Ensure proper API permissions

4. **Import Errors**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

### Debug Mode

Enable Flask debug mode for development:
```python
app.run(debug=True)
```

### Logging

Add logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Update documentation

## License

This project is for educational purposes. Please ensure compliance with financial data regulations in your jurisdiction.

## Support

For issues and questions:
1. Check this documentation
2. Run `python test_setup.py`
3. Review error logs
4. Check Plaid documentation for API issues