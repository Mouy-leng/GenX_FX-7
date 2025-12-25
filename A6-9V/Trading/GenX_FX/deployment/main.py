import functions_framework
from flask import jsonify
import os
from datetime import datetime

# Your CLIENT_ID configuration
CLIENT_ID = "723463751699-hu9v70at667lbo9e77mje9rugqq39hon.apps.googleusercontent.com"

@functions_framework.http
def genx_fx_autonomous_agent(request):
    """
    GenX-FX Autonomous Agent Cloud Function
    HTTP endpoint for the autonomous trading agent
    """
    
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    # Set CORS headers for actual requests
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    try:
        if request.method == 'GET':
            # Return agent status
            response_data = {
                'success': True,
                'message': 'GenX-FX Autonomous Agent is running',
                'client_id': CLIENT_ID,
                'project_id': os.environ.get('GCP_PROJECT', 'genx-fx-autonomous-trading'),
                'timestamp': datetime.now().isoformat(),
                'status': {
                    'state': 'initialized',
                    'version': '1.0.0',
                    'deployed': True
                },
                'endpoints': {
                    'status': 'GET /',
                    'start_trading': 'POST / with {"action": "start"}',
                    'pause_trading': 'POST / with {"action": "pause"}',
                    'get_performance': 'POST / with {"action": "performance"}'
                }
            }
            return jsonify(response_data), 200, headers
            
        elif request.method == 'POST':
            # Handle trading commands
            data = request.get_json() or {}
            action = data.get('action', 'status')
            
            if action == 'start':
                return jsonify({
                    'success': True,
                    'message': 'Trading started successfully',
                    'action': 'start',
                    'timestamp': datetime.now().isoformat()
                }), 200, headers
                
            elif action == 'pause':
                return jsonify({
                    'success': True,
                    'message': 'Trading paused successfully',
                    'action': 'pause',
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
                        'max_drawdown': 0.0
                    },
                    'timestamp': datetime.now().isoformat()
                }), 200, headers
                
            elif action == 'status':
                return jsonify({
                    'success': True,
                    'status': {
                        'state': 'running',
                        'client_id': CLIENT_ID,
                        'uptime': '0 seconds',
                        'last_update': datetime.now().isoformat()
                    }
                }), 200, headers
                
            else:
                return jsonify({
                    'success': False,
                    'error': f'Unknown action: {action}',
                    'available_actions': ['start', 'pause', 'performance', 'status']
                }), 400, headers
                
        else:
            return jsonify({
                'success': False,
                'error': 'Method not allowed'
            }), 405, headers
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500, headers