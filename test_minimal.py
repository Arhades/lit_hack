#!/usr/bin/env python3
"""
Minimal test to check if the API works with quota limitations
"""

import os
import openai

def test_minimal_api():
    """Test with the most minimal API call possible"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ API key not set")
        return False
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Try the most minimal request possible
        print("🔍 Testing minimal API call...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5,
            temperature=0
        )
        
        result = response.choices[0].message.content
        print(f"✅ Success! Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Minimal API Test\n")
    test_minimal_api()
