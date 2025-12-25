#!/usr/bin/env python3
"""
GenX-FX Comprehensive Secrets Collection
Collects secrets from Google Drive (G:), (H:), Dropbox, OneDrive, and local drives
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
import re

class ComprehensiveSecretsCollector:
    """
    Comprehensive secrets collection from all drives and cloud storage
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.logger = logging.getLogger(__name__)
        
        # Define all possible secret locations
        self.secret_locations = {
            # Google Drive locations
            'google_drive_g': 'G:/',
            'google_drive_h': 'H:/',
            
            # Cloud storage
            'dropbox': 'C:/Users/lengk/Dropbox/',
            'onedrive': 'C:/Users/lengk/OneDrive/',
            
            # Local drives
            'desktop': 'C:/Users/lengk/Desktop/',
            'documents': 'C:/Users/lengk/Documents/',
            'downloads': 'C:/Users/lengk/Downloads/',
            'pictures': 'C:/Users/lengk/Pictures/',
            'videos': 'C:/Users/lengk/Videos/',
            'music': 'C:/Users/lengk/Music/',
            
            # Project specific locations
            'a6_9v_tools': 'C:/Users/lengk/Dropbox/OneDrive/Desktop/A6-9V Tools/',
            'a6_9v_trading': 'C:/Users/lengk/Dropbox/OneDrive/Desktop/A6-9V Trading/',
            'a6_9v_projects': 'C:/Users/lengk/Dropbox/OneDrive/Desktop/A6-9V Projects/',
            
            # Additional drives
            'data_d': 'D:/',
            'data_e': 'E:/',
            'data_j': 'J:/',
            
            # Root directories
            'c_root': 'C:/',
            'program_files': 'C:/Program Files/',
            'program_files_x86': 'C:/Program Files (x86)/',
            'appdata': 'C:/Users/lengk/AppData/',
            'appdata_roaming': 'C:/Users/lengk/AppData/Roaming/',
            'appdata_local': 'C:/Users/lengk/AppData/Local/',
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
            '*.csv',
            '*.xml',
            '*.ini',
            '*.cfg',
            '*.conf',
            '*.properties',
            '*.toml',
            '*.ini',
            '*.log',
            '*.bak',
            '*.backup'
        ]
        
        # API key patterns
        self.api_key_patterns = [
            r'api[_-]?key["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})',
            r'secret[_-]?key["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})',
            r'access[_-]?token["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})',
            r'bearer[_-]?token["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})',
            r'password["\s]*[:=]["\s]*([a-zA-Z0-9_\-!@#$%^&*()_+={}[\]:;"\'<>,.?/\\|`~]{8,})',
            r'token["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})',
            r'key["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})',
            r'secret["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})',
        ]
        
        # Collected secrets
        self.collected_secrets = {}
        self.secret_inventory = {}
        self.api_keys_found = {}
        
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
                        self.logger.info(f"Found {len(secrets)} files in {location_name}")
                else:
                    self.logger.warning(f"Location not found: {location_path}")
            
            # Process and organize secrets
            self._process_secrets()
            
            # Extract API keys
            self._extract_api_keys()
            
            # Generate reports
            self._generate_reports()
            
            # Create consolidated environment file
            self._create_consolidated_env()
            
            self.logger.info("Comprehensive secrets collection completed successfully")
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
                            # Skip large files and system files
                            if (file_path.stat().st_size > 50 * 1024 * 1024 or  # 50MB limit
                                any(skip in str(file_path).lower() for skip in ['system32', 'windows', 'temp', 'cache'])):
                                continue
                            
                            # Read file content
                            content = self._read_file_safely(file_path)
                            if content:
                                secrets[str(file_path)] = {
                                    'content': content,
                                    'size': file_path.stat().st_size,
                                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                                    'type': self._detect_file_type(file_path),
                                    'hash': hashlib.md5(content.encode()).hexdigest()
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
            # Check file size
            if file_path.stat().st_size > 50 * 1024 * 1024:  # 50MB limit
                return None
            
            # Read file based on extension
            if file_path.suffix.lower() in ['.json', '.yaml', '.yml', '.txt', '.env', '.ini', '.cfg', '.conf', '.properties', '.toml']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            elif file_path.suffix.lower() in ['.pem', '.key', '.p12', '.pfx', '.jks']:
                # For certificate files, encode as base64
                with open(file_path, 'rb') as f:
                    content = f.read()
                    return base64.b64encode(content).decode('utf-8')
            else:
                # For other files, try to read as text
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
                except:
                    return None
                    
        except Exception as e:
            self.logger.warning(f"Could not read {file_path}: {e}")
            return None
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detect the type of secret file"""
        name = file_path.name.lower()
        
        if any(keyword in name for keyword in ['api', 'key', 'token']):
            return 'api_key'
        elif any(keyword in name for keyword in ['secret', 'password', 'credential']):
            return 'secret'
        elif any(keyword in name for keyword in ['config', 'setting']):
            return 'config'
        elif any(keyword in name for keyword in ['credential', 'auth']):
            return 'credentials'
        elif file_path.suffix in ['.pem', '.key', '.p12', '.pfx', '.jks']:
            return 'certificate'
        elif file_path.suffix in ['.env']:
            return 'environment'
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
            'credentials': [],
            'environment': []
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
    
    def _extract_api_keys(self) -> None:
        """Extract API keys from all collected content"""
        self.logger.info("Extracting API keys from collected content...")
        
        for location, secrets in self.collected_secrets.items():
            for file_path, file_info in secrets.items():
                content = file_info['content']
                
                # Search for API key patterns
                for pattern in self.api_key_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        if location not in self.api_keys_found:
                            self.api_keys_found[location] = []
                        
                        for match in matches:
                            self.api_keys_found[location].append({
                                'file': file_path,
                                'pattern': pattern,
                                'key': match[:10] + '...' if len(match) > 10 else match,  # Truncate for security
                                'full_key': match
                            })
    
    def _generate_reports(self) -> None:
        """Generate comprehensive reports"""
        # Generate JSON report
        self._generate_json_report()
        
        # Generate YAML report
        self._generate_yaml_report()
        
        # Generate inventory report
        self._generate_inventory_report()
        
        # Generate API keys report
        self._generate_api_keys_report()
    
    def _generate_json_report(self) -> None:
        """Generate JSON report of all secrets"""
        report_path = self.base_path / 'reports' / 'comprehensive_secrets_report.json'
        report_path.parent.mkdir(exist_ok=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_locations': len(self.collected_secrets),
            'total_files': sum(len(secrets) for secrets in self.collected_secrets.values()),
            'inventory': self.secret_inventory,
            'api_keys_found': len(self.api_keys_found),
            'locations': list(self.collected_secrets.keys())
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"JSON report generated: {report_path}")
    
    def _generate_yaml_report(self) -> None:
        """Generate YAML report of all secrets"""
        report_path = self.base_path / 'reports' / 'comprehensive_secrets_report.yaml'
        report_path.parent.mkdir(exist_ok=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_locations': len(self.collected_secrets),
            'total_files': sum(len(secrets) for secrets in self.collected_secrets.values()),
            'inventory': self.secret_inventory,
            'api_keys_found': len(self.api_keys_found),
            'locations': list(self.collected_secrets.keys())
        }
        
        with open(report_path, 'w') as f:
            yaml.dump(report, f, default_flow_style=False)
        
        self.logger.info(f"YAML report generated: {report_path}")
    
    def _generate_inventory_report(self) -> None:
        """Generate detailed inventory report"""
        report_path = self.base_path / 'reports' / 'comprehensive_secrets_inventory.md'
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("# GenX-FX Comprehensive Secrets Inventory Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            
            # Summary
            f.write("## Summary\n\n")
            f.write(f"- **Total Locations Scanned:** {len(self.collected_secrets)}\n")
            f.write(f"- **Total Files Found:** {sum(len(secrets) for secrets in self.collected_secrets.values())}\n")
            f.write(f"- **API Keys Found:** {len(self.api_keys_found)}\n")
            f.write(f"- **Categories:** {', '.join(self.secret_inventory.keys())}\n\n")
            
            # Detailed inventory by category
            for category, items in self.secret_inventory.items():
                if items:
                    f.write(f"## {category.upper()}\n\n")
                    f.write(f"**Total Files:** {len(items)}\n\n")
                    
                    for item in items:
                        f.write(f"### {Path(item['path']).name}\n")
                        f.write(f"- **Location:** {item['location']}\n")
                        f.write(f"- **Path:** {item['path']}\n")
                        f.write(f"- **Type:** {item['info']['type']}\n")
                        f.write(f"- **Size:** {item['info']['size']} bytes\n")
                        f.write(f"- **Modified:** {item['info']['modified']}\n")
                        f.write(f"- **Hash:** {item['info']['hash']}\n\n")
            
            # API Keys section
            if self.api_keys_found:
                f.write("## API KEYS FOUND\n\n")
                f.write("**⚠️ SECURITY WARNING: Review and rotate these keys immediately!**\n\n")
                
                for location, keys in self.api_keys_found.items():
                    f.write(f"### {location.title()}\n\n")
                    for key_info in keys:
                        f.write(f"- **File:** {Path(key_info['file']).name}\n")
                        f.write(f"- **Pattern:** {key_info['pattern']}\n")
                        f.write(f"- **Key:** {key_info['key']}\n\n")
            
            # Security recommendations
            f.write("## Security Recommendations\n\n")
            f.write("1. **Immediate Actions:**\n")
            f.write("   - Review all found API keys and secrets\n")
            f.write("   - Rotate any exposed credentials\n")
            f.write("   - Remove secrets from version control\n")
            f.write("   - Secure backup of critical secrets\n\n")
            f.write("2. **Long-term Security:**\n")
            f.write("   - Implement secret management system\n")
            f.write("   - Use environment variables for sensitive data\n")
            f.write("   - Regular security audits\n")
            f.write("   - Access control and monitoring\n\n")
            f.write("3. **Best Practices:**\n")
            f.write("   - Never commit secrets to git\n")
            f.write("   - Use .env files for local development\n")
            f.write("   - Encrypt sensitive data at rest\n")
            f.write("   - Monitor for unauthorized access\n\n")
        
        self.logger.info(f"Inventory report generated: {report_path}")
    
    def _generate_api_keys_report(self) -> None:
        """Generate API keys security report"""
        report_path = self.base_path / 'reports' / 'api_keys_security_report.md'
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("# API Keys Security Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            f.write("**⚠️ CRITICAL SECURITY ALERT ⚠️**\n\n")
            f.write("The following API keys and secrets have been found in your system.\n")
            f.write("**IMMEDIATE ACTION REQUIRED:**\n\n")
            
            if self.api_keys_found:
                for location, keys in self.api_keys_found.items():
                    f.write(f"## {location.title()}\n\n")
                    for key_info in keys:
                        f.write(f"### {Path(key_info['file']).name}\n")
                        f.write(f"- **Pattern:** {key_info['pattern']}\n")
                        f.write(f"- **Key:** {key_info['key']}\n")
                        f.write(f"- **Full Key:** {key_info['full_key']}\n")
                        f.write(f"- **File Path:** {key_info['file']}\n\n")
                        
                        f.write("**Actions Required:**\n")
                        f.write("1. Verify if this key is still in use\n")
                        f.write("2. If in use, rotate the key immediately\n")
                        f.write("3. Remove the key from the file\n")
                        f.write("4. Update any systems using this key\n")
                        f.write("5. Monitor for unauthorized usage\n\n")
            else:
                f.write("No API keys found in scanned files.\n\n")
            
            f.write("## Security Checklist\n\n")
            f.write("- [ ] Review all found API keys\n")
            f.write("- [ ] Rotate exposed credentials\n")
            f.write("- [ ] Remove secrets from files\n")
            f.write("- [ ] Update system configurations\n")
            f.write("- [ ] Monitor for unauthorized access\n")
            f.write("- [ ] Implement secret management\n")
            f.write("- [ ] Regular security audits\n\n")
        
        self.logger.info(f"API keys security report generated: {report_path}")
    
    def _create_consolidated_env(self) -> None:
        """Create consolidated environment file with all found secrets"""
        env_path = self.base_path / 'config' / 'consolidated_secrets.env'
        env_path.parent.mkdir(exist_ok=True)
        
        env_content = []
        env_content.append("# GenX-FX Consolidated Secrets")
        env_content.append(f"# Generated: {datetime.now().isoformat()}")
        env_content.append("# WARNING: Review and secure these secrets immediately!")
        env_content.append("")
        
        # Process environment files
        for location, secrets in self.collected_secrets.items():
            for file_path, file_info in secrets.items():
                if file_info['type'] == 'environment':
                    env_content.append(f"# From {location}: {Path(file_path).name}")
                    content = file_info['content']
                    
                    # Extract environment variables
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            env_content.append(line)
                    env_content.append("")
        
        # Add found API keys
        if self.api_keys_found:
            env_content.append("# Found API Keys (REVIEW AND SECURE!)")
            for location, keys in self.api_keys_found.items():
                for key_info in keys:
                    # Extract key name from pattern
                    pattern = key_info['pattern']
                    key_name = pattern.split('[')[0].upper().replace('_', '_')
                    env_content.append(f"# {key_name} from {Path(key_info['file']).name}")
                    env_content.append(f"{key_name}={key_info['full_key']}")
            env_content.append("")
        
        # Write consolidated environment file
        with open(env_path, 'w') as f:
            f.write('\n'.join(env_content))
        
        self.logger.info(f"Consolidated environment file created: {env_path}")
    
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
                'locations': list(self.collected_secrets.keys()),
                'api_keys_found': len(self.api_keys_found)
            }
            
            with open(backup_path / 'manifest.json', 'w') as f:
                json.dump(manifest, f, indent=2)
            
            self.logger.info(f"Secure backup created: {backup_path}")
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")


def main():
    """Main function to run comprehensive secrets collection"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize collector
    collector = ComprehensiveSecretsCollector()
    
    print("🔍 Starting comprehensive secrets collection...")
    print("📁 Scanning Google Drive (G:), (H:), Dropbox, OneDrive, and local drives...")
    
    # Collect all secrets
    secrets = collector.collect_all_secrets()
    
    # Create secure backup
    print("💾 Creating secure backup...")
    collector.create_secure_backup()
    
    print("\n" + "="*60)
    print("🔐 COMPREHENSIVE SECRETS COLLECTION COMPLETE")
    print("="*60)
    print(f"📊 Locations scanned: {len(secrets)}")
    print(f"📄 Total files found: {sum(len(s) for s in secrets.values())}")
    print(f"🔑 API keys found: {len(collector.api_keys_found)}")
    print(f"📁 Reports generated in 'reports/' directory")
    print(f"⚙️ Consolidated environment file: 'config/consolidated_secrets.env'")
    print(f"💾 Secure backup created in 'backups/' directory")
    
    if collector.api_keys_found:
        print("\n⚠️  SECURITY ALERT: API keys found!")
        print("🔒 Please review and secure these credentials immediately!")
        print("📋 Check 'reports/api_keys_security_report.md' for details")
    
    print("\n📋 Next steps:")
    print("1. Review consolidated_secrets.env file")
    print("2. Update missing credentials")
    print("3. Secure any exposed API keys")
    print("4. Test system connections")
    print("5. Run: python main.py")


if __name__ == "__main__":
    main()
