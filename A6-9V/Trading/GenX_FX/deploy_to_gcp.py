#!/usr/bin/env python3
"""
GenX-FX Autonomous Agent - Google Cloud Deployment Script
Deploys the autonomous trading agent to Google Cloud Platform
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

class GCPDeployment:
    """
    Deploy GenX-FX Autonomous Agent to Google Cloud Platform
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self.logger = logging.getLogger(__name__)
        
        # Your Google Cloud configuration
        self.client_id = "723463751699-hu9v70at667lbo9e77mje9rugqq39hon.apps.googleusercontent.com"
        self.project_id = None  # Will be detected or set
        
        # Deployment configuration
        self.deployment_config = {
            'function_name': 'genx-fx-autonomous-agent',
            'runtime': 'python39',
            'memory': '2048MB',
            'timeout': '540s',
            'trigger': 'https',
            'region': 'us-central1',
            'source_dir': str(self.base_path)
        }
        
    def deploy_autonomous_agent(self) -> Dict[str, Any]:
        """Deploy the autonomous agent to Google Cloud"""
        self.logger.info("Starting Google Cloud deployment...")
        
        try:
            # Step 1: Setup Google Cloud project
            project_setup = self._setup_gcp_project()
            if not project_setup['success']:
                return project_setup
            
            # Step 2: Prepare deployment files
            prep_result = self._prepare_deployment_files()
            if not prep_result['success']:
                return prep_result
            
            # Step 3: Deploy to Cloud Functions
            deploy_result = self._deploy_to_cloud_functions()
            if not deploy_result['success']:
                return deploy_result
            
            # Step 4: Setup authentication
            auth_result = self._setup_oauth_authentication()
            if not auth_result['success']:
                return auth_result
            
            # Step 5: Configure environment variables
            env_result = self._configure_environment_variables()
            
            return {
                'success': True,
                'message': 'Autonomous agent deployed successfully to Google Cloud',
                'deployment_url': deploy_result.get('url'),
                'project_id': self.project_id,
                'function_name': self.deployment_config['function_name']
            }
            
        except Exception as e:
            self.logger.error(f"Deployment failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _setup_gcp_project(self) -> Dict[str, Any]:
        """Setup Google Cloud project"""
        try:
            # Get current project or create new one
            result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                self.project_id = result.stdout.strip()
                self.logger.info(f"Using existing project: {self.project_id}")
            else:
                # Extract project ID from client ID
                project_id = self.client_id.split('-')[0]
                self.project_id = f"genx-fx-{project_id}"
                
                # Set project
                subprocess.run(['gcloud', 'config', 'set', 'project', self.project_id], 
                             check=True)
                self.logger.info(f"Set project: {self.project_id}")
            
            # Enable required APIs
            apis_to_enable = [
                'cloudfunctions.googleapis.com',
                'cloudbuild.googleapis.com',
                'cloudresourcemanager.googleapis.com',
                'iam.googleapis.com'
            ]
            
            for api in apis_to_enable:
                subprocess.run(['gcloud', 'services', 'enable', api], check=True)
                self.logger.info(f"Enabled API: {api}")
            
            return {
                'success': True,
                'project_id': self.project_id
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f"Failed to setup GCP project: {e}"
            }
    
    def _prepare_deployment_files(self) -> Dict[str, Any]:
        """Prepare files for deployment"""
        try:
            # Create deployment directory
            deploy_dir = self.base_path / 'deployment'
            deploy_dir.mkdir(exist_ok=True)
            
            # Create main.py for Cloud Functions
            main_py_content = '''
import functions_framework
import asyncio
import logging
from flask import jsonify
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import the autonomous agent
from core.autonomous_agent import AutonomousAgent, AgentConfig
from core.decision_engine import DecisionEngine
from core.risk_manager import RiskManager
from core.self_manager import SelfManager
from ml.model_registry import ModelRegistry
from data.market_data import MarketDataManager
from execution.broker_adapter import BrokerAdapter
from observability.metrics import MetricsCollector

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agent instance
agent = None

@functions_framework.http
def genx_fx_autonomous_agent(request):
    """Main Cloud Function entry point"""
    global agent
    
    try:
        # Initialize agent if not already done
        if agent is None:
            logger.info("Initializing GenX-FX Autonomous Agent...")
            agent = initialize_agent()
        
        # Handle different request types
        if request.method == 'GET':
            return handle_status_request()
        elif request.method == 'POST':
            return handle_trading_request(request)
        else:
            return jsonify({'error': 'Method not allowed'}), 405
            
    except Exception as e:
        logger.error(f"Error in Cloud Function: {e}")
        return jsonify({'error': str(e)}), 500

def initialize_agent():
    """Initialize the autonomous agent"""
    try:
        # Create agent configuration
        config = AgentConfig(
            max_risk_per_trade=float(os.environ.get('MAX_RISK_PER_TRADE', 0.02)),
            max_daily_loss=float(os.environ.get('MAX_DAILY_LOSS', 0.05)),
            learning_rate=float(os.environ.get('LEARNING_RATE', 0.001)),
            auto_update_enabled=os.environ.get('AUTO_UPDATE_ENABLED', 'true').lower() == 'true'
        )
        
        # Initialize agent
        agent = AutonomousAgent(config)
        
        # Initialize components (mock for cloud deployment)
        market_data = MarketDataManager()
        broker = BrokerAdapter()
        model_registry = ModelRegistry()
        decision_engine = DecisionEngine()
        self_manager = SelfManager()
        metrics = MetricsCollector()
        
        # Run async initialization
        asyncio.run(agent.initialize(
            market_data=market_data,
            broker=broker,
            model_registry=model_registry,
            decision_engine=decision_engine,
            self_manager=self_manager,
            metrics=metrics
        ))
        
        logger.info("Autonomous agent initialized successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        raise

def handle_status_request():
    """Handle status requests"""
    try:
        status = agent.get_status()
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def handle_trading_request(request):
    """Handle trading requests"""
    try:
        data = request.get_json() or {}
        action = data.get('action', 'status')
        
        if action == 'start':
            # Start trading
            asyncio.run(agent.start_trading())
            return jsonify({'success': True, 'message': 'Trading started'})
        elif action == 'pause':
            # Pause trading
            asyncio.run(agent.pause_trading())
            return jsonify({'success': True, 'message': 'Trading paused'})
        elif action == 'resume':
            # Resume trading
            asyncio.run(agent.resume_trading())
            return jsonify({'success': True, 'message': 'Trading resumed'})
        elif action == 'status':
            return handle_status_request()
        else:
            return jsonify({'error': 'Unknown action'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''
            
            # Write main.py
            with open(deploy_dir / 'main.py', 'w') as f:
                f.write(main_py_content)
            
            # Create requirements.txt for Cloud Functions
            requirements_content = """
functions-framework==3.4.0
flask==2.3.3
numpy==1.24.3
pandas==2.0.3
asyncio-mqtt==0.13.0
aiohttp==3.8.5
python-dotenv==1.0.0
pyyaml==6.0.1
"""
            
            with open(deploy_dir / 'requirements.txt', 'w') as f:
                f.write(requirements_content.strip())
            
            # Copy source files
            import shutil
            
            # Copy core modules
            for module in ['core', 'ml', 'data', 'execution', 'observability']:
                src_dir = self.base_path / module
                if src_dir.exists():
                    dest_dir = deploy_dir / module
                    if dest_dir.exists():
                        shutil.rmtree(dest_dir)
                    shutil.copytree(src_dir, dest_dir)
            
            self.logger.info("Deployment files prepared successfully")
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _deploy_to_cloud_functions(self) -> Dict[str, Any]:
        """Deploy to Google Cloud Functions"""
        try:
            deploy_dir = self.base_path / 'deployment'
            
            # Build deployment command
            cmd = [
                'gcloud', 'functions', 'deploy', self.deployment_config['function_name'],
                '--runtime', self.deployment_config['runtime'],
                '--trigger-http',
                '--allow-unauthenticated',
                '--memory', self.deployment_config['memory'],
                '--timeout', self.deployment_config['timeout'],
                '--region', self.deployment_config['region'],
                '--source', str(deploy_dir),
                '--entry-point', 'genx_fx_autonomous_agent'
            ]
            
            # Execute deployment
            self.logger.info(f"Deploying function: {self.deployment_config['function_name']}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=deploy_dir)
            
            if result.returncode == 0:
                # Extract function URL
                url_cmd = [
                    'gcloud', 'functions', 'describe', self.deployment_config['function_name'],
                    '--region', self.deployment_config['region'],
                    '--format', 'value(httpsTrigger.url)'
                ]
                
                url_result = subprocess.run(url_cmd, capture_output=True, text=True)
                function_url = url_result.stdout.strip() if url_result.returncode == 0 else None
                
                self.logger.info("Cloud Function deployed successfully")
                return {
                    'success': True,
                    'url': function_url,
                    'message': 'Function deployed successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f"Deployment failed: {result.stderr}"
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _setup_oauth_authentication(self) -> Dict[str, Any]:
        """Setup OAuth 2.0 authentication"""
        try:
            # Create OAuth consent screen configuration
            oauth_config = {
                'client_id': self.client_id,
                'project_id': self.project_id,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
                'redirect_uris': [
                    f'https://{self.deployment_config["region"]}-{self.project_id}.cloudfunctions.net/{self.deployment_config["function_name"]}'
                ]
            }
            
            # Save OAuth configuration
            oauth_file = self.base_path / 'config' / 'oauth_config.json'
            oauth_file.parent.mkdir(exist_ok=True)
            
            with open(oauth_file, 'w') as f:
                json.dump(oauth_config, f, indent=2)
            
            self.logger.info("OAuth configuration saved")
            return {'success': True, 'oauth_config': oauth_config}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _configure_environment_variables(self) -> Dict[str, Any]:
        """Configure environment variables for the Cloud Function"""
        try:
            # Define environment variables
            env_vars = {
                'GOOGLE_CLIENT_ID': self.client_id,
                'PROJECT_ID': self.project_id,
                'MAX_RISK_PER_TRADE': '0.02',
                'MAX_DAILY_LOSS': '0.05',
                'LEARNING_RATE': '0.001',
                'AUTO_UPDATE_ENABLED': 'true',
                'PYTHON_ENV': 'production'
            }
            
            # Update function with environment variables
            env_vars_str = ','.join([f"{k}={v}" for k, v in env_vars.items()])
            
            cmd = [
                'gcloud', 'functions', 'deploy', self.deployment_config['function_name'],
                '--update-env-vars', env_vars_str,
                '--region', self.deployment_config['region']
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("Environment variables configured")
                return {'success': True, 'env_vars': env_vars}
            else:
                self.logger.warning(f"Failed to set env vars: {result.stderr}")
                return {'success': False, 'error': result.stderr}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_deployment(self, function_url: str) -> Dict[str, Any]:
        """Test the deployed function"""
        try:
            import requests
            
            # Test status endpoint
            response = requests.get(function_url)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'response': response.json(),
                    'status_code': response.status_code
                }
            else:
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': response.text
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


def main():
    """Main deployment function"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Starting Google Cloud deployment for GenX-FX Autonomous Agent...")
    print("=" * 70)
    
    # Initialize deployment
    deployment = GCPDeployment()
    
    # Deploy the autonomous agent
    result = deployment.deploy_autonomous_agent()
    
    print("\n" + "=" * 70)
    if result['success']:
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 70)
        print(f"🔗 Function URL: {result.get('deployment_url', 'N/A')}")
        print(f"📦 Project ID: {result.get('project_id')}")
        print(f"⚡ Function Name: {result.get('function_name')}")
        print(f"🔑 Client ID: {deployment.client_id}")
        
        # Test deployment if URL is available
        if result.get('deployment_url'):
            print("\n🧪 Testing deployment...")
            test_result = deployment.test_deployment(result['deployment_url'])
            if test_result['success']:
                print("✅ Deployment test successful!")
                print(f"📊 Status: {test_result.get('response', {}).get('status', 'Unknown')}")
            else:
                print("⚠️ Deployment test failed (this is normal for initial deployment)")
        
        print("\n📋 Next Steps:")
        print("1. Configure OAuth consent screen in Google Cloud Console")
        print("2. Add authorized domains for your application")
        print("3. Test the function with HTTP requests")
        print("4. Monitor function logs in Google Cloud Console")
        print("5. Set up monitoring and alerting")
        
    else:
        print("❌ DEPLOYMENT FAILED!")
        print("=" * 70)
        print(f"Error: {result.get('error')}")
        print("\n📋 Troubleshooting:")
        print("1. Check your Google Cloud authentication")
        print("2. Verify project permissions")
        print("3. Ensure required APIs are enabled")
        print("4. Check deployment logs for details")


if __name__ == "__main__":
    main()