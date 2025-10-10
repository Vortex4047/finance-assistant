#!/usr/bin/env python3
"""
Setup script for Finance Mentor AI
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def setup_environment():
    """Set up the development environment"""
    print("🚀 Setting up Finance Mentor AI development environment\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment if it doesn't exist
    if not Path("venv").exists():
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Download spaCy model
    if os.name == 'nt':
        spacy_cmd = "venv\\Scripts\\python -m spacy download en_core_web_sm"
    else:
        spacy_cmd = "venv/bin/python -m spacy download en_core_web_sm"
    
    run_command(spacy_cmd, "Downloading spaCy English model")
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        print("📝 Creating .env file from template...")
        with open(".env.example", "r") as template:
            content = template.read()
        
        with open(".env", "w") as env_file:
            env_file.write(content)
        
        print("✅ .env file created. Please update it with your actual values.")
    
    # Create necessary directories
    directories = ["models", "static/css", "static/js", "static/images", "templates/auth"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with actual API keys")
    print("2. For Plaid integration, sign up at https://plaid.com/")
    print("3. Run the application with: python app.py")
    print("4. Visit http://localhost:5000 in your browser")
    
    return True

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking system requirements...\n")
    
    # Check if pip is available
    try:
        subprocess.run(["pip", "--version"], check=True, capture_output=True)
        print("✅ pip is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pip is not available. Please install pip first.")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Finance Mentor AI - Setup Script")
    print("=" * 50)
    
    if not check_requirements():
        sys.exit(1)
    
    if not setup_environment():
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Setup completed! You're ready to start developing.")
    print("=" * 50)