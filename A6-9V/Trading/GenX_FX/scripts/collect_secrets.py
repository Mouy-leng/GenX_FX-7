#!/usr/bin/env python3
"""
GenX-FX Secrets Collection Script
Automatically collects and organizes secrets from various sources
"""

import os
import json
import yaml
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import base64
import hashlib

class SecretsCollector:
    """
    Comprehensive secrets collection and management system
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.logger = logging.getLogger(__name__)
        
        # Define secret locations
        self.secret_locations = {
            'google_drive_g': 'G:/',
            'google_drive_h': 'H:/',
            'dropbox': 'C:/Users/lengk/Dropbox/',
            'onedrive': 'C:/Users/lengk/OneDrive/',
            'local_desktop': 'C:/Users/lengk/Desktop/',
            'documents': 'C:/Users/lengk/Documents/',
            'downloads': 'C:/Users/lengk/Downloads/'
        }
        
        # Secret file patterns
        self.secret_patterns = [
            '*.env',
            '*.key',
            '*.pem',
            '*.p12',
            '*.pfx',
            '*.jks',
            '*.keystore',
            'secrets*',
            'credentials*',
            'config*',
            '*.json',
            '*.yaml',
            '*.yml',
            '*.txt',
            '*.csv'
        ]
        
        # Collected secrets
        self.collected_secrets = {}
        self.secret_inventory = {}
        
    def collect_all_secrets(self) -> Dict[str, Any]:
        """Collect secrets from all configured locations"""
        self.logger.info("Starting comprehensive secrets collection...")
        
        try:
            # Collect from each location
            for location_name, location_path in self.secret_locations.items():
                if os.path.exists(location_path):
                    self.logger.info(f"Scanning {location_name}: {location_path}")
                    secrets = self._scan_location(location_path)
                    if secrets:
                        self.collected_secrets[location_name] = secrets
                else:
                    self.logger.warning(f"Location not found: {location_path}")
            
            # Process and organize secrets
            self._process_secrets()
            
            # Generate reports
            self._generate_reports()
            
            self.logger.info("Secrets collection completed successfully")
            return self.collected_secrets
            
        except Exception as e:
            self.logger.error(f"Error collecting secrets: {e}")
            return {}
    
    def _scan_location(self, path: str) -> Dict[str, Any]:
        """Scan a specific location for secrets"""
        secrets = {}
        path_obj = Path(path)
        
        try:
            # Search for secret files
            for pattern in self.secret_patterns:
                for file_path in path_obj.rglob(pattern):
                    if file_path.is_file():
                        try:
                            # Read file content
                            content = self._read_file_safely(file_path)
                            if content:
                                secrets[str(file_path)] = {
                                    'content': content,
                                    'size': file_path.stat().st_size,
                                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                                    'type': self._detect_file_type(file_path)
                                }
                        except Exception as e:
                            self.logger.warning(f"Could not read {file_path}: {e}")
            
            return secrets
            
        except Exception as e:
            self.logger.error(f"Error scanning {path}: {e}")
            return {}
    
    def _read_file_safely(self, file_path: Path) -> Optional[str]:
        """Safely read file content"""
        try:
            # Check file size (skip large files)
            if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB limit
                return None
            
            # Read file based on extension
            if file_path.suffix.lower() in ['.json', '.yaml', '.yml', '.txt', '.env']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            else:
                # For binary files, encode as base64
                with open(file_path, 'rb') as f:
                    content = f.read()
                    return base64.b64encode(content).decode('utf-8')
                    
        except Exception as e:
            self.logger.warning(f"Could not read {file_path}: {e}")
            return None
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detect the type of secret file"""
        name = file_path.name.lower()
        
        if 'api' in name or 'key' in name:
            return 'api_key'
        elif 'secret' in name or 'password' in name:
            return 'secret'
        elif 'config' in name:
            return 'config'
        elif 'credential' in name:
            return 'credentials'
        elif file_path.suffix in ['.pem', '.key', '.p12', '.pfx']:
            return 'certificate'
        else:
            return 'unknown'
    
    def _process_secrets(self) -> None:
        """Process and organize collected secrets"""
        self.logger.info("Processing collected secrets...")
        
        # Categorize secrets
        categories = {
            'api_keys': [],
            'secrets': [],
            'certificates': [],
            'configs': [],
            'credentials': []
        }
        
        for location, secrets in self.collected_secrets.items():
            for file_path, file_info in secrets.items():
                file_type = file_info['type']
                if file_type in categories:
                    categories[file_type].append({
                        'location': location,
                        'path': file_path,
                        'info': file_info
                    })
        
        self.secret_inventory = categories
    
    def _generate_reports(self) -> None:
        """Generate comprehensive reports"""
        # Generate JSON report
        self._generate_json_report()
        
        # Generate YAML report
        self._generate_yaml_report()
        
        # Generate environment file
        self._generate_env_file()
        
        # Generate inventory report
        self._generate_inventory_report()
    
    def _generate_json_report(self) -> None:
        """Generate JSON report of all secrets"""
        report_path = self.base_path / 'reports' / 'secrets_report.json'
        report_path.parent.mkdir(exist_ok=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_locations': len(self.collected_secrets),
            'total_files': sum(len(secrets) for secrets in self.collected_secrets.values()),
            'inventory': self.secret_inventory,
            'locations': list(self.collected_secrets.keys())
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"JSON report generated: {report_path}")
    
    def _generate_yaml_report(self) -> None:
        """Generate YAML report of all secrets"""
        report_path = self.base_path / 'reports' / 'secrets_report.yaml'
        report_path.parent.mkdir(exist_ok=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_locations': len(self.collected_secrets),
            'total_files': sum(len(secrets) for secrets in self.collected_secrets.values()),
            'inventory': self.secret_inventory,
            'locations': list(self.collected_secrets.keys())
        }
        
        with open(report_path, 'w') as f:
            yaml.dump(report, f, default_flow_style=False)
        
        self.logger.info(f"YAML report generated: {report_path}")
    
    def _generate_env_file(self) -> None:
        """Generate consolidated environment file"""
        env_path = self.base_path / 'config' / 'secrets.env'
        env_path.parent.mkdir(exist_ok=True)
        
        env_content = []
        env_content.append("# GenX-FX Consolidated Secrets")
        env_content.append(f"# Generated: {datetime.now().isoformat()}")
        env_content.append("")
        
        # Process each category
        for category, items in self.secret_inventory.items():
            if items:
                env_content.append(f"# {category.upper()}")
                for item in items:
                    file_path = item['path']
                    content = item['info']['content']
                    
                    # Extract environment variables
                    if item['info']['type'] in ['config', 'credentials']:
                        env_vars = self._extract_env_vars(content)
                        for key, value in env_vars.items():
                            env_content.append(f"{key}={value}")
                
                env_content.append("")
        
        with open(env_path, 'w') as f:
            f.write('\n'.join(env_content))
        
        self.logger.info(f"Environment file generated: {env_path}")
    
    def _extract_env_vars(self, content: str) -> Dict[str, str]:
        """Extract environment variables from content"""
        env_vars = {}
        
        try:
            # Parse .env format
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        except Exception as e:
            self.logger.warning(f"Error extracting env vars: {e}")
        
        return env_vars
    
    def _generate_inventory_report(self) -> None:
        """Generate detailed inventory report"""
        report_path = self.base_path / 'reports' / 'secrets_inventory.md'
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("# GenX-FX Secrets Inventory Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            
            # Summary
            f.write("## Summary\n\n")
            f.write(f"- **Total Locations Scanned:** {len(self.collected_secrets)}\n")
            f.write(f"- **Total Files Found:** {sum(len(secrets) for secrets in self.collected_secrets.values())}\n")
            f.write(f"- **Categories:** {', '.join(self.secret_inventory.keys())}\n\n")
            
            # Detailed inventory
            for category, items in self.secret_inventory.items():
                if items:
                    f.write(f"## {category.upper()}\n\n")
                    for item in items:
                        f.write(f"### {Path(item['path']).name}\n")
                        f.write(f"- **Location:** {item['location']}\n")
                        f.write(f"- **Path:** {item['path']}\n")
                        f.write(f"- **Type:** {item['info']['type']}\n")
                        f.write(f"- **Size:** {item['info']['size']} bytes\n")
                        f.write(f"- **Modified:** {item['info']['modified']}\n\n")
            
            # Security recommendations
            f.write("## Security Recommendations\n\n")
            f.write("1. **Rotate Secrets:** Regularly rotate all API keys and passwords\n")
            f.write("2. **Access Control:** Limit access to secret files\n")
            f.write("3. **Encryption:** Encrypt sensitive data at rest\n")
            f.write("4. **Monitoring:** Monitor for unauthorized access\n")
            f.write("5. **Backup:** Secure backup of critical secrets\n\n")
        
        self.logger.info(f"Inventory report generated: {report_path}")
    
    def create_secure_backup(self) -> None:
        """Create encrypted backup of all secrets"""
        backup_path = self.base_path / 'backups' / f'secrets_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        backup_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Copy all secret files to backup
            for location, secrets in self.collected_secrets.items():
                location_backup = backup_path / location
                location_backup.mkdir(exist_ok=True)
                
                for file_path, file_info in secrets.items():
                    source_path = Path(file_path)
                    if source_path.exists():
                        dest_path = location_backup / source_path.name
                        shutil.copy2(source_path, dest_path)
            
            # Create manifest
            manifest = {
                'timestamp': datetime.now().isoformat(),
                'total_files': sum(len(secrets) for secrets in self.collected_secrets.values()),
                'locations': list(self.collected_secrets.keys())
            }
            
            with open(backup_path / 'manifest.json', 'w') as f:
                json.dump(manifest, f, indent=2)
            
            self.logger.info(f"Secure backup created: {backup_path}")
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")


def main():
    """Main function to run secrets collection"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize collector
    collector = SecretsCollector()
    
    # Collect all secrets
    secrets = collector.collect_all_secrets()
    
    # Create secure backup
    collector.create_secure_backup()
    
    print(f"Secrets collection completed. Found {len(secrets)} locations with secrets.")
    print("Reports generated in 'reports/' directory")
    print("Environment file generated in 'config/secrets.env'")


if __name__ == "__main__":
    main()
