#!/usr/bin/env python3
"""
Demo script that shows the PDPA Legal Advisor functionality without requiring an API key
"""

from pdpa_legal_advisor import PDPALegalAdvisor
import json

def demo_basic_functionality():
    """Demonstrate basic functionality without API calls"""
    print("🚀 PDPA Legal Advisor Demo (No API Required)\n")
    
    try:
        # Initialize advisor (this will work without API key for basic functionality)
        print("1. Loading PDPA sections...")
        advisor = PDPALegalAdvisor("pdpa_sections.csv", api_key="demo-key")
        print(f"   ✅ Loaded {len(advisor.df)} sections from CSV")
        
        # Show some sample sections
        print("\n2. Sample PDPA sections:")
        sample_sections = advisor.df.head(5)
        for _, section in sample_sections.iterrows():
            print(f"   • Section {section['section_number']}: {section['section_title']}")
        
        # Test fallback section search
        print("\n3. Testing section search (fallback mode)...")
        scenario = "A company collected customer data without explicit consent"
        sections = advisor._get_fallback_sections()
        print(f"   ✅ Retrieved {len(sections)} relevant sections")
        
        # Show the sections that would be used
        print("\n4. Relevant sections for the scenario:")
        for section in sections[:3]:  # Show first 3
            print(f"   • Section {section['section_number']}: {section['title']}")
        
        # Create a mock legal advice
        print("\n5. Mock legal advice structure:")
        mock_advice = {
            "issue": "Whether the company's collection of customer data without explicit consent violates PDPA requirements",
            "rule": "Sections 11-15 of PDPA require consent for collection, use, and disclosure of personal data",
            "analysis": "The company's actions likely violate multiple PDPA provisions including consent requirements and purpose limitation",
            "conclusion": "The data collection without consent is likely non-compliant and poses significant legal risks",
            "risk_level": "High",
            "recommendations": [
                "Obtain explicit consent before data collection",
                "Implement proper consent management system",
                "Review data processing agreements"
            ]
        }
        
        print(f"   Issue: {mock_advice['issue']}")
        print(f"   Risk Level: {mock_advice['risk_level']}")
        print(f"   Recommendations: {len(mock_advice['recommendations'])} items")
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 To use the full AI-powered analysis:")
        print("   1. Get your OpenAI API key from https://platform.openai.com/api-keys")
        print("   2. Set it: export OPENAI_API_KEY='your-key-here'")
        print("   3. Run: python3 test_api_key.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

if __name__ == "__main__":
    demo_basic_functionality()
