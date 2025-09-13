#!/usr/bin/env python3
"""
Check which OpenAI models you have access to
"""

import os
import openai

def check_available_models():
    """Check which OpenAI models are available"""
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("\n💡 To set your API key, run:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # List of models to test
        models_to_test = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-4o-mini"
        ]
        
        print("\n🔍 Checking available models...")
        available_models = []
        
        for model in models_to_test:
            try:
                print(f"   Testing {model}...", end=" ")
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10,
                    temperature=0
                )
                print("✅ Available")
                available_models.append(model)
            except Exception as e:
                if "model_not_found" in str(e) or "does not exist" in str(e):
                    print("❌ Not available")
                else:
                    print(f"❌ Error: {str(e)[:50]}...")
        
        print(f"\n📋 Summary:")
        print(f"   Available models: {len(available_models)}")
        for model in available_models:
            print(f"   ✅ {model}")
        
        if available_models:
            print(f"\n💡 Recommended model: {available_models[0]}")
            print("   The PDPA Legal Advisor will automatically use the first available model.")
        else:
            print("\n❌ No models available. Please check your OpenAI account access.")
        
        return len(available_models) > 0
        
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

if __name__ == "__main__":
    print("🚀 OpenAI Models Checker\n")
    success = check_available_models()
    
    if success:
        print("\n🎉 You have access to OpenAI models!")
    else:
        print("\n❌ Please check your OpenAI account and API key.")
