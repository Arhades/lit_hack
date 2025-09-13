#!/usr/bin/env python3
"""
Test script for PDPA Legal Advisor
"""

import os
import sys
from pdpa_legal_advisor import PDPALegalAdvisor

def test_basic_functionality():
    """Test basic functionality without OpenAI API"""
    print("🧪 Testing PDPA Legal Advisor...")
    
    try:
        # Test CSV loading
        print("1. Testing CSV data loading...")
        advisor = PDPALegalAdvisor("pdpa_sections.csv", api_key="test-key")
        print(f"   ✅ Loaded {len(advisor.df)} sections from CSV")
        
        # Test section search (without API call)
        print("2. Testing section search...")
        sections = advisor._get_fallback_sections()
        print(f"   ✅ Retrieved {len(sections)} fallback sections")
        
        # Test data structure
        print("3. Testing data structure...")
        if not advisor.df.empty:
            print(f"   ✅ CSV has columns: {list(advisor.df.columns)}")
            print(f"   ✅ Sample section: {advisor.df.iloc[0]['section_number']}")
        else:
            print("   ❌ CSV is empty")
            return False
        
        print("\n✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_with_api():
    """Test with actual OpenAI API (if available)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set, skipping API test")
        return True
    
    print("\n🔗 Testing with OpenAI API...")
    try:
        advisor = PDPALegalAdvisor("pdpa_sections.csv")
        
        # Test with a simple scenario
        scenario = "A company wants to collect customer data for marketing purposes"
        print(f"   Testing scenario: {scenario}")
        
        advice = advisor.generate_legal_advice(scenario)
        
        print("   ✅ Generated legal advice successfully!")
        print(f"   Risk level: {advice.risk_level}")
        print(f"   Relevant sections: {len(advice.relevant_sections)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 PDPA Legal Advisor Test Suite\n")
    
    # Test basic functionality
    basic_test = test_basic_functionality()
    
    # Test with API if available
    api_test = test_with_api()
    
    if basic_test and api_test:
        print("\n🎉 All tests passed! The advisor is ready to use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
