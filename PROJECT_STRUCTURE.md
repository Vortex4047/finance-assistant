# 📁 Project Structure

```
finance-mentor-ai/
├── 📄 Core Application Files
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration settings
│   └── .env                      # Environment variables (create from .env.example)
│
├── 📦 Application Modules
│   ├── api/                      # External API integrations
│   │   ├── __init__.py
│   │   ├── plaid_client.py       # Plaid banking API client
│   │   └── ...
│   ├── models/                   # Data models and ML components
│   │   ├── __init__.py
│   │   ├── database.py           # SQLAlchemy database models
│   │   └── forecasting.py        # Cash flow forecasting
│   ├── nlp/                      # Natural Language Processing
│   │   ├── __init__.py
│   │   └── intent_classifier.py  # AI chat intent classification
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── helpers.py            # Helper functions
│
├── 🎨 Frontend Assets
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Landing page
│   │   ├── dashboard.html       # Main dashboard
│   │   ├── analytics.html       # Analytics page
│   │   ├── budgets.html         # Budget management
│   │   ├── goals.html           # Financial goals
│   │   ├── investments.html     # Investment portfolio
│   │   ├── reports.html         # Financial reports
│   │   ├── settings.html        # User settings
│   │   └── auth/                # Authentication templates
│   │       ├── login.html
│   │       └── register.html
│   └── static/                  # Static assets
│       ├── css/
│       │   └── style.css        # Custom styles
│       └── js/
│           ├── app.js           # Main JavaScript
│           └── performance.js   # Performance optimizations
│
├── 📚 Documentation
│   ├── README.md                # Main project documentation
│   ├── INSTALLATION.md          # Setup instructions
│   ├── CONTRIBUTING.md          # Contribution guidelines
│   └── LICENSE                  # MIT License
│
├── ⚙️ Configuration & Setup
│   ├── .env.example             # Environment variables template
│   ├── .gitignore              # Git ignore rules
│   ├── requirements_simple.txt  # Core dependencies
│   └── requirements_ml.txt      # Optional ML dependencies
│
├── 🧪 Testing & Utilities
│   ├── test_app.py             # Application tests
│   ├── test_setup.py           # Setup verification
│   ├── quick_start.py          # Automated setup script
│   └── prepare_for_github.py   # GitHub preparation script
│
└── 🗂️ Generated/Runtime
    ├── venv/                   # Virtual environment (local)
    ├── .git/                   # Git repository data
    └── finance_mentor.db       # SQLite database (created at runtime)
```

## 📋 File Descriptions

### Core Application
- **app.py**: Main Flask application with all routes and business logic
- **config.py**: Configuration management for different environments

### Data Layer
- **models/database.py**: SQLAlchemy models for users, accounts, transactions, etc.
- **models/forecasting.py**: Machine learning models for cash flow prediction

### AI & NLP
- **nlp/intent_classifier.py**: Natural language processing for chat assistant

### External Integrations
- **api/plaid_client.py**: Banking API integration for real account data

### Frontend
- **templates/**: Jinja2 HTML templates with Bootstrap 5 styling
- **static/**: CSS, JavaScript, and other static assets

### Setup & Testing
- **quick_start.py**: One-command setup for new users
- **test_setup.py**: Comprehensive system verification
- **requirements_*.txt**: Dependency management

## 🚀 Getting Started

1. **Quick Setup**: `python quick_start.py`
2. **Manual Setup**: See `INSTALLATION.md`
3. **Run Application**: `python app.py`
4. **Visit**: `http://localhost:5000`

## 🔧 Development

- **Add Features**: Extend `app.py` or create new modules
- **Modify UI**: Edit templates and static files
- **Add Dependencies**: Update requirements files
- **Test Changes**: Run `python test_setup.py`