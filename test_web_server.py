#!/usr/bin/env python3
"""
Test script to verify web server is working
"""

import requests
import time
import subprocess
import sys

def test_web_server():
    """Test if the web server is accessible"""
    
    # Common ports to test
    ports_to_test = [5000, 5001, 5002, 6000, 7000, 8000, 9000]
    
    print("🔍 Testing web server connectivity...")
    
    for port in ports_to_test:
        try:
            print(f"   Testing port {port}...", end=" ")
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Working!")
                data = response.json()
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Advisor ready: {data.get('advisor_ready', False)}")
                print(f"   🌐 Use this URL: http://localhost:{port}")
                return port
            else:
                print(f"❌ Status {response.status_code}")
        except requests.exceptions.RequestException:
            print("❌ Not responding")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n❌ No working web server found!")
    print("💡 Try starting the web interface manually:")
    print("   python3 web_interface.py")
    return None

def start_web_server():
    """Start the web server in background"""
    print("🚀 Starting web server...")
    try:
        process = subprocess.Popen([sys.executable, "web_interface.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        print("✅ Web server started in background")
        print("⏳ Waiting 5 seconds for server to initialize...")
        time.sleep(5)
        return process
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Web Server Test\n")
    
    # First test if server is already running
    port = test_web_server()
    
    if port is None:
        print("\n🔄 No server found, starting one...")
        process = start_web_server()
        
        if process:
            print("\n🔍 Testing again...")
            port = test_web_server()
            
            if port:
                print(f"\n🎉 Web server is working on port {port}!")
                print(f"🌐 Open your browser to: http://localhost:{port}")
            else:
                print("\n❌ Web server failed to start properly")
        else:
            print("\n❌ Could not start web server")
    else:
        print(f"\n🎉 Web server is already working on port {port}!")
        print(f"🌐 Open your browser to: http://localhost:{port}")
