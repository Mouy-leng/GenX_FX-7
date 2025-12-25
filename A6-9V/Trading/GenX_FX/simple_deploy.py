#!/usr/bin/env python3
"""
Simple GenX-FX Cloud Function Deployment
Uses your CLIENT_ID: 723463751699-hu9v70at667lbo9e77mje9rugqq39hon.apps.googleusercontent.com
"""

import subprocess
import os
from pathlib import Path

def deploy_simple_function():
    """Deploy a simple Cloud Function"""
    
    CLIENT_ID = "723463751699-hu9v70at667lbo9e77mje9rugqq39hon.apps.googleusercontent.com"
    PROJECT_ID = "genx-fx-autonomous-trading"
    FUNCTION_NAME = "genx-fx-agent"
    REGION = "us-central1"
    
    print("🚀 GenX-FX Simple Cloud Function Deployment")
    print("=" * 50)
    print(f"📱 Client ID: {CLIENT_ID}")
    print(f"📦 Project: {PROJECT_ID}")
    print(f"⚡ Function: {FUNCTION_NAME}")
    print("=" * 50)
    
    # Change to deployment directory
    deployment_dir = Path("deployment")
    if not deployment_dir.exists():
        print("❌ Deployment directory not found!")
        return False
    
    os.chdir(deployment_dir)
    
    try:
        # Try to deploy the function
        print("🔧 Deploying Cloud Function...")
        
        cmd = [
            "gcloud", "functions", "deploy", FUNCTION_NAME,
            "--runtime", "python39",
            "--trigger-http",
            "--allow-unauthenticated",
            "--memory", "512MB",
            "--timeout", "60s",
            "--region", REGION,
            "--entry-point", "genx_fx_autonomous_agent"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            
            # Get function URL
            url_cmd = [
                "gcloud", "functions", "describe", FUNCTION_NAME,
                "--region", REGION,
                "--format", "value(httpsTrigger.url)"
            ]
            
            url_result = subprocess.run(url_cmd, capture_output=True, text=True)
            function_url = url_result.stdout.strip()
            
            print(f"🔗 Function URL: {function_url}")
            print("\n📋 Test your function:")
            print(f"GET {function_url}")
            print(f"POST {function_url} with JSON: {{\"action\": \"start\"}}")
            
            return True
            
        else:
            print("❌ Deployment failed!")
            print(f"Error: {result.stderr}")
            
            if "billing" in result.stderr.lower():
                print("\n💳 BILLING ISSUE DETECTED!")
                print("🔧 Solutions:")
                print("1. Enable billing in Google Cloud Console:")
                print("   https://console.cloud.google.com/billing")
                print("2. Or use a different project with billing enabled")
                print("3. Or deploy to a free service like Heroku")
            
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_alternative_options():
    """Show alternative deployment options"""
    print("\n🔄 Alternative Deployment Options:")
    print("=" * 50)
    print("1. 🆓 Heroku Free Tier")
    print("   - Deploy Python Flask app to Heroku")
    print("   - No billing required")
    print("   - Easy deployment with git")
    
    print("\n2. 🐳 Local Docker Container")
    print("   - Run the agent locally in Docker")
    print("   - Full control over environment")
    print("   - No cloud costs")
    
    print("\n3. 🖥️ Local Development Server")
    print("   - Run Flask dev server locally")
    print("   - Test functionality before cloud deployment")
    print("   - Use ngrok for external access")
    
    print("\n4. ☁️ Other Cloud Providers")
    print("   - AWS Lambda (has free tier)")
    print("   - Azure Functions (has free tier)")
    print("   - Vercel (free for personal projects)")

def create_local_server():
    """Create a local development server"""
    local_server_code = '''
import os
from datetime import datetime
from flask import Flask, jsonify, request

# Your CLIENT_ID
CLIENT_ID = "723463751699-hu9v70at667lbo9e77mje9rugqq39hon.apps.googleusercontent.com"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def genx_fx_autonomous_agent():
    """GenX-FX Autonomous Agent Local Server"""
    
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    headers = {'Access-Control-Allow-Origin': '*'}
    
    try:
        if request.method == 'GET':
            return jsonify({
                'success': True,
                'message': 'GenX-FX Autonomous Agent - Local Development Server',
                'client_id': CLIENT_ID,
                'server': 'local',
                'timestamp': datetime.now().isoformat(),
                'status': {
                    'state': 'development',
                    'version': '1.0.0-local',
                    'deployed': True
                }
            }), 200, headers
            
        elif request.method == 'POST':
            data = request.get_json() or {}
            action = data.get('action', 'status')
            
            return jsonify({
                'success': True,
                'message': f'Action "{action}" processed locally',
                'action': action,
                'client_id': CLIENT_ID,
                'timestamp': datetime.now().isoformat()
            }), 200, headers
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500, headers

if __name__ == '__main__':
    print("🚀 Starting GenX-FX Local Development Server...")
    print(f"🔑 Client ID: {CLIENT_ID}")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📋 Test endpoints:")
    print("   GET  http://localhost:5000")
    print("   POST http://localhost:5000 with JSON data")
    print("⏹️ Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open("local_server.py", "w") as f:
        f.write(local_server_code)
    
    print("✅ Created local_server.py")
    print("🏃 Run with: python local_server.py")

if __name__ == "__main__":
    success = deploy_simple_function()
    
    if not success:
        show_alternative_options()
        print("\n💡 Creating local development server as fallback...")
        create_local_server()
        
        print("\n🎯 RECOMMENDED NEXT STEPS:")
        print("1. Enable billing in Google Cloud Console")
        print("2. Or run locally: python local_server.py")
        print("3. Or deploy to Heroku for free cloud hosting")