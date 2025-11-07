#!/usr/bin/env python3
"""
Finance Mentor AI - Quick Start Script
This script helps users get started quickly with the application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("⚠️  Not running in virtual environment")
        print("   Recommendation: Create and activate a virtual environment")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # Windows")
        print("   source venv/bin/activate  # macOS/Linux")
        return False
    print("✅ Virtual environment detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install core dependencies
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_simple.txt'])
        print("✅ Core dependencies installed")
        
        # Ask about optional ML dependencies
        response = input("\n🤖 Install optional ML dependencies for enhanced features? (y/N): ")
        if response.lower() in ['y', 'yes']:
            if Path('requirements_ml.txt').exists():
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_ml.txt'])
                print("✅ ML dependencies installed")
                
                # Try to download spaCy model
                try:
                    subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
                    print("✅ spaCy model downloaded")
                except subprocess.CalledProcessError:
                    print("⚠️  Could not download spaCy model (optional)")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment file"""
    print("\n⚙️  Setting up environment...")
    
    if not Path('.env').exists():
        if Path('.env.example').exists():
            # Copy example file
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created from template")
        else:
            # Create basic .env file
            env_content = """SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///finance_mentor.db
PLAID_CLIENT_ID=demo-client-id
PLAID_SECRET=demo-secret-key
PLAID_ENV=sandbox
"""
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ Basic .env file created")
    else:
        print("✅ .env file already exists")

def test_application():
    """Test if application can start"""
    print("\n🧪 Testing application...")
    
    try:
        # Try to import the app
        import app
        print("✅ Application imports successfully")
        
        # Test database models
        from models.database import db, User
        print("✅ Database models work")
        
        # Test NLP components
        from nlp.intent_classifier import IntentClassifier
        classifier = IntentClassifier()
        intent, confidence = classifier.classify_intent("what is my balance")
        print(f"✅ NLP classifier works: '{intent}' ({confidence:.2f})")
        
        return True
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Finance Mentor AI - Quick Start")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check virtual environment (warning only)
    check_virtual_environment()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Test application
    if not test_application():
        print("\n❌ Setup incomplete. Please check the errors above.")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("🎉 Setup complete! You're ready to go!")
    print("\nTo start the application:")
    print("   python app.py")
    print("\nThen visit: http://localhost:5000")
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main()