#!/usr/bin/env python3
"""
Setup script for PDPA Legal Advisor
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_api_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY environment variable not set!")
        print("   Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    else:
        print("✅ OpenAI API key found!")
        return True

def check_csv_file():
    """Check if PDPA CSV file exists"""
    if os.path.exists("pdpa_sections.csv"):
        print("✅ PDPA sections CSV file found!")
        return True
    else:
        print("❌ pdpa_sections.csv file not found!")
        print("   Please ensure the CSV file is in the current directory.")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up PDPA Legal Advisor...\n")
    
    # Check CSV file
    if not check_csv_file():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check API key
    if not check_api_key():
        print("\n💡 After setting your API key, you can run:")
        print("   python pdpa_legal_advisor.py 'Your scenario here'")
        print("   python example_usage.py")
        print("   python web_interface.py")
        return False
    
    print("\n🎉 Setup complete! You can now use the PDPA Legal Advisor.")
    print("\n📖 Usage examples:")
    print("   Command line: python pdpa_legal_advisor.py 'Your scenario here'")
    print("   Examples:     python example_usage.py")
    print("   Web interface: python web_interface.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
