#!/usr/bin/env python3
"""
Setup script for Resume & Cover Letter Generator
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_env_file():
    """Set up environment file"""
    env_file = ".env"
    env_example = "env.example"
    
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists(env_example):
        print("📝 Creating .env file from template...")
        try:
            shutil.copy(env_example, env_file)
            print("✅ .env file created")
            print("⚠️  Please edit .env file and add your GEMINI_API_KEY")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env.example file not found")
        return False

def main():
    """Main setup function"""
    print("🚀 Resume & Cover Letter Generator Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_env_file():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your GEMINI_API_KEY")
    print("2. Run: streamlit run app.py")
    print("3. Or use: start_app.bat (Windows)")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main() 