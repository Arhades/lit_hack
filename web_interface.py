#!/usr/bin/env python3
"""
Web interface for PDPA Legal Advisor using Flask
"""

from flask import Flask, render_template, request, jsonify
from pdpa_legal_advisor import PDPALegalAdvisor
import os

app = Flask(__name__)

# Initialize the advisor
advisor = None
advisor_ready = False

def init_advisor():
    """Initialize the advisor with proper error handling"""
    global advisor, advisor_ready
    try:
        advisor = PDPALegalAdvisor("pdpa_sections.csv")
        advisor_ready = True
        print("✅ PDPA Legal Advisor initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing advisor: {e}")
        advisor_ready = False

# Initialize on startup
init_advisor()

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

@app.route('/reinit', methods=['POST'])
def reinit():
    """Reinitialize the advisor"""
    global advisor, advisor_ready
    try:
        init_advisor()
        return jsonify({
            'success': True,
            'message': 'Advisor reinitialized successfully' if advisor_ready else 'Failed to initialize advisor',
            'advisor_ready': advisor_ready
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}',
            'advisor_ready': advisor_ready
        }), 500

if __name__ == '__main__':
    # Try different ports if 5000 is in use
    import socket
    
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    port = 5000
    try:
        # Test if port 5000 is available
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 5000))
        print(f"🚀 Starting web interface on port {port}")
    except OSError:
        port = find_free_port()
        print(f"⚠️  Port 5000 in use, using port {port}")
    
    print(f"🌐 Open your browser to: http://localhost:{port}")
    print(f"🌐 Alternative URL: http://127.0.0.1:{port}")
    print(f"🌐 Network URL: http://10.119.143.159:{port}")
    app.run(debug=True, host='127.0.0.1', port=port)
