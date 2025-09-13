#!/usr/bin/env python3
"""
Web interface for PDPA Legal Advisor using Flask
"""

from flask import Flask, render_template, request, jsonify
from pdpa_legal_advisor import PDPALegalAdvisor
import os

app = Flask(__name__)

# Initialize the advisor
try:
    advisor = PDPALegalAdvisor("pdpa_sections.csv")
    advisor_ready = True
except Exception as e:
    print(f"Error initializing advisor: {e}")
    advisor_ready = False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', advisor_ready=advisor_ready)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a legal scenario"""
    if not advisor_ready:
        return jsonify({'error': 'Advisor not ready. Please check configuration.'}), 500
    
    try:
        data = request.get_json()
        scenario = data.get('scenario', '')
        
        if not scenario:
            return jsonify({'error': 'No scenario provided'}), 400
        
        # Generate legal advice
        advice = advisor.generate_legal_advice(scenario)
        
        # Convert to JSON-serializable format
        result = {
            'issue': advice.issue,
            'rule': advice.rule,
            'analysis': advice.analysis,
            'conclusion': advice.conclusion,
            'risk_level': advice.risk_level,
            'recommendations': advice.recommendations,
            'relevant_sections': advice.relevant_sections
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if advisor_ready else 'unhealthy',
        'advisor_ready': advisor_ready
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
