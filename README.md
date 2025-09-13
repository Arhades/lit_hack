# PDPA Legal Advisor

A ChatGPT-powered legal advisor for Singapore's Personal Data Protection Act 2012 (PDPA) that provides structured legal advice using the IRAC (Issue, Rule, Analysis, Conclusion) framework.

## Features

- 🔍 **Intelligent Section Search**: Automatically identifies relevant PDPA sections based on factual scenarios
- 📋 **IRAC Framework**: Provides structured legal analysis using Issue, Rule, Analysis, Conclusion format
- ⚠️ **Risk Assessment**: Evaluates compliance risk levels (Low/Medium/High)
- 💡 **Actionable Recommendations**: Provides specific compliance recommendations
- 🚀 **Easy Integration**: Simple Python API and command-line interface

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd lit_hack-1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Command Line Interface

```bash
python pdpa_legal_advisor.py "Your factual scenario here"
```

Example:
```bash
python pdpa_legal_advisor.py "A company collected customer data without explicit consent and is now planning to sell it to third parties for marketing purposes."
```

### Python API

```python
from pdpa_legal_advisor import PDPALegalAdvisor

# Initialize the advisor
advisor = PDPALegalAdvisor("pdpa_sections.csv")

# Generate legal advice
scenario = "Your factual scenario here"
advice = advisor.generate_legal_advice(scenario)

# Display formatted advice
print(advisor.format_advice(advice))
```

### Example Usage

Run the example script to see the advisor in action:

```bash
python example_usage.py
```

## How It Works

1. **Section Search**: The system uses GPT-4 to analyze the factual scenario and identify relevant PDPA sections
2. **Context Building**: Relevant sections are retrieved from the CSV database
3. **IRAC Analysis**: GPT-4 generates structured legal advice using the IRAC framework
4. **Risk Assessment**: The system evaluates compliance risk and provides recommendations

## IRAC Framework

The legal advice follows the standard IRAC structure:

- **Issue**: Identifies the key legal questions raised by the scenario
- **Rule**: States the relevant legal rules and principles from PDPA sections
- **Analysis**: Applies the legal rules to the specific facts
- **Conclusion**: Provides legal conclusions and recommendations

## Example Output

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           PDPA LEGAL ADVICE REPORT                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔍 ISSUE:
Whether the company's collection and proposed sale of customer data without explicit consent violates PDPA requirements.

📋 RULE:
Sections 11-20 of PDPA require consent for collection, use, and disclosure of personal data.

🔬 ANALYSIS:
The company's actions likely violate multiple PDPA provisions...

✅ CONCLUSION:
The proposed data sale without consent is likely non-compliant and poses significant legal risks.

⚠️  RISK LEVEL: HIGH

📚 RELEVANT SECTIONS:
• Section 11: Consent required
• Section 12: Provision of consent
• Section 18: Notification of purpose

💡 RECOMMENDATIONS:
1. Obtain explicit consent before data collection
2. Implement proper consent management system
3. Review data processing agreements
```

## File Structure

```
lit_hack-1/
├── pdpa_legal_advisor.py    # Main application
├── example_usage.py         # Example usage script
├── requirements.txt         # Python dependencies
├── pdpa_sections.csv       # PDPA sections database
└── README.md               # This file
```

## Requirements

- Python 3.7+
- OpenAI API key
- pandas
- openai

## Legal Disclaimer

This tool is for educational and research purposes only. It does not constitute legal advice. Always consult with qualified legal professionals for actual legal matters.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.