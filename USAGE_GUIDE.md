# PDPA Legal Advisor - Usage Guide

## Quick Start

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run setup script
python setup.py
```

### 2. Basic Usage

#### Command Line
```bash
python pdpa_legal_advisor.py "Your factual scenario here"
```

#### Python API
```python
from pdpa_legal_advisor import PDPALegalAdvisor

advisor = PDPALegalAdvisor("pdpa_sections.csv")
advice = advisor.generate_legal_advice("Your scenario here")
print(advisor.format_advice(advice))
```

#### Web Interface
```bash
python web_interface.py
# Open http://localhost:5000 in your browser
```

## Example Scenarios

### 1. Data Collection Without Consent
**Scenario**: "A company collected customer data without explicit consent and is now planning to sell it to third parties for marketing purposes."

**Expected Analysis**: High risk, violations of consent requirements (Sections 11-15), purpose limitation (Sections 18-20).

### 2. Data Breach Notification
**Scenario**: "An organization experienced a data breach where personal data of 1000 customers was accessed by unauthorized parties. The breach was discovered 3 days ago."

**Expected Analysis**: High risk, breach notification requirements (Sections 26A-26D), potential penalties.

### 3. Data Subject Access Request
**Scenario**: "A customer requests access to their personal data and wants to correct some information. The organization has 30 days to respond but is unsure about the process."

**Expected Analysis**: Medium risk, access and correction rights (Sections 21-22), response timeframes.

### 4. Marketing Communications
**Scenario**: "A company wants to send marketing messages to customers who have not opted in to receive such communications."

**Expected Analysis**: High risk, Do Not Call Registry requirements (Sections 36-48), consent for marketing.

### 5. International Data Transfer
**Scenario**: "An organization is transferring personal data to a country that does not have adequate data protection laws."

**Expected Analysis**: High risk, cross-border transfer restrictions, adequacy requirements.

## Understanding the IRAC Framework

### Issue
- Identifies the specific legal questions raised by the scenario
- Focuses on PDPA compliance requirements
- Highlights potential violations or concerns

### Rule
- States the relevant legal provisions from PDPA sections
- References specific section numbers and requirements
- Explains the legal framework that applies

### Analysis
- Applies the legal rules to the specific facts
- Considers the circumstances and context
- Evaluates compliance or non-compliance

### Conclusion
- Provides clear legal conclusions
- States the risk level and potential consequences
- Offers actionable recommendations

## Risk Assessment

### Low Risk
- Scenario appears compliant with PDPA
- Minor procedural issues that can be easily addressed
- Good practices already in place

### Medium Risk
- Some compliance concerns identified
- Requires attention and corrective action
- Potential for penalties if not addressed

### High Risk
- Clear violations of PDPA requirements
- Significant compliance gaps
- High potential for penalties and enforcement action

## Key PDPA Sections

### Consent and Collection (Sections 11-20)
- **Section 11**: Compliance with Act
- **Section 12**: Policies and practices
- **Section 13**: Consent required
- **Section 14**: Provision of consent
- **Section 15**: Deemed consent
- **Section 18**: Notification of purpose
- **Section 19**: Purpose limitation
- **Section 20**: Limitation of purpose and extent

### Data Subject Rights (Sections 21-22)
- **Section 21**: Access to personal data
- **Section 22**: Correction of personal data

### Protection and Retention (Sections 23-26)
- **Section 23**: Protection of personal data
- **Section 24**: Retention of personal data
- **Section 25**: Transfer limitation
- **Section 26**: Accuracy of personal data

### Data Breach Notification (Sections 26A-26D)
- **Section 26A**: Notification of data breach
- **Section 26B**: Notification of data breach to Commission
- **Section 26C**: Notification of data breach to affected individuals
- **Section 26D**: Notification of data breach by data intermediary

### Do Not Call Registry (Sections 36-48)
- **Section 36**: Register
- **Section 43**: Duty to check register
- **Section 44**: Consent
- **Section 45**: Withdrawal of consent

### Offences and Penalties (Sections 48C-48F)
- **Section 48C**: Unauthorised disclosure of personal data
- **Section 48D**: Unauthorised use of personal data
- **Section 48E**: Unauthorised re-identification of anonymised information
- **Section 48F**: Offences by corporations

## Troubleshooting

### Common Issues

1. **"OpenAI API key not provided"**
   - Set the OPENAI_API_KEY environment variable
   - Or pass the api_key parameter when initializing

2. **"Error loading PDPA data"**
   - Ensure pdpa_sections.csv is in the current directory
   - Check that the CSV file is not corrupted

3. **"Advisor not ready"**
   - Check your internet connection
   - Verify your OpenAI API key is valid
   - Ensure you have sufficient API credits

4. **Poor quality results**
   - Try rephrasing your scenario with more specific details
   - Include relevant context about the organization and data processing
   - Consider breaking complex scenarios into smaller parts

### Performance Tips

1. **Be specific**: Include details about the type of data, processing purpose, and context
2. **Use clear language**: Avoid ambiguous terms and legal jargon
3. **Include relevant facts**: Mention timing, parties involved, and specific actions
4. **Consider the context**: Include information about the organization's size and industry

## Advanced Usage

### Custom Analysis
```python
# Get only relevant sections without full IRAC analysis
sections = advisor.search_relevant_sections("Your scenario", top_k=5)

# Generate advice with custom parameters
advice = advisor.generate_legal_advice("Your scenario")
```

### Batch Processing
```python
scenarios = [
    "Scenario 1...",
    "Scenario 2...",
    "Scenario 3..."
]

for i, scenario in enumerate(scenarios):
    print(f"Processing scenario {i+1}...")
    advice = advisor.generate_legal_advice(scenario)
    print(advisor.format_advice(advice))
```

### Integration with Other Tools
```python
# Save results to file
with open("legal_advice.txt", "w") as f:
    f.write(advisor.format_advice(advice))

# Export to JSON
import json
advice_dict = {
    "issue": advice.issue,
    "rule": advice.rule,
    "analysis": advice.analysis,
    "conclusion": advice.conclusion,
    "risk_level": advice.risk_level,
    "recommendations": advice.recommendations
}
json.dump(advice_dict, open("advice.json", "w"), indent=2)
```

## Legal Disclaimer

This tool is for educational and research purposes only. It does not constitute legal advice and should not be relied upon for actual legal matters. Always consult with qualified legal professionals for specific legal advice and compliance matters.

The tool is designed to help identify relevant PDPA provisions and provide general guidance, but it cannot replace professional legal analysis and advice tailored to specific circumstances.
