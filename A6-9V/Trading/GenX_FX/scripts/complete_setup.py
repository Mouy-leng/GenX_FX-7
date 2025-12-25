#!/usr/bin/env python3
"""
GenX-FX Complete Setup Script
Comprehensive setup for all agents, environments, and secrets management
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
import asyncio

class CompleteGenXSetup:
    """
    Complete setup for GenX-FX Autonomous Trading System
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.logger = logging.getLogger(__name__)
        
        # Setup results
        self.setup_results = {}
        
    def run_complete_setup(self) -> Dict[str, Any]:
        """Run complete setup process"""
        self.logger.info("Starting complete GenX-FX setup...")
        
        try:
            # Step 1: Collect all secrets
            print("🔍 Step 1: Collecting secrets from all drives...")
            secrets_result = self._collect_all_secrets()
            self.setup_results['secrets_collection'] = secrets_result
            
            # Step 2: Setup development environments
            print("🛠️ Step 2: Setting up development environments...")
            dev_env_result = self._setup_development_environments()
            self.setup_results['development_environments'] = dev_env_result
            
            # Step 3: Create agent notebooks
            print("📓 Step 3: Creating agent notebooks...")
            notebooks_result = self._create_agent_notebooks()
            self.setup_results['agent_notebooks'] = notebooks_result
            
            # Step 4: Setup virtual environments
            print("🐍 Step 4: Setting up virtual environments...")
            venv_result = self._setup_virtual_environments()
            self.setup_results['virtual_environments'] = venv_result
            
            # Step 5: Install dependencies
            print("📦 Step 5: Installing dependencies...")
            deps_result = self._install_dependencies()
            self.setup_results['dependencies'] = deps_result
            
            # Step 6: Configure IDE settings
            print("⚙️ Step 6: Configuring IDE settings...")
            ide_result = self._configure_ide_settings()
            self.setup_results['ide_configuration'] = ide_result
            
            # Step 7: Test system
            print("🧪 Step 7: Testing system...")
            test_result = self._test_system()
            self.setup_results['system_test'] = test_result
            
            # Generate final report
            self._generate_final_report()
            
            self.logger.info("Complete GenX-FX setup completed successfully")
            return self.setup_results
            
        except Exception as e:
            self.logger.error(f"Error in complete setup: {e}")
            return {'error': str(e)}
    
    def _collect_all_secrets(self) -> bool:
        """Collect secrets from all drives"""
        try:
            # Run secrets collection script
            script_path = self.base_path / 'scripts' / 'collect_all_secrets.py'
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, cwd=self.base_path)
            
            if result.returncode == 0:
                self.logger.info("Secrets collection completed successfully")
                return True
            else:
                self.logger.error(f"Secrets collection failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error collecting secrets: {e}")
            return False
    
    def _setup_development_environments(self) -> bool:
        """Setup all development environments"""
        try:
            # Run development environment setup script
            script_path = self.base_path / 'scripts' / 'setup_dev_env.py'
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, cwd=self.base_path)
            
            if result.returncode == 0:
                self.logger.info("Development environments setup completed successfully")
                return True
            else:
                self.logger.error(f"Development environments setup failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting up development environments: {e}")
            return False
    
    def _create_agent_notebooks(self) -> bool:
        """Create comprehensive agent notebooks"""
        try:
            notebooks_dir = self.base_path / 'notebooks'
            notebooks_dir.mkdir(exist_ok=True)
            
            # Create main agent notebook
            main_notebook = {
                "cells": [
                    {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [
                            "# GenX-FX Autonomous Trading System\n",
                            "\n",
                            "## 🤖 Complete Agent Configuration\n",
                            "\n",
                            "This notebook contains all configuration, secrets, and setup for the GenX-FX system."
                        ]
                    },
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": [
                            "# Import GenX-FX components\n",
                            "import sys\n",
                            "import os\n",
                            "from pathlib import Path\n",
                            "\n",
                            "# Add project root to path\n",
                            "project_root = Path.cwd().parent\n",
                            "sys.path.append(str(project_root))\n",
                            "\n",
                            "# Import all components\n",
                            "from core.autonomous_agent import AutonomousAgent, AgentConfig\n",
                            "from core.decision_engine import DecisionEngine, DecisionEngineConfig\n",
                            "from core.risk_manager import RiskManager, RiskLimits\n",
                            "from core.self_manager import SelfManager, SelfManagerConfig\n",
                            "from ml.model_registry import ModelRegistry, ModelRegistryConfig\n",
                            "from data.market_data import MarketDataManager, MarketDataConfig\n",
                            "from execution.broker_adapter import BrokerAdapter, BrokerConfig, BrokerType\n",
                            "from observability.metrics import MetricsCollector, MetricsConfig\n",
                            "\n",
                            "print(\"✅ GenX-FX components imported successfully\")\n",
                            "print(f\"📁 Project root: {project_root}\")\n",
                            "print(f\"🐍 Python version: {sys.version}\")"
                        ]
                    }
                ],
                "metadata": {
                    "kernelspec": {
                        "display_name": "Python 3",
                        "language": "python",
                        "name": "python3"
                    }
                },
                "nbformat": 4,
                "nbformat_minor": 4
            }
            
            # Write main notebook
            with open(notebooks_dir / 'GenX_FX_Main_Notebook.ipynb', 'w') as f:
                json.dump(main_notebook, f, indent=2)
            
            # Create individual agent notebooks
            agents = [
                'Autonomous_Agent',
                'Decision_Engine', 
                'Risk_Manager',
                'Self_Manager',
                'Model_Registry',
                'Market_Data',
                'Broker_Adapter',
                'Metrics_Collector'
            ]
            
            for agent in agents:
                agent_notebook = {
                    "cells": [
                        {
                            "cell_type": "markdown",
                            "metadata": {},
                            "source": [
                                f"# {agent} Configuration\n",
                                f"\n",
                                f"## 🤖 {agent} Setup and Configuration\n",
                                f"\n",
                                f"This notebook contains the configuration and setup for the {agent} component."
                            ]
                        }
                    ],
                    "metadata": {
                        "kernelspec": {
                            "display_name": "Python 3",
                            "language": "python",
                            "name": "python3"
                        }
                    },
                    "nbformat": 4,
                    "nbformat_minor": 4
                }
                
                with open(notebooks_dir / f'{agent}_Notebook.ipynb', 'w') as f:
                    json.dump(agent_notebook, f, indent=2)
            
            self.logger.info("Agent notebooks created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating agent notebooks: {e}")
            return False
    
    def _setup_virtual_environments(self) -> bool:
        """Setup virtual environments for different purposes"""
        try:
            venv_dir = self.base_path / 'venvs'
            venv_dir.mkdir(exist_ok=True)
            
            # Create main virtual environment
            main_venv = venv_dir / 'genx_main'
            if not main_venv.exists():
                subprocess.run([sys.executable, '-m', 'venv', str(main_venv)], check=True)
            
            # Create development virtual environment
            dev_venv = venv_dir / 'genx_dev'
            if not dev_venv.exists():
                subprocess.run([sys.executable, '-m', 'venv', str(dev_venv)], check=True)
            
            # Create testing virtual environment
            test_venv = venv_dir / 'genx_test'
            if not test_venv.exists():
                subprocess.run([sys.executable, '-m', 'venv', str(test_venv)], check=True)
            
            self.logger.info("Virtual environments created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up virtual environments: {e}")
            return False
    
    def _install_dependencies(self) -> bool:
        """Install all dependencies"""
        try:
            # Install main dependencies
            requirements_file = self.base_path / 'requirements.txt'
            if requirements_file.exists():
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)], 
                             check=True, cwd=self.base_path)
            
            # Install development dependencies
            dev_requirements = [
                'pytest',
                'pytest-asyncio',
                'black',
                'flake8',
                'mypy',
                'jupyter',
                'ipykernel'
            ]
            
            for dep in dev_requirements:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)
            
            self.logger.info("Dependencies installed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error installing dependencies: {e}")
            return False
    
    def _configure_ide_settings(self) -> bool:
        """Configure IDE settings for all environments"""
        try:
            # Create VS Code settings
            vscode_dir = self.base_path / '.vscode'
            vscode_dir.mkdir(exist_ok=True)
            
            vscode_settings = {
                "python.defaultInterpreterPath": "python3.9",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.formatting.provider": "black",
                "python.analysis.typeCheckingMode": "basic",
                "jupyter.askForKernelRestart": False,
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/*.pyc": True,
                    "**/.git": True,
                    "**/node_modules": True,
                    "**/venvs": True,
                    "**/backups": True
                },
                "python.terminal.activateEnvironment": True,
                "python.terminal.activateEnvInCurrentTerminal": True
            }
            
            with open(vscode_dir / 'settings.json', 'w') as f:
                json.dump(vscode_settings, f, indent=2)
            
            # Create launch configuration
            launch_config = {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "GenX-FX Main",
                        "type": "python",
                        "request": "launch",
                        "program": "${workspaceFolder}/main.py",
                        "console": "integratedTerminal",
                        "cwd": "${workspaceFolder}"
                    },
                    {
                        "name": "GenX-FX Test",
                        "type": "python",
                        "request": "launch",
                        "program": "${workspaceFolder}/tests/test_main.py",
                        "console": "integratedTerminal",
                        "cwd": "${workspaceFolder}"
                    }
                ]
            }
            
            with open(vscode_dir / 'launch.json', 'w') as f:
                json.dump(launch_config, f, indent=2)
            
            self.logger.info("IDE settings configured successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error configuring IDE settings: {e}")
            return False
    
    def _test_system(self) -> bool:
        """Test the system"""
        try:
            # Test imports
            test_script = """
import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent))

try:
    from core.autonomous_agent import AutonomousAgent
    from core.decision_engine import DecisionEngine
    from core.risk_manager import RiskManager
    from core.self_manager import SelfManager
    from ml.model_registry import ModelRegistry
    from data.market_data import MarketDataManager
    from execution.broker_adapter import BrokerAdapter
    from observability.metrics import MetricsCollector
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
"""
            
            result = subprocess.run([sys.executable, '-c', test_script], 
                                  capture_output=True, text=True, cwd=self.base_path)
            
            if result.returncode == 0:
                self.logger.info("System test passed successfully")
                return True
            else:
                self.logger.error(f"System test failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error testing system: {e}")
            return False
    
    def _generate_final_report(self) -> None:
        """Generate final setup report"""
        report_path = self.base_path / 'reports' / 'complete_setup_report.md'
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("# GenX-FX Complete Setup Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            
            # Setup summary
            f.write("## Setup Summary\n\n")
            total_steps = len(self.setup_results)
            successful_steps = sum(1 for result in self.setup_results.values() if result is True)
            
            f.write(f"- **Total Steps:** {total_steps}\n")
            f.write(f"- **Successful:** {successful_steps}\n")
            f.write(f"- **Failed:** {total_steps - successful_steps}\n")
            f.write(f"- **Success Rate:** {(successful_steps/total_steps)*100:.1f}%\n\n")
            
            # Detailed results
            f.write("## Detailed Results\n\n")
            for step, result in self.setup_results.items():
                status = "✅ Success" if result is True else "❌ Failed"
                f.write(f"- **{step.replace('_', ' ').title()}:** {status}\n")
            
            # Next steps
            f.write("\n## Next Steps\n\n")
            f.write("1. **Review Secrets:** Check 'config/consolidated_secrets.env'\n")
            f.write("2. **Update Credentials:** Fill in missing API keys\n")
            f.write("3. **Test Connections:** Verify all external services\n")
            f.write("4. **Run System:** Execute 'python main.py'\n")
            f.write("5. **Monitor Performance:** Watch the system dashboard\n")
            f.write("6. **Review Reports:** Check all generated reports\n")
            
            # File structure
            f.write("\n## Generated Files\n\n")
            f.write("- `config/consolidated_secrets.env` - All collected secrets\n")
            f.write("- `notebooks/` - Agent configuration notebooks\n")
            f.write("- `reports/` - Comprehensive setup reports\n")
            f.write("- `.vscode/` - VS Code configuration\n")
            f.write("- `venvs/` - Virtual environments\n")
            f.write("- `backups/` - Secure backups of secrets\n")
        
        self.logger.info(f"Final setup report generated: {report_path}")


def main():
    """Main function to run complete setup"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Starting Complete GenX-FX Setup...")
    print("="*60)
    
    # Initialize setup
    setup = CompleteGenXSetup()
    
    # Run complete setup
    results = setup.run_complete_setup()
    
    print("\n" + "="*60)
    print("🎉 COMPLETE GENX-FX SETUP FINISHED")
    print("="*60)
    
    # Display results
    total_steps = len(results)
    successful_steps = sum(1 for result in results.values() if result is True)
    
    print(f"📊 Setup Results: {successful_steps}/{total_steps} steps completed successfully")
    print(f"📈 Success Rate: {(successful_steps/total_steps)*100:.1f}%")
    
    print("\n📁 Generated Files:")
    print("- 📋 Reports: 'reports/' directory")
    print("- 🔐 Secrets: 'config/consolidated_secrets.env'")
    print("- 📓 Notebooks: 'notebooks/' directory")
    print("- ⚙️ IDE Config: '.vscode/' directory")
    print("- 🐍 Virtual Envs: 'venvs/' directory")
    print("- 💾 Backups: 'backups/' directory")
    
    print("\n🔧 Development Environments Configured:")
    print("- ✅ Cursor IDE")
    print("- ✅ PyCharm Professional")
    print("- ✅ Visual Studio Code")
    print("- ✅ Jupyter Notebooks")
    
    print("\n📋 Next Steps:")
    print("1. Review 'config/consolidated_secrets.env'")
    print("2. Update missing API keys and credentials")
    print("3. Test system: python main.py")
    print("4. Monitor performance in notebooks")
    print("5. Check reports for detailed information")
    
    if successful_steps == total_steps:
        print("\n🎉 All setup steps completed successfully!")
        print("🚀 Your GenX-FX Autonomous Trading System is ready!")
    else:
        print(f"\n⚠️ {total_steps - successful_steps} setup steps failed")
        print("📋 Check the setup report for details")


if __name__ == "__main__":
    main()
