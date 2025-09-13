#!/usr/bin/env python3
"""
Simple script to test your OpenAI API key
"""

import os
import openai

def test_api_key():
    """Test if the OpenAI API key is working"""
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("\n💡 To set your API key, run:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\n   Or add it to your shell profile:")
        print("   echo 'export OPENAI_API_KEY=\"your-api-key-here\"' >> ~/.zshrc")
        print("   source ~/.zshrc")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Test the API with a simple request
        print("🔍 Testing API connection...")
        
        client = openai.OpenAI(api_key=api_key)
        
        # Try different models to see which ones are available
        models_to_try = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        response = None
        used_model = None
        
        for model in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say 'Hello, API test successful!'"}],
                    max_tokens=50,
                    temperature=0
                )
                used_model = model
                break
            except Exception as e:
                if "model_not_found" in str(e) or "does not exist" in str(e):
                    print(f"   Model {model} not available, trying next...")
                    continue
                else:
                    raise e
        
        if response is None:
            raise Exception("No available models found")
        
        result = response.choices[0].message.content
        print(f"✅ API test successful!")
        print(f"   Model used: {used_model}")
        print(f"   Response: {result}")
        
        # Test with the PDPA advisor
        print("\n🔍 Testing PDPA Legal Advisor...")
        from pdpa_legal_advisor import PDPALegalAdvisor
        
        advisor = PDPALegalAdvisor("pdpa_sections.csv")
        print("✅ PDPA Legal Advisor initialized successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("\n💡 Common issues:")
        print("   1. Invalid API key - check if you copied it correctly")
        print("   2. No credits - add funds to your OpenAI account")
        print("   3. Network issues - check your internet connection")
        return False

if __name__ == "__main__":
    print("🚀 OpenAI API Key Test\n")
    success = test_api_key()
    
    if success:
        print("\n🎉 Everything is working! You can now use the PDPA Legal Advisor.")
        print("\n📖 Next steps:")
        print("   python example_usage.py          # Run example scenarios")
        print("   python web_interface.py          # Start web interface")
        print("   python pdpa_legal_advisor.py 'Your scenario here'  # Command line")
    else:
        print("\n❌ Please fix the issues above and try again.")
