#!/usr/bin/env python3
"""
Finance Mentor AI - GitHub Preparation Script
This script prepares the project for GitHub upload by:
1. Checking all files are present
2. Validating code syntax
3. Creating necessary documentation
4. Setting up proper .gitignore
"""

import os
import sys
from pathlib import Path

def check_required_files():
    """Check if all required files are present"""
    print("🔍 Checking required files...")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements_simple.txt',
        'README.md',
        '.env.example',
        '.gitignore',
        'models/database.py',
        'models/forecasting.py',
        'nlp/intent_classifier.py',
        'api/plaid_client.py',
        'utils/helpers.py',
        'templates/base.html',
        'templates/dashboard.html',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files present")
    return True

def validate_python_syntax():
    """Validate Python file syntax"""
    print("\n🐍 Validating Python syntax...")
    
    python_files = [
        'app.py',
        'config.py',
        'models/database.py',
        'models/forecasting.py',
        'nlp/intent_classifier.py',
        'api/plaid_client.py',
        'utils/helpers.py'
    ]
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), file_path, 'exec')
            print(f"✅ {file_path}")
        except SyntaxError as e:
            print(f"❌ {file_path}: {e}")
            return False
        except Exception as e:
            print(f"⚠️  {file_path}: {e}")
    
    print("✅ All Python files have valid syntax")
    return True

def create_gitignore():
    """Create or update .gitignore file"""
    print("\n📝 Creating .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite
*.sqlite3
finance_mentor.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp

# ML Models (optional - uncomment if you want to exclude trained models)
# models/*.pkl
# models/*.joblib

# Deployment
.vercel/
node_modules/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Documentation
docs/_build/
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore created")

def create_installation_guide():
    """Create installation guide"""
    print("\n📖 Creating INSTALLATION.md...")
    
    installation_content = """# Installation Guide

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
venv\\Scripts\\activate
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
"""
    
    with open('INSTALLATION.md', 'w', encoding='utf-8') as f:
        f.write(installation_content)
    
    print("✅ INSTALLATION.md created")

def create_contributing_guide():
    """Create contributing guide"""
    print("\n🤝 Creating CONTRIBUTING.md...")
    
    contributing_content = """# Contributing to Finance Mentor AI

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/finance-mentor-ai.git
   cd finance-mentor-ai
   ```
3. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\\Scripts\\activate on Windows
   pip install -r requirements_simple.txt
   pip install -r requirements_ml.txt  # optional
   ```

## Code Standards

### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

### JavaScript
- Use ES6+ features
- Follow consistent naming conventions
- Comment complex logic
- Optimize for performance

### HTML/CSS
- Use semantic HTML
- Follow Bootstrap conventions
- Ensure responsive design
- Maintain accessibility standards

## Testing

Run tests before submitting:
```bash
python test_setup.py
python test_app.py
```

## Submitting Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test thoroughly

3. Commit with clear messages:
   ```bash
   git commit -m "Add: new feature description"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

## Areas for Contribution

### High Priority
- [ ] Enhanced ML models for forecasting
- [ ] Mobile app development
- [ ] Additional banking integrations
- [ ] Advanced security features

### Medium Priority
- [ ] More chart types and visualizations
- [ ] Export functionality improvements
- [ ] Performance optimizations
- [ ] Accessibility improvements

### Low Priority
- [ ] UI/UX enhancements
- [ ] Additional language support
- [ ] Social features
- [ ] Gamification elements

## Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Browser/OS information
- Error messages or screenshots

## Feature Requests

For feature requests, please:
- Check existing issues first
- Describe the use case
- Explain the expected benefit
- Consider implementation complexity

## Questions?

Feel free to open an issue for questions or join our discussions!
"""
    
    with open('CONTRIBUTING.md', 'w', encoding='utf-8') as f:
        f.write(contributing_content)
    
    print("✅ CONTRIBUTING.md created")

def create_license():
    """Create MIT license"""
    print("\n📄 Creating LICENSE...")
    
    license_content = """MIT License

Copyright (c) 2024 Finance Mentor AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open('LICENSE', 'w', encoding='utf-8') as f:
        f.write(license_content)
    
    print("✅ LICENSE created")

def main():
    """Main preparation function"""
    print("🚀 Preparing Finance Mentor AI for GitHub...")
    print("=" * 50)
    
    success = True
    
    # Check files
    if not check_required_files():
        success = False
    
    # Validate syntax
    if not validate_python_syntax():
        success = False
    
    # Create supporting files
    create_gitignore()
    create_installation_guide()
    create_contributing_guide()
    create_license()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Project is ready for GitHub!")
        print("\nNext steps:")
        print("1. Create a new repository on GitHub")
        print("2. git init")
        print("3. git add .")
        print("4. git commit -m 'Initial commit: Finance Mentor AI'")
        print("5. git remote add origin <your-repo-url>")
        print("6. git push -u origin main")
        print("\n📖 Don't forget to update the repository URL in README.md!")
    else:
        print("❌ Please fix the issues above before uploading to GitHub")
        sys.exit(1)

if __name__ == "__main__":
    main()