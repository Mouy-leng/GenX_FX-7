#!/usr/bin/env python3
"""
GenX-FX Development Environment Setup
Automatically configures all coding environments and collects secrets
"""

import os
import json
import yaml
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import subprocess
import sys

class DevelopmentEnvironmentSetup:
    """
    Comprehensive development environment setup for GenX-FX
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.logger = logging.getLogger(__name__)
        
        # Development environments
        self.environments = {
            'cursor': {
                'name': 'Cursor IDE',
                'config_path': 'C:/Users/lengk/.cursor',
                'workspace_path': str(self.base_path),
                'extensions': [
                    'ms-python.python',
                    'ms-toolsai.jupyter',
                    'ms-python.pylint',
                    'ms-python.black-formatter',
                    'eamodio.gitlens',
                    'ms-vscode.vscode-json'
                ]
            },
            'pycharm': {
                'name': 'PyCharm Professional',
                'config_path': 'C:/Users/lengk/.PyCharm',
                'project_path': str(self.base_path),
                'interpreter': 'python3.9',
                'plugins': [
                    'com.intellij.python',
                    'org.jetbrains.plugins.jupyter',
                    'com.intellij.plugins.python',
                    'org.jetbrains.plugins.git'
                ]
            },
            'vscode': {
                'name': 'Visual Studio Code',
                'config_path': 'C:/Users/lengk/.vscode',
                'workspace_path': str(self.base_path),
                'extensions': [
                    'ms-python.python',
                    'ms-toolsai.jupyter',
                    'ms-python.pylint',
                    'ms-python.black-formatter',
                    'eamodio.gitlens',
                    'ms-vscode.vscode-json',
                    'ms-python.flake8',
                    'ms-python.mypy-type-checker'
                ]
            }
        }
        
        # Secret locations
        self.secret_locations = {
            'google_drive_g': 'G:/',
            'google_drive_h': 'H:/',
            'dropbox': 'C:/Users/lengk/Dropbox/',
            'onedrive': 'C:/Users/lengk/OneDrive/',
            'desktop': 'C:/Users/lengk/Desktop/',
            'documents': 'C:/Users/lengk/Documents/',
            'downloads': 'C:/Users/lengk/Downloads/'
        }
    
    def setup_all_environments(self) -> Dict[str, bool]:
        """Setup all development environments"""
        results = {}
        
        for env_name, env_config in self.environments.items():
            try:
                self.logger.info(f"Setting up {env_config['name']}...")
                success = self._setup_environment(env_name, env_config)
                results[env_name] = success
                
                if success:
                    self.logger.info(f"✅ {env_config['name']} setup completed")
                else:
                    self.logger.warning(f"⚠️ {env_config['name']} setup failed")
                    
            except Exception as e:
                self.logger.error(f"❌ Error setting up {env_config['name']}: {e}")
                results[env_name] = False
        
        return results
    
    def _setup_environment(self, env_name: str, env_config: Dict[str, Any]) -> bool:
        """Setup individual development environment"""
        try:
            if env_name == 'cursor':
                return self._setup_cursor(env_config)
            elif env_name == 'pycharm':
                return self._setup_pycharm(env_config)
            elif env_name == 'vscode':
                return self._setup_vscode(env_config)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting up {env_name}: {e}")
            return False
    
    def _setup_cursor(self, config: Dict[str, Any]) -> bool:
        """Setup Cursor IDE"""
        try:
            # Create Cursor workspace configuration
            workspace_config = {
                "folders": [
                    {
                        "path": config['workspace_path'],
                        "name": "GenX-FX Trading System"
                    }
                ],
                "settings": {
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
                        "**/node_modules": True
                    }
                },
                "extensions": {
                    "recommendations": config['extensions']
                }
            }
            
            # Write workspace file
            workspace_file = self.base_path / 'GenX-FX.code-workspace'
            with open(workspace_file, 'w') as f:
                json.dump(workspace_config, f, indent=2)
            
            # Create Cursor settings
            cursor_settings = {
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
                    "**/node_modules": True
                }
            }
            
            # Write settings file
            settings_file = self.base_path / '.vscode' / 'settings.json'
            settings_file.parent.mkdir(exist_ok=True)
            with open(settings_file, 'w') as f:
                json.dump(cursor_settings, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Cursor: {e}")
            return False
    
    def _setup_pycharm(self, config: Dict[str, Any]) -> bool:
        """Setup PyCharm Professional"""
        try:
            # Create PyCharm project configuration
            project_config = {
                "name": "GenX-FX Trading System",
                "path": config['project_path'],
                "interpreter": config['interpreter'],
                "plugins": config['plugins'],
                "settings": {
                    "python.interpreter": "python3.9",
                    "python.linting.enabled": True,
                    "python.linting.pylintEnabled": True,
                    "python.formatting.provider": "black",
                    "python.analysis.typeCheckingMode": "basic"
                }
            }
            
            # Write project configuration
            project_file = self.base_path / '.idea' / 'project_config.json'
            project_file.parent.mkdir(exist_ok=True)
            with open(project_file, 'w') as f:
                json.dump(project_config, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up PyCharm: {e}")
            return False
    
    def _setup_vscode(self, config: Dict[str, Any]) -> bool:
        """Setup Visual Studio Code"""
        try:
            # Create VS Code workspace configuration
            workspace_config = {
                "folders": [
                    {
                        "path": config['workspace_path'],
                        "name": "GenX-FX Trading System"
                    }
                ],
                "settings": {
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
                        "**/node_modules": True
                    }
                },
                "extensions": {
                    "recommendations": config['extensions']
                }
            }
            
            # Write workspace file
            workspace_file = self.base_path / 'GenX-FX.code-workspace'
            with open(workspace_file, 'w') as f:
                json.dump(workspace_config, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up VS Code: {e}")
            return False
    
    def collect_all_secrets(self) -> Dict[str, Any]:
        """Collect secrets from all configured locations"""
        self.logger.info("Collecting secrets from all locations...")
        
        collected_secrets = {}
        
        for location_name, location_path in self.secret_locations.items():
            if os.path.exists(location_path):
                self.logger.info(f"Scanning {location_name}: {location_path}")
                secrets = self._scan_location_for_secrets(location_path)
                if secrets:
                    collected_secrets[location_name] = secrets
            else:
                self.logger.warning(f"Location not found: {location_path}")
        
        return collected_secrets
    
    def _scan_location_for_secrets(self, path: str) -> Dict[str, Any]:
        """Scan location for secret files"""
        secrets = {}
        path_obj = Path(path)
        
        # Secret file patterns
        secret_patterns = [
            '*.env',
            '*.key',
            '*.pem',
            '*.p12',
            '*.pfx',
            'secrets*',
            'credentials*',
            'config*',
            '*.json',
            '*.yaml',
            '*.yml',
            '*.txt'
        ]
        
        try:
            for pattern in secret_patterns:
                for file_path in path_obj.rglob(pattern):
                    if file_path.is_file() and file_path.stat().st_size < 10 * 1024 * 1024:  # 10MB limit
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                secrets[str(file_path)] = {
                                    'content': content,
                                    'size': file_path.stat().st_size,
                                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                                }
                        except Exception as e:
                            self.logger.warning(f"Could not read {file_path}: {e}")
        except Exception as e:
            self.logger.error(f"Error scanning {path}: {e}")
        
        return secrets
    
    def create_consolidated_env_file(self, collected_secrets: Dict[str, Any]) -> None:
        """Create consolidated environment file"""
        env_file_path = self.base_path / 'config' / 'secrets.env'
        env_file_path.parent.mkdir(exist_ok=True)
        
        env_content = []
        env_content.append("# GenX-FX Consolidated Secrets")
        env_content.append(f"# Generated: {datetime.now().isoformat()}")
        env_content.append("")
        
        # Process collected secrets
        for location, secrets in collected_secrets.items():
            if secrets:
                env_content.append(f"# Secrets from {location}")
                for file_path, file_info in secrets.items():
                    content = file_info['content']
                    # Extract environment variables
                    env_vars = self._extract_env_vars(content)
                    for key, value in env_vars.items():
                        env_content.append(f"{key}={value}")
                env_content.append("")
        
        # Write consolidated environment file
        with open(env_file_path, 'w') as f:
            f.write('\n'.join(env_content))
        
        self.logger.info(f"Consolidated environment file created: {env_file_path}")
    
    def _extract_env_vars(self, content: str) -> Dict[str, str]:
        """Extract environment variables from content"""
        env_vars = {}
        
        try:
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        except Exception as e:
            self.logger.warning(f"Error extracting env vars: {e}")
        
        return env_vars
    
    def create_development_notebook(self) -> None:
        """Create comprehensive development notebook"""
        notebook_path = self.base_path / 'notebooks' / 'Development_Environment.ipynb'
        notebook_path.parent.mkdir(exist_ok=True)
        
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# GenX-FX Development Environment\n",
                        "\n",
                        "## 🛠️ Complete Development Setup\n",
                        "\n",
                        "This notebook contains all the configuration and setup for the GenX-FX development environment."
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# Import required libraries\n",
                        "import os\n",
                        "import sys\n",
                        "import json\n",
                        "import yaml\n",
                        "from pathlib import Path\n",
                        "from datetime import datetime\n",
                        "import logging\n",
                        "\n",
                        "# Set up logging\n",
                        "logging.basicConfig(level=logging.INFO)\n",
                        "logger = logging.getLogger(__name__)\n",
                        "\n",
                        "print(\"Development environment setup complete\")"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.9.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        with open(notebook_path, 'w') as f:
            json.dump(notebook_content, f, indent=2)
        
        self.logger.info(f"Development notebook created: {notebook_path}")
    
    def generate_setup_report(self, results: Dict[str, bool], collected_secrets: Dict[str, Any]) -> None:
        """Generate comprehensive setup report"""
        report_path = self.base_path / 'reports' / 'development_setup_report.md'
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("# GenX-FX Development Environment Setup Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            
            # Environment setup results
            f.write("## Development Environment Setup\n\n")
            for env_name, success in results.items():
                status = "✅ Success" if success else "❌ Failed"
                f.write(f"- **{env_name.title()}**: {status}\n")
            
            f.write("\n## Secrets Collection\n\n")
            f.write(f"- **Total Locations Scanned**: {len(collected_secrets)}\n")
            f.write(f"- **Total Files Found**: {sum(len(secrets) for secrets in collected_secrets.values())}\n")
            
            # Detailed secrets inventory
            for location, secrets in collected_secrets.items():
                if secrets:
                    f.write(f"\n### {location.title()}\n\n")
                    for file_path, file_info in secrets.items():
                        f.write(f"- **File**: {Path(file_path).name}\n")
                        f.write(f"  - **Size**: {file_info['size']} bytes\n")
                        f.write(f"  - **Modified**: {file_info['modified']}\n")
            
            # Next steps
            f.write("\n## Next Steps\n\n")
            f.write("1. **Review Secrets**: Check the consolidated secrets.env file\n")
            f.write("2. **Update Credentials**: Fill in missing API keys and passwords\n")
            f.write("3. **Test Connections**: Verify all external service connections\n")
            f.write("4. **Run System**: Start the GenX-FX trading system\n")
            f.write("5. **Monitor Performance**: Watch the system dashboard\n")
        
        self.logger.info(f"Setup report generated: {report_path}")


def main():
    """Main function to run development environment setup"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize setup
    setup = DevelopmentEnvironmentSetup()
    
    # Setup all development environments
    print("Setting up development environments...")
    results = setup.setup_all_environments()
    
    # Collect all secrets
    print("Collecting secrets from all locations...")
    collected_secrets = setup.collect_all_secrets()
    
    # Create consolidated environment file
    print("Creating consolidated environment file...")
    setup.create_consolidated_env_file(collected_secrets)
    
    # Create development notebook
    print("Creating development notebook...")
    setup.create_development_notebook()
    
    # Generate setup report
    print("Generating setup report...")
    setup.generate_setup_report(results, collected_secrets)
    
    print("\n" + "="*50)
    print("DEVELOPMENT ENVIRONMENT SETUP COMPLETE")
    print("="*50)
    print(f"Environments setup: {sum(results.values())}/{len(results)}")
    print(f"Secrets collected from: {len(collected_secrets)} locations")
    print(f"Total secret files: {sum(len(secrets) for secrets in collected_secrets.values())}")
    print("\nNext steps:")
    print("1. Review config/secrets.env file")
    print("2. Update missing credentials")
    print("3. Test system connections")
    print("4. Run: python main.py")


if __name__ == "__main__":
    main()
