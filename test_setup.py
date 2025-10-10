#!/usr/bin/env python3
"""
Test script to verify Finance Mentor AI setup
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'pandas',
        'numpy',
        'sklearn',
        'transformers',
        'spacy',
        'prophet'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def test_file_structure():
    """Test if all required files and directories exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'models/__init__.py',
        'models/database.py',
        'models/forecasting.py',
        'nlp/__init__.py',
        'nlp/intent_classifier.py',
        'api/__init__.py',
        'api/plaid_client.py',
        'utils/__init__.py',
        'utils/helpers.py',
        'templates/base.html',
        'templates/index.html',
        'templates/dashboard.html',
        'templates/auth/login.html',
        'templates/auth/register.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_database_models():
    """Test if database models can be imported and initialized"""
    print("\n🗄️  Testing database models...")
    
    try:
        from models.database import db, User, Account, Transaction
        print("✅ Database models imported successfully")
        
        # Test model attributes
        user_attrs = ['id', 'email', 'name', 'password_hash']
        for attr in user_attrs:
            if hasattr(User, attr):
                print(f"✅ User.{attr}")
            else:
                print(f"❌ User.{attr}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Database models test failed: {e}")
        return False

def test_nlp_components():
    """Test if NLP components can be initialized"""
    print("\n🤖 Testing NLP components...")
    
    try:
        from nlp.intent_classifier import IntentClassifier
        classifier = IntentClassifier()
        print("✅ Intent classifier initialized")
        
        # Test classification
        test_message = "what is my balance"
        intent, confidence = classifier.classify_intent(test_message)
        print(f"✅ Test classification: '{test_message}' -> {intent} ({confidence:.2f})")
        
        return True
    except Exception as e:
        print(f"❌ NLP components test failed: {e}")
        return False

def test_forecasting():
    """Test if forecasting components can be initialized"""
    print("\n📈 Testing forecasting components...")
    
    try:
        from models.forecasting import CashFlowForecaster
        forecaster = CashFlowForecaster()
        print("✅ Cash flow forecaster initialized")
        return True
    except Exception as e:
        print(f"❌ Forecasting test failed: {e}")
        return False

def test_configuration():
    """Test if configuration can be loaded"""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config import Config
        config = Config()
        print("✅ Configuration loaded")
        
        # Check for required config attributes
        required_attrs = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI']
        for attr in required_attrs:
            if hasattr(config, attr):
                print(f"✅ Config.{attr}")
            else:
                print(f"❌ Config.{attr}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Finance Mentor AI - Setup Verification")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Database Models", test_database_models),
        ("NLP Components", test_nlp_components),
        ("Forecasting", test_forecasting),
        ("Configuration", test_configuration)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Update your .env file with actual API keys")
        print("2. Run: python app.py")
        print("3. Visit: http://localhost:5000")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)