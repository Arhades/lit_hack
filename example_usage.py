#!/usr/bin/env python3
"""
Example usage of the PDPA Legal Advisor
"""

from pdpa_legal_advisor import PDPALegalAdvisor
import os

def main():
    """Example usage of the PDPA Legal Advisor"""
    
    # Example scenarios for testing
    scenarios = [
        "A company collected customer data without explicit consent and is now planning to sell it to third parties for marketing purposes.",
        
        "An organization experienced a data breach where personal data of 1000 customers was accessed by unauthorized parties. The breach was discovered 3 days ago.",
        
        "A customer requests access to their personal data and wants to correct some information. The organization has 30 days to respond but is unsure about the process.",
        
        "A company wants to send marketing messages to customers who have not opted in to receive such communications.",
        
        "An organization is transferring personal data to a country that does not have adequate data protection laws."
    ]
    
    try:
        # Initialize the advisor
        print("🚀 Initializing PDPA Legal Advisor...")
        advisor = PDPALegalAdvisor("pdpa_sections.csv")
        
        print("✅ Advisor initialized successfully!\n")
        
        # Test each scenario
        for i, scenario in enumerate(scenarios, 1):
            print(f"📋 SCENARIO {i}:")
            print(f"   {scenario}")
            print("\n" + "="*80 + "\n")
            
            # Generate legal advice
            advice = advisor.generate_legal_advice(scenario)
            
            # Display formatted advice
            print(advisor.format_advice(advice))
            print("\n" + "="*80 + "\n")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set your OPENAI_API_KEY environment variable")
        print("   2. Installed required packages: pip install -r requirements.txt")
        print("   3. The pdpa_sections.csv file in the current directory")

if __name__ == "__main__":
    main()
