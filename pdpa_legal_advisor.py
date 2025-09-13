#!/usr/bin/env python3
"""
PDPA Legal Advisor - A ChatGPT wrapper for Singapore Personal Data Protection Act 2012
Provides legal advice using IRAC framework based on factual scenarios
"""

import pandas as pd
import openai
import json
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import os
from pathlib import Path

@dataclass
class LegalAdvice:
    """Structure for legal advice using IRAC framework"""
    issue: str
    rule: str
    analysis: str
    conclusion: str
    relevant_sections: List[Dict[str, str]]
    risk_level: str  # Low, Medium, High
    recommendations: List[str]

class PDPALegalAdvisor:
    """Main class for PDPA legal advice generation"""
    
    def __init__(self, csv_path: str, api_key: Optional[str] = None):
        """
        Initialize the PDPA Legal Advisor
        
        Args:
            csv_path: Path to the PDPA sections CSV file
            api_key: OpenAI API key (if None, will look for OPENAI_API_KEY env var)
        """
        self.csv_path = csv_path
        self.df = self._load_pdpa_data()
        self.client = self._setup_openai_client(api_key)
        
    def _load_pdpa_data(self) -> pd.DataFrame:
        """Load and preprocess PDPA sections data"""
        try:
            df = pd.read_csv(self.csv_path)
            # Clean and filter the data
            df = df.dropna(subset=['section_number'])
            df['section_number'] = df['section_number'].astype(str)
            # Remove empty or invalid sections
            df = df[df['section_number'].str.match(r'^\d+$')]
            return df
        except Exception as e:
            raise Exception(f"Error loading PDPA data: {e}")
    
    def _setup_openai_client(self, api_key: Optional[str] = None):
        """Setup OpenAI client"""
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        elif os.getenv("OPENAI_API_KEY"):
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        else:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        return self.client
    
    def search_relevant_sections(self, scenario: str, top_k: int = 10) -> List[Dict[str, str]]:
        """
        Search for relevant PDPA sections based on factual scenario
        
        Args:
            scenario: The factual scenario to analyze
            top_k: Number of most relevant sections to return
            
        Returns:
            List of relevant sections with metadata
        """
        # Use OpenAI to identify relevant sections
        search_prompt = f"""
        Given this factual scenario about data protection: "{scenario}"
        
        Analyze the scenario and identify which sections of the Singapore Personal Data Protection Act 2012 are most relevant.
        
        Consider these key areas:
        - Data collection and consent (Sections 11-20)
        - Purpose limitation (Sections 18-20)
        - Accuracy and correction (Sections 21-22)
        - Protection and retention (Sections 23-26)
        - Access and correction rights (Sections 21-22)
        - Data breach notification (Sections 26A-26D)
        - Do Not Call Registry (Sections 36-48)
        - Offences and penalties (Sections 48C-48F)
        
        Return a JSON list of section numbers that are most relevant, ordered by relevance.
        Format: ["section_number1", "section_number2", ...]
        """
        
        try:
            # Try models in order of preference
            models_to_try = ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"]
            response = None
            
            for model in models_to_try:
                try:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": search_prompt}],
                        temperature=0.1,
                        max_tokens=500
                    )
                    break
                except Exception as e:
                    if "model_not_found" in str(e) or "does not exist" in str(e):
                        print(f"Model {model} not available, trying next...")
                        continue
                    else:
                        raise e
            
            if response is None:
                raise Exception("No available models found")
            
            # Parse the response to get section numbers
            content = response.choices[0].message.content.strip()
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                section_numbers = json.loads(json_match.group())
            else:
                # Fallback: extract numbers from text
                section_numbers = re.findall(r'\b\d+\b', content)
            
            # Get the actual section data
            relevant_sections = []
            for section_num in section_numbers[:top_k]:
                section_data = self.df[self.df['section_number'] == section_num]
                if not section_data.empty:
                    section = section_data.iloc[0]
                    relevant_sections.append({
                        'section_number': section['section_number'],
                        'title': section['section_title'],
                        'text': section['text'][:1000] + "..." if len(str(section['text'])) > 1000 else section['text']
                    })
            
            return relevant_sections
            
        except Exception as e:
            print(f"Error in section search: {e}")
            # Fallback: return some common sections
            return self._get_fallback_sections()
    
    def _get_fallback_sections(self) -> List[Dict[str, str]]:
        """Fallback method to return common PDPA sections"""
        common_sections = ['11', '12', '13', '14', '15', '18', '19', '20', '21', '22']
        sections = []
        for section_num in common_sections:
            section_data = self.df[self.df['section_number'] == section_num]
            if not section_data.empty:
                section = section_data.iloc[0]
                sections.append({
                    'section_number': section['section_number'],
                    'title': section['section_title'],
                    'text': section['text'][:1000] + "..." if len(str(section['text'])) > 1000 else section['text']
                })
        return sections
    
    def is_legal_scenario(self, scenario: str) -> tuple[bool, str]:
        """
        Check if the scenario is related to legal/data protection issues
        
        Args:
            scenario: The scenario to check
            
        Returns:
            Tuple of (is_legal, reason)
        """
        # Convert to lowercase for checking
        scenario_lower = scenario.lower()
        
        # Legal/data protection keywords
        legal_keywords = [
            'data', 'personal', 'privacy', 'consent', 'collection', 'disclosure',
            'breach', 'access', 'correction', 'retention', 'protection', 'purpose',
            'organization', 'individual', 'customer', 'client', 'employee', 'user',
            'information', 'records', 'database', 'processing', 'storage', 'transfer',
            'compliance', 'policy', 'procedure', 'notification', 'request', 'rights',
            'unauthorized', 'security', 'confidential', 'sensitive', 'identifiable',
            'pdp', 'gdpr', 'regulation', 'law', 'legal', 'statute', 'act',
            'company', 'business', 'organization', 'entity', 'corporation'
        ]
        
        # Check if scenario contains legal keywords
        keyword_count = sum(1 for keyword in legal_keywords if keyword in scenario_lower)
        
        # Minimum threshold for legal relevance
        if keyword_count < 2:
            return False, "Scenario does not appear to contain legal or data protection related content. Please provide a scenario involving personal data, privacy, or legal compliance issues."
        
        # Check for obviously non-legal content
        non_legal_indicators = [
            'chocolate', 'labubu', 'matcha', 'food', 'recipe', 'cooking',
            'gaming', 'game', 'entertainment', 'music', 'movie', 'book',
            'weather', 'sports', 'travel', 'vacation', 'hobby', 'art',
            'random', 'joke', 'meme', 'funny', 'test', 'hello', 'hi'
        ]
        
        if any(indicator in scenario_lower for indicator in non_legal_indicators):
            if keyword_count < 3:  # Lower threshold if non-legal indicators present
                return False, "Scenario appears to be non-legal content. Please provide a factual scenario involving data protection, privacy, or legal compliance issues."
        
        return True, "Scenario appears to be legal-related."

    def generate_legal_advice(self, scenario: str) -> LegalAdvice:
        """
        Generate comprehensive legal advice using IRAC framework
        
        Args:
            scenario: The factual scenario to analyze
            
        Returns:
            LegalAdvice object with structured analysis
        """
        # First check if this is a legal scenario
        is_legal, reason = self.is_legal_scenario(scenario)
        if not is_legal:
            return LegalAdvice(
                issue="Input validation failed",
                rule="The PDPA Legal Advisor is designed for data protection and privacy law scenarios only",
                analysis=reason,
                conclusion="Please provide a scenario involving personal data, privacy, or legal compliance issues.",
                relevant_sections=[],
                risk_level="N/A",
                recommendations=["Provide a legal scenario involving data protection", "Include details about personal data handling", "Describe privacy or compliance concerns"]
            )
        
        # Get relevant sections
        relevant_sections = self.search_relevant_sections(scenario)
        
        # Prepare context for IRAC analysis
        sections_context = "\n\n".join([
            f"Section {s['section_number']}: {s['title']}\n{s['text']}"
            for s in relevant_sections
        ])
        
        irac_prompt = f"""
        You are a legal expert specializing in Singapore's Personal Data Protection Act 2012. 
        Analyze the following factual scenario and provide legal advice using the IRAC framework.
        
        FACTUAL SCENARIO:
        {scenario}
        
        RELEVANT PDPA SECTIONS:
        {sections_context}
        
        Please provide a comprehensive legal analysis using the IRAC framework:
        
        1. ISSUE: Identify the key legal issues and questions raised by this scenario
        2. RULE: State the relevant legal rules and principles from the PDPA sections
        3. ANALYSIS: Apply the legal rules to the specific facts of the scenario
        4. CONCLUSION: Provide your legal conclusion and recommendations
        
        Also assess:
        - Risk level (Low/Medium/High) and reasoning
        - Specific recommendations for compliance
        - Potential penalties or consequences
        
        Format your response as valid JSON with these exact fields (use null for missing values, not NaN or undefined):
        {{
            "issue": "string",
            "rule": "string", 
            "analysis": "string",
            "conclusion": "string",
            "risk_level": "Low/Medium/High",
            "recommendations": ["recommendation1", "recommendation2", ...]
        }}
        
        IMPORTANT: Ensure all values are valid JSON strings, numbers, or arrays. Do not use NaN, undefined, or other invalid JSON values.
        """
        
        try:
            # Try models in order of preference
            models_to_try = ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"]
            response = None
            
            for model in models_to_try:
                try:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": irac_prompt}],
                        temperature=0.1,
                        max_tokens=2000
                    )
                    break
                except Exception as e:
                    if "model_not_found" in str(e) or "does not exist" in str(e):
                        print(f"Model {model} not available, trying next...")
                        continue
                    else:
                        raise e
            
            if response is None:
                raise Exception("No available models found")
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response with better pattern matching
            json_patterns = [
                r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # More precise JSON object pattern
                r'\{.*\}',  # Fallback to original pattern
            ]
            
            advice_data = None
            for pattern in json_patterns:
                json_match = re.search(pattern, content, re.DOTALL)
                if json_match:
                    try:
                        # Clean the JSON string to handle all NaN variations
                        json_str = json_match.group()
                        
                        # Replace all possible NaN variations
                        json_str = re.sub(r'\bNaN\b', 'null', json_str)
                        json_str = re.sub(r'\bundefined\b', 'null', json_str)
                        json_str = re.sub(r'\bnull\b', 'null', json_str)
                        
                        # Remove any remaining problematic values
                        json_str = re.sub(r':\s*NaN\s*', ': null', json_str)
                        json_str = re.sub(r':\s*undefined\s*', ': null', json_str)
                        
                        # Try to parse the cleaned JSON
                        advice_data = json.loads(json_str)
                        break  # Success, exit the loop
                        
                    except json.JSONDecodeError as e:
                        print(f"JSON parsing error with pattern {pattern}: {e}")
                        print(f"Problematic JSON: {json_str[:200]}...")
                        continue  # Try next pattern
            
            # If no JSON could be parsed, use fallback
            if advice_data is None:
                print("Using fallback response parsing")
                advice_data = self._parse_fallback_response(content)
            
            # Clean and validate the advice data
            def clean_text(text):
                if text is None or text == 'NaN' or text == 'undefined' or str(text).strip() == '':
                    return 'Information not available'
                # Clean the text thoroughly
                cleaned = str(text).replace('NaN', 'N/A').replace('undefined', 'N/A').strip()
                return cleaned if cleaned else 'Information not available'
            
            def clean_list(lst):
                if not isinstance(lst, list):
                    return []
                cleaned_items = []
                for item in lst:
                    if item is not None and item != 'NaN' and item != 'undefined' and str(item).strip() != '':
                        cleaned_items.append(clean_text(item))
                return cleaned_items if cleaned_items else ['Consult with legal counsel']
            
            def validate_advice_data(data):
                """Validate and clean the advice data structure"""
                if not isinstance(data, dict):
                    return self._parse_fallback_response("Invalid response format")
                
                # Ensure all required fields exist and are properly formatted
                validated = {}
                for key in ['issue', 'rule', 'analysis', 'conclusion', 'risk_level', 'recommendations']:
                    if key in data:
                        if key == 'recommendations':
                            validated[key] = clean_list(data[key])
                        else:
                            validated[key] = clean_text(data[key])
                    else:
                        # Provide default values for missing fields
                        if key == 'recommendations':
                            validated[key] = ['Consult with legal counsel']
                        else:
                            validated[key] = 'Information not available'
                
                return validated
            
            # Validate the advice data
            advice_data = validate_advice_data(advice_data)
            
            return LegalAdvice(
                issue=advice_data['issue'],
                rule=advice_data['rule'],
                analysis=advice_data['analysis'],
                conclusion=advice_data['conclusion'],
                relevant_sections=relevant_sections,
                risk_level=advice_data['risk_level'],
                recommendations=advice_data['recommendations']
            )
            
        except Exception as e:
            print(f"Error generating legal advice: {e}")
            return self._create_error_advice(relevant_sections, str(e))
    
    def _parse_fallback_response(self, content: str) -> Dict[str, Any]:
        """Fallback method to parse non-JSON responses"""
        # Clean the content to remove any problematic characters
        clean_content = content.replace('NaN', 'N/A').replace('undefined', 'N/A')
        
        # Try to extract meaningful information from the content
        issue = "Legal issues identified from scenario"
        rule = "Relevant PDPA provisions apply"
        analysis = clean_content[:500] + "..." if len(clean_content) > 500 else clean_content
        conclusion = "Further legal review recommended"
        risk_level = "Medium"
        recommendations = ['Consult with legal counsel', 'Review PDPA compliance']
        
        # Try to extract risk level from content
        if 'high' in clean_content.lower():
            risk_level = "High"
        elif 'low' in clean_content.lower():
            risk_level = "Low"
        
        return {
            'issue': issue,
            'rule': rule,
            'analysis': analysis,
            'conclusion': conclusion,
            'risk_level': risk_level,
            'recommendations': recommendations
        }
    
    def _create_error_advice(self, sections: List[Dict], error: str) -> LegalAdvice:
        """Create error advice when generation fails"""
        return LegalAdvice(
            issue="Error in analysis",
            rule="PDPA provisions may apply",
            analysis=f"Technical error occurred: {error}",
            conclusion="Manual legal review required",
            relevant_sections=sections,
            risk_level="Unknown",
            recommendations=["Consult legal expert", "Review relevant PDPA sections"]
        )
    
    def format_advice(self, advice: LegalAdvice) -> str:
        """Format legal advice for display"""
        output = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           PDPA LEGAL ADVICE REPORT                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔍 ISSUE:
{advice.issue}

📋 RULE:
{advice.rule}

🔬 ANALYSIS:
{advice.analysis}

✅ CONCLUSION:
{advice.conclusion}

⚠️  RISK LEVEL: {advice.risk_level.upper()}

📚 RELEVANT SECTIONS:
"""
        for section in advice.relevant_sections:
            output += f"\n• Section {section['section_number']}: {section['title']}"
        
        if advice.recommendations:
            output += f"\n\n💡 RECOMMENDATIONS:\n"
            for i, rec in enumerate(advice.recommendations, 1):
                output += f"{i}. {rec}\n"
        
        return output

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PDPA Legal Advisor - IRAC Framework Analysis")
    parser.add_argument("scenario", help="Factual scenario to analyze")
    parser.add_argument("--csv", default="pdpa_sections.csv", help="Path to PDPA sections CSV")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    
    args = parser.parse_args()
    
    try:
        # Initialize advisor
        advisor = PDPALegalAdvisor(args.csv, args.api_key)
        
        # Generate advice
        print("🔍 Analyzing scenario...")
        advice = advisor.generate_legal_advice(args.scenario)
        
        # Display results
        print(advisor.format_advice(advice))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
