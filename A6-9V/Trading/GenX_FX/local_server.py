#!/usr/bin/env python3
"""
GenX-FX Autonomous Agent - Local Development Server
Uses your CLIENT_ID: 723463751699-hu9v70at667lbo9e77mje9rugqq39hon.apps.googleusercontent.com
"""

import os
from datetime import datetime
from flask import Flask, jsonify, request

# Your CLIENT_ID configuration
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
                },
                'endpoints': {
                    'status': 'GET /',
                    'start_trading': 'POST / with {"action": "start"}',
                    'pause_trading': 'POST / with {"action": "pause"}',
                    'performance': 'POST / with {"action": "performance"}'
                }
            }), 200, headers
            
        elif request.method == 'POST':
            data = request.get_json() or {}
            action = data.get('action', 'status')
            
            if action == 'start':
                return jsonify({
                    'success': True,
                    'message': 'Trading started successfully',
                    'action': 'start',
                    'client_id': CLIENT_ID,
                    'timestamp': datetime.now().isoformat()
                }), 200, headers
                
            elif action == 'pause':
                return jsonify({
                    'success': True,
                    'message': 'Trading paused successfully',
                    'action': 'pause',
                    'client_id': CLIENT_ID,
                    'timestamp': datetime.now().isoformat()
                }), 200, headers
                
            elif action == 'performance':
                return jsonify({
                    'success': True,
                    'performance': {
                        'total_trades': 0,
                        'profit_loss': 0.0,
                        'win_rate': 0.0,
                        'sharpe_ratio': 0.0,
                        'max_drawdown': 0.0,
                        'uptime': '5 minutes'
                    },
                    'client_id': CLIENT_ID,
                    'timestamp': datetime.now().isoformat()
                }), 200, headers
                
            elif action == 'status':
                return jsonify({
                    'success': True,
                    'status': {
                        'state': 'running',
                        'client_id': CLIENT_ID,
                        'uptime': '5 minutes',
                        'last_update': datetime.now().isoformat(),
                        'server': 'local'
                    }
                }), 200, headers
                
            else:
                return jsonify({
                    'success': False,
                    'error': f'Unknown action: {action}',
                    'available_actions': ['start', 'pause', 'performance', 'status'],
                    'client_id': CLIENT_ID
                }), 400, headers
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'client_id': CLIENT_ID,
            'timestamp': datetime.now().isoformat()
        }), 500, headers

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'GenX-FX Autonomous Agent',
        'client_id': CLIENT_ID,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("  GenX-FX Autonomous Agent - Local Development Server")
    print("=" * 60)
    print(f"Client ID: {CLIENT_ID}")
    print("Server URL: http://localhost:5000")
    print("Health Check: http://localhost:5000/health")
    print("=" * 60)
    print("Test Commands:")
    print("  GET  http://localhost:5000")
    print("  POST http://localhost:5000 with JSON: {\"action\": \"start\"}")
    print("  POST http://localhost:5000 with JSON: {\"action\": \"performance\"}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Use production-ready settings to prevent crashes
    port = int(os.environ.get('SERVER_PORT', 5000))
    host = os.environ.get('SERVER_HOST', '127.0.0.1')
    
    try:
        app.run(debug=False, host=host, port=port, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        import sys
        sys.exit(1)
