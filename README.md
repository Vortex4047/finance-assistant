# 🤖 Finance Mentor AI

> **Your Intelligent Personal Finance Companion**

A comprehensive, AI-powered financial management platform that provides personalized financial advice, predictive analytics, investment tracking, and intelligent conversational assistance. Built with modern web technologies and machine learning capabilities.

![Finance Mentor AI](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 **Key Features**

### 🧠 **AI-Powered Financial Assistant**
- **Natural Language Processing**: Ask questions in plain English like "How much did I spend on food this month?"
- **Intent Recognition**: Advanced NLP using spaCy and custom-trained models
- **Contextual Responses**: Personalized advice based on your financial data
- **Smart Recommendations**: AI-generated savings tips and budget optimization

### 📊 **Advanced Analytics & Forecasting**
- **Cash Flow Prediction**: 30-90 day balance forecasting using Facebook Prophet
- **Spending Pattern Analysis**: Identify trends and anomalies in your expenses
- **Category-based Insights**: Detailed breakdown of spending by category
- **Performance Metrics**: Track your financial health over time

### 💰 **Comprehensive Financial Management**
- **Multi-Account Support**: Connect and manage multiple bank accounts
- **Budget Tracking**: Set and monitor spending limits by category
- **Goal Management**: Track progress toward financial milestones
- **Investment Portfolio**: Monitor stocks, bonds, and other investments

### 🔒 **Enterprise-Grade Security**
- **Bank-Level Encryption**: Secure data storage and transmission
- **OAuth Integration**: Secure authentication with financial institutions
- **Session Management**: Advanced user session handling
- **Data Privacy**: GDPR-compliant data handling practices

### 📱 **Modern User Experience**
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Real-time Updates**: Live data synchronization
- **Interactive Charts**: Dynamic visualizations with Chart.js
- **Professional UI**: Clean, modern interface with smooth animations

## 🚀 **Quick Start Guide**

### **Prerequisites**
- Python 3.8 or higher
- pip package manager
- Modern web browser

### **1. Installation**

```bash
# Clone the repository
git clone <repository-url>
cd finance-mentor-ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements_simple.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### **2. Configuration**

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# Required variables:
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///finance_mentor.db
PLAID_CLIENT_ID=your-plaid-client-id  # Optional for demo
PLAID_SECRET=your-plaid-secret-key    # Optional for demo
PLAID_ENV=sandbox
```

### **3. Run the Application**

```bash
# Start the development server
python app.py

# Visit in your browser
http://localhost:5000
```

### **4. First-Time Setup**

1. **Register Account**: Create your user account
2. **Explore Demo Data**: The system automatically creates demo financial data
3. **Connect Real Accounts**: (Optional) Set up Plaid integration for real bank data
4. **Start Chatting**: Use the AI assistant to explore your finances

## 🏗️ **Architecture Overview**

### **Backend Components**

```
finance-mentor-ai/
├── app.py                    # Main Flask application & routes
├── config.py                 # Configuration management
├── requirements_simple.txt   # Optimized dependencies
├── setup.py                  # Automated setup script
├── test_setup.py            # System verification tests
├── models/
│   ├── database.py          # SQLAlchemy ORM models
│   └── forecasting.py       # ML forecasting algorithms
├── nlp/
│   └── intent_classifier.py # NLP intent recognition
├── api/
│   └── plaid_client.py      # Banking API integration
├── utils/
│   └── helpers.py           # Utility functions
├── templates/               # Jinja2 HTML templates
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Landing page
│   ├── dashboard.html      # Main dashboard
│   ├── analytics.html      # Advanced analytics
│   ├── budgets.html        # Budget management
│   ├── goals.html          # Financial goals tracking
│   ├── investments.html    # Investment portfolio
│   ├── reports.html        # Financial reports
│   ├── settings.html       # User preferences
│   └── auth/               # Authentication pages
└── static/
    ├── css/
    │   └── style.css       # Custom styling
    └── js/
        ├── app.js          # Main JavaScript functionality
        └── performance.js  # Performance optimizations
```

### **Database Schema**

#### **Core Tables**
- **Users**: User accounts and authentication
- **Accounts**: Connected bank accounts
- **Transactions**: Financial transaction records
- **Budgets**: Spending limit configurations
- **Goals**: Financial milestone tracking
- **Investments**: Investment portfolio data
- **Notifications**: User alerts and messages
- **Reports**: Generated financial reports

## 🎯 **Feature Deep Dive**

### **1. AI Chat Assistant**

**Supported Query Types:**
- **Balance Inquiries**: "What's my current balance?"
- **Spending Analysis**: "How much did I spend on food this month?"
- **Forecasting**: "Will I have enough money next month?"
- **Savings Advice**: "How can I save more money?"
- **Affordability Checks**: "Can I afford a $500 purchase?"
- **Investment Guidance**: "How should I manage my portfolio?"

**Technical Implementation:**
```python
# Intent Classification Pipeline
1. Text Preprocessing (spaCy)
2. Rule-based Classification
3. ML Model Fallback (Naive Bayes + TF-IDF)
4. Confidence Scoring
5. Response Generation
```

### **2. Predictive Analytics**

**Cash Flow Forecasting:**
- **Algorithm**: Facebook Prophet time-series forecasting
- **Features**: Historical transactions, seasonal patterns, income cycles
- **Accuracy**: Confidence intervals and trend analysis
- **Timeframes**: 30, 60, and 90-day predictions

**Spending Pattern Analysis:**
- **Categorization**: Automatic transaction categorization
- **Trend Detection**: Identify spending increases/decreases
- **Anomaly Detection**: Flag unusual spending patterns
- **Comparative Analysis**: Month-over-month comparisons

### **3. Investment Tracking**

**Portfolio Management:**
- **Real-time Pricing**: Stock price updates (demo mode)
- **Performance Metrics**: Gain/loss calculations
- **Asset Allocation**: Portfolio diversification analysis
- **Risk Assessment**: Basic portfolio risk evaluation

**Supported Assets:**
- Stocks (individual securities)
- ETFs and mutual funds
- Bonds and fixed income
- Cash and cash equivalents

### **4. Budget & Goal Management**

**Smart Budgeting:**
- **Category-based Budgets**: Set limits by spending category
- **Progress Tracking**: Real-time budget vs. actual spending
- **Alert System**: Notifications when approaching limits
- **Optimization Suggestions**: AI-powered budget recommendations

**Goal Tracking:**
- **SMART Goals**: Specific, Measurable, Achievable, Relevant, Time-bound
- **Progress Visualization**: Charts and progress bars
- **Milestone Celebrations**: Achievement notifications
- **Automatic Calculations**: Required monthly savings amounts

## 🔧 **Technical Specifications**

### **Backend Stack**
- **Framework**: Flask 3.1+ with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Flask-Login with bcrypt password hashing
- **API Integration**: Plaid API for banking data
- **Machine Learning**: scikit-learn, Facebook Prophet, spaCy

### **Frontend Stack**
- **UI Framework**: Bootstrap 5.1+ for responsive design
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome 6.0+
- **Animations**: CSS3 transitions and transforms
- **Performance**: Optimized with lazy loading and throttling

### **Security Features**
- **Password Security**: bcrypt hashing with salt
- **Session Management**: Secure session handling
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Data Encryption**: Sensitive data encryption at rest
- **API Security**: Token-based authentication for external APIs

## 📈 **Performance Optimizations**

### **Frontend Optimizations**
- **Lazy Loading**: Charts and images load only when visible
- **Code Splitting**: Modular JavaScript loading
- **CSS Optimization**: Reduced animations and GPU usage
- **Caching**: Browser caching for static assets
- **Compression**: Minified CSS and JavaScript

### **Backend Optimizations**
- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: In-memory caching for frequent queries
- **Async Processing**: Background tasks for heavy operations
- **Connection Pooling**: Efficient database connections

## 🔌 **API Integration**

### **Plaid Banking API**
```python
# Configuration
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret_key
PLAID_ENV=sandbox  # sandbox/development/production

# Supported Features
- Account linking and authentication
- Transaction history retrieval
- Real-time balance updates
- Account metadata and categorization
```

### **Custom API Endpoints**
```
GET  /api/forecast              # Cash flow predictions
GET  /api/insights              # Spending insights
POST /api/budget               # Create/update budgets
POST /api/goal                 # Create/update goals
POST /api/investment           # Add investments
GET  /api/generate-report/<type> # Generate financial reports
GET  /api/download-report/<type> # Download reports
```

## 🧪 **Testing & Development**

### **Run Tests**
```bash
# Verify system setup
python test_setup.py

# Test individual components
python -c "from nlp.intent_classifier import IntentClassifier; c = IntentClassifier(); print(c.classify_intent('what is my balance'))"

# Test chat functionality
curl -X POST http://localhost:5000/test_chat
```

### **Development Mode**
```bash
# Enable debug mode
export FLASK_ENV=development
python app.py

# Access debug information
# Debugger PIN will be displayed in console
```

### **Performance Monitoring**
- Browser DevTools for frontend performance
- Flask debug toolbar for backend profiling
- Chart.js performance metrics
- Memory usage monitoring

## 🚀 **Deployment Guide**

### **Production Setup**

1. **Environment Configuration**
```bash
# Production environment variables
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@localhost/finance_mentor
PLAID_ENV=production
PLAID_CLIENT_ID=your-production-client-id
PLAID_SECRET=your-production-secret
```

2. **Database Migration**
```bash
# Set up PostgreSQL database
createdb finance_mentor

# Run migrations (if using Flask-Migrate)
flask db upgrade
```

3. **Web Server Setup**
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements_simple.txt .
RUN pip install -r requirements_simple.txt
RUN python -m spacy download en_core_web_sm

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🎨 **Customization Guide**

### **Adding New Financial Categories**
```python
# In utils/helpers.py
def categorize_transaction(transaction_data):
    # Add your custom categorization logic
    name = transaction_data.get('name', '').lower()
    
    # Custom category example
    if 'gym' in name or 'fitness' in name:
        return 'Health & Fitness'
    
    # ... existing logic
```

### **Custom AI Intents**
```python
# In nlp/intent_classifier.py
self.intents = {
    'custom_intent': [
        'custom query example',
        'another example phrase'
    ],
    # ... existing intents
}
```

### **New Dashboard Widgets**
```html
<!-- In templates/dashboard.html -->
<div class="col-md-4">
    <div class="card financial-card h-100">
        <div class="card-body text-center">
            <div class="financial-icon icon-custom mx-auto">
                <i class="fas fa-custom-icon"></i>
            </div>
            <div class="metric-label">Custom Metric</div>
            <div class="metric-value">$0.00</div>
        </div>
    </div>
</div>
```

## 🔍 **Troubleshooting**

### **Common Issues**

**1. Charts Not Loading**
```bash
# Check browser console for errors
# Verify Chart.js is loaded
# Ensure canvas elements have proper IDs
```

**2. Plaid Integration Issues**
```bash
# Verify credentials in .env file
# Check Plaid environment setting
# Review API permissions in Plaid dashboard
```

**3. Performance Issues**
```bash
# Enable performance mode
document.body.classList.add('performance-mode');

# Check browser DevTools Performance tab
# Monitor memory usage
# Disable animations if needed
```

**4. Database Errors**
```bash
# Reset database
rm finance_mentor.db
python app.py  # Will recreate database

# Check SQLAlchemy logs
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Debug Mode**
```python
# Enable detailed logging
app.config['DEBUG'] = True
app.config['SQLALCHEMY_ECHO'] = True

# Access Flask debug toolbar
pip install flask-debugtoolbar
```

## 📊 **Analytics & Reporting**

### **Available Reports**
- **Monthly Reports**: Comprehensive monthly financial summary
- **Quarterly Reports**: Quarterly performance analysis
- **Annual Reports**: Yearly financial overview
- **Custom Reports**: Date-range specific analysis

### **Export Formats**
- **PDF Reports**: Professional formatted reports
- **CSV Data**: Raw transaction data export
- **JSON API**: Programmatic data access

### **Key Metrics Tracked**
- Income vs. Expenses
- Spending by Category
- Budget Performance
- Goal Progress
- Investment Returns
- Cash Flow Trends
- Financial Health Score

## 🛡️ **Security & Privacy**

### **Data Protection**
- **Encryption**: AES-256 encryption for sensitive data
- **Secure Storage**: Encrypted database fields
- **API Security**: OAuth 2.0 for external integrations
- **Session Security**: Secure session cookies

### **Privacy Compliance**
- **Data Minimization**: Only collect necessary data
- **User Control**: Full data export and deletion options
- **Transparency**: Clear privacy policy and data usage
- **Consent Management**: Granular permission controls

### **Best Practices**
- Regular security updates
- Dependency vulnerability scanning
- Secure coding practices
- Regular backups
- Access logging and monitoring

## 🤝 **Contributing**

### **Development Setup**
```bash
# Fork the repository
git clone <your-fork-url>
cd finance-mentor-ai

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python test_setup.py

# Submit pull request
```

### **Code Standards**
- **Python**: Follow PEP 8 style guidelines
- **JavaScript**: Use ES6+ features
- **HTML/CSS**: Semantic markup and responsive design
- **Documentation**: Comprehensive docstrings and comments

### **Testing Requirements**
- Unit tests for all new features
- Integration tests for API endpoints
- Performance tests for heavy operations
- Security tests for authentication flows

## 📚 **API Documentation**

### **Authentication Endpoints**
```
POST /register          # User registration
POST /login            # User authentication
GET  /logout           # User logout
```

### **Financial Data Endpoints**
```
GET  /dashboard        # Main dashboard data
POST /chat            # AI chat interface
GET  /api/forecast    # Cash flow predictions
GET  /api/insights    # Spending insights
```

### **Management Endpoints**
```
POST /api/budget      # Budget management
POST /api/goal        # Goal management
POST /api/investment  # Investment tracking
GET  /api/generate-report/<type>  # Report generation
GET  /api/download-report/<type>  # Report download
```

## 🎓 **Educational Resources**

### **Financial Concepts**
- **Budgeting**: 50/30/20 rule implementation
- **Emergency Funds**: 3-6 months expense calculation
- **Investment Basics**: Asset allocation principles
- **Cash Flow Management**: Income vs. expense optimization

### **Technical Learning**
- **Machine Learning**: Time-series forecasting with Prophet
- **NLP**: Intent classification and entity extraction
- **Web Development**: Modern Flask application architecture
- **Data Visualization**: Interactive charts with Chart.js

## 🔮 **Future Roadmap**

### **Planned Features**
- [ ] **Mobile App**: React Native mobile application
- [ ] **Advanced ML**: Deep learning for better predictions
- [ ] **Social Features**: Financial goal sharing and challenges
- [ ] **Tax Integration**: Tax preparation and optimization
- [ ] **Credit Monitoring**: Credit score tracking and improvement
- [ ] **Bill Management**: Automatic bill tracking and reminders

### **Technical Improvements**
- [ ] **Microservices**: Break into smaller services
- [ ] **Real-time Updates**: WebSocket integration
- [ ] **Advanced Security**: Multi-factor authentication
- [ ] **API Expansion**: RESTful API for third-party integrations
- [ ] **Performance**: Redis caching and optimization
- [ ] **Monitoring**: Application performance monitoring

## 📞 **Support & Community**

### **Getting Help**
- **Documentation**: Comprehensive guides and tutorials
- **Issue Tracker**: GitHub issues for bug reports
- **Community Forum**: User discussions and tips
- **Email Support**: Direct support for critical issues

### **Contributing**
- **Bug Reports**: Detailed issue descriptions
- **Feature Requests**: Enhancement suggestions
- **Code Contributions**: Pull requests welcome
- **Documentation**: Help improve guides and tutorials

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Plaid**: Banking API integration
- **Facebook Prophet**: Time-series forecasting
- **spaCy**: Natural language processing
- **Chart.js**: Data visualization
- **Bootstrap**: UI framework
- **Flask**: Web framework

---

**Built with ❤️ for better financial wellness**

*Finance Mentor AI - Your path to financial freedom starts here.*