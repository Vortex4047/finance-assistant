# Installation Guide

## Quick Start (Recommended)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd finance-mentor-ai
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install core dependencies
pip install -r requirements_simple.txt

# Optional: Install ML dependencies for enhanced features
pip install -r requirements_ml.txt

# Download spaCy model (optional, for enhanced NLP)
python -m spacy download en_core_web_sm
```

### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (optional for demo)
```

### 5. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Features Available

### Core Features (No Setup Required)
- ✅ User registration and authentication
- ✅ Demo financial data
- ✅ AI chat assistant (rule-based)
- ✅ Basic spending analysis
- ✅ Simple cash flow forecasting
- ✅ Budget and goal tracking
- ✅ Investment portfolio tracking

### Enhanced Features (Requires ML Dependencies)
- 🔧 Advanced NLP with spaCy
- 🔧 Machine learning forecasting
- 🔧 Advanced analytics

### Banking Integration (Requires Plaid Setup)
- 🔧 Real bank account connection
- 🔧 Automatic transaction import
- 🔧 Real-time balance updates

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# If you get import errors, install missing packages:
pip install flask flask-sqlalchemy flask-login
```

**Database Issues**
```bash
# If database issues occur, delete and recreate:
rm finance_mentor.db
python app.py
```

**Port Already in Use**
```bash
# Change port in app.py or kill existing process:
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

## Optional Enhancements

### Set Up Plaid (Real Banking Data)
1. Sign up at https://plaid.com/
2. Get your API keys
3. Update `.env` file:
   ```
   PLAID_CLIENT_ID=your_client_id
   PLAID_SECRET=your_secret_key
   PLAID_ENV=sandbox
   ```

### Deploy to Production
See `DEPLOYMENT.md` for deployment instructions.
