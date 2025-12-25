#!/usr/bin/env python3
"""
A6-9V Autonomous Credential Collection System
Continuously monitors, collects, and organizes credentials with AI-powered analysis
"""

import os
import json
import yaml
import time
import shutil
import asyncio
import logging
import hashlib
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict
import re
import base64
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

@dataclass
class CredentialFile:
    """Represents a discovered credential file"""
    path: str
    content_hash: str
    file_type: str
    confidence_score: float
    last_modified: datetime
    size: int
    location: str
    sensitive_data: List[Dict[str, Any]]
    risk_level: str
    status: str = "discovered"
    
@dataclass
class SecretPattern:
    """Represents a secret detection pattern"""
    name: str
    pattern: str
    description: str
    confidence: float
    risk_level: str

class CredentialDatabase:
    """SQLite database for credential tracking"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the credential tracking database"""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE,
                    content_hash TEXT,
                    file_type TEXT,
                    confidence_score REAL,
                    last_modified TIMESTAMP,
                    size INTEGER,
                    location TEXT,
                    risk_level TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sensitive_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    credential_id INTEGER,
                    pattern_name TEXT,
                    matched_value TEXT,
                    confidence REAL,
                    risk_level TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (credential_id) REFERENCES credentials (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS collection_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    files_scanned INTEGER,
                    credentials_found INTEGER,
                    high_risk_found INTEGER,
                    status TEXT,
                    notes TEXT
                )
            ''')
            
            conn.commit()
        finally:
            conn.close()
    
    def insert_credential(self, credential: CredentialFile) -> int:
        """Insert or update a credential file record"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO credentials 
                (path, content_hash, file_type, confidence_score, last_modified, 
                 size, location, risk_level, status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                credential.path,
                credential.content_hash,
                credential.file_type,
                credential.confidence_score,
                credential.last_modified,
                credential.size,
                credential.location,
                credential.risk_level,
                credential.status
            ))
            
            credential_id = cursor.lastrowid
            
            # Insert sensitive data
            for sensitive in credential.sensitive_data:
                cursor.execute('''
                    INSERT INTO sensitive_data 
                    (credential_id, pattern_name, matched_value, confidence, risk_level)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    credential_id,
                    sensitive.get('pattern_name', ''),
                    sensitive.get('value', '')[:50],  # Truncate for security
                    sensitive.get('confidence', 0.0),
                    sensitive.get('risk_level', 'medium')
                ))
            
            conn.commit()
            return credential_id
        finally:
            conn.close()

class AutonomousCredentialCollector:
    """
    Advanced autonomous credential collection and monitoring system
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.logger = self._setup_logging()
        self.db = CredentialDatabase(self.base_path / "data" / "credentials.db")
        
        # Monitoring configuration
        self.is_running = False
        self.scheduler = BackgroundScheduler()
        self.file_observer = Observer()
        self.watched_paths: Set[str] = set()
        
        # Enhanced secret locations with priority levels
        self.secret_locations = {
            # High priority - Cloud storage and project directories
            'dropbox_desktop': {
                'path': 'C:/Users/lengk/Dropbox/OneDrive/Desktop/',
                'priority': 'high',
                'recursive': True,
                'watch': True
            },
            'onedrive': {
                'path': 'C:/Users/lengk/OneDrive/',
                'priority': 'high',
                'recursive': True,
                'watch': True
            },
            'a6_9v_projects': {
                'path': 'C:/Users/lengk/Dropbox/OneDrive/Desktop/A6-9V/',
                'priority': 'critical',
                'recursive': True,
                'watch': True
            },
            # Medium priority - Google Drive
            'google_drive_g': {
                'path': 'G:/',
                'priority': 'medium',
                'recursive': True,
                'watch': False  # May not be always mounted
            },
            'google_drive_h': {
                'path': 'H:/',
                'priority': 'medium', 
                'recursive': True,
                'watch': False
            },
            # Low priority - System directories
            'documents': {
                'path': 'C:/Users/lengk/Documents/',
                'priority': 'low',
                'recursive': False,
                'watch': False
            },
            'downloads': {
                'path': 'C:/Users/lengk/Downloads/',
                'priority': 'low',
                'recursive': False,
                'watch': False
            },
            # Data drives
            'data_drives': {
                'path': ['D:/', 'E:/', 'J:/'],
                'priority': 'low',
                'recursive': True,
                'watch': False
            }
        }
        
        # Enhanced secret patterns with ML-style confidence scoring
        self.secret_patterns = [
            SecretPattern("api_key", r'(?i)api[_-]?key["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})', "API Key", 0.9, "high"),
            SecretPattern("secret_key", r'(?i)secret[_-]?key["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})', "Secret Key", 0.9, "high"),
            SecretPattern("access_token", r'(?i)access[_-]?token["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})', "Access Token", 0.85, "high"),
            SecretPattern("bearer_token", r'(?i)bearer[_-]?token["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{20,})', "Bearer Token", 0.85, "high"),
            SecretPattern("password", r'(?i)password["\s]*[:=]["\s]*([a-zA-Z0-9_\-!@#$%^&*()_+={}[\]:;"\'<>,.?/\\|`~]{8,})', "Password", 0.8, "high"),
            SecretPattern("private_key", r'-----BEGIN [A-Z ]+PRIVATE KEY-----', "Private Key", 0.95, "critical"),
            SecretPattern("aws_key", r'(?i)aws[_-]?access[_-]?key[_-]?id["\s]*[:=]["\s]*([A-Z0-9]{20})', "AWS Access Key", 0.9, "high"),
            SecretPattern("aws_secret", r'(?i)aws[_-]?secret[_-]?access[_-]?key["\s]*[:=]["\s]*([A-Za-z0-9/+=]{40})', "AWS Secret Key", 0.9, "high"),
            SecretPattern("github_token", r'(?i)gh[ps]_[A-Za-z0-9_]{36}', "GitHub Token", 0.85, "medium"),
            SecretPattern("slack_token", r'(?i)xox[baprs]-[A-Za-z0-9\-]+', "Slack Token", 0.8, "medium"),
            SecretPattern("jwt_token", r'(?i)ey[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*', "JWT Token", 0.7, "medium"),
            SecretPattern("connection_string", r'(?i)(mongodb|mysql|postgres)://[^\s]+', "Database Connection", 0.8, "high"),
            SecretPattern("email_password", r'(?i)(smtp|email)[_-]?password["\s]*[:=]["\s]*([^\s"\']{8,})', "Email Password", 0.75, "medium")
        ]
        
        # File patterns to scan
        self.file_patterns = [
            '*.env*', '*.key', '*.pem', '*.p12', '*.pfx', '*.jks', '*.keystore',
            'secrets*', 'credentials*', 'config*', '*.json', '*.yaml', '*.yml',
            '*.txt', '*.csv', '*.xml', '*.ini', '*.cfg', '*.conf', '*.properties',
            '*.toml', '*.log', '*.bak', '*.backup', '*.sql', '*.sh', '*.bat',
            '*.ps1', '*.py', '*.js', '*.ts', '*.java', '*.cs', '*.php'
        ]
        
        # Statistics
        self.stats = {
            'files_scanned': 0,
            'credentials_found': 0,
            'high_risk_found': 0,
            'last_scan': None,
            'scan_duration': 0
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        logger = logging.getLogger('AutonomousCredentialCollector')
        logger.setLevel(logging.DEBUG)
        
        # Create logs directory
        log_dir = self.base_path / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # File handler for all logs
        file_handler = logging.FileHandler(log_dir / f"credential_collector_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler for important messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    async def start_autonomous_collection(self):
        """Start the autonomous credential collection system"""
        try:
            self.logger.info("🚀 Starting Autonomous Credential Collection System")
            self.is_running = True
            
            # Initial comprehensive scan
            await self.initial_comprehensive_scan()
            
            # Setup file system monitoring
            self.setup_file_monitoring()
            
            # Schedule periodic tasks
            self.schedule_periodic_tasks()
            
            # Start background services
            self.scheduler.start()
            self.file_observer.start()
            
            self.logger.info("✅ Autonomous Credential Collection System started successfully")
            
            # Keep running
            while self.is_running:
                await asyncio.sleep(60)  # Check every minute
                await self.health_check()
                
        except Exception as e:
            self.logger.error(f"❌ Error starting autonomous collection: {e}")
            await self.shutdown()
    
    async def initial_comprehensive_scan(self):
        """Perform initial comprehensive scan of all locations"""
        self.logger.info("🔍 Starting initial comprehensive credential scan...")
        start_time = datetime.now()
        
        total_files = 0
        total_credentials = 0
        
        for location_name, config in self.secret_locations.items():
            paths = config['path'] if isinstance(config['path'], list) else [config['path']]
            
            for path in paths:
                if os.path.exists(path):
                    self.logger.info(f"📁 Scanning {location_name}: {path}")
                    files, credentials = await self.scan_location_comprehensive(path, location_name, config)
                    total_files += files
                    total_credentials += credentials
                else:
                    self.logger.warning(f"⚠️ Location not found: {path}")
        
        duration = datetime.now() - start_time
        self.stats.update({
            'files_scanned': total_files,
            'credentials_found': total_credentials,
            'last_scan': start_time,
            'scan_duration': duration.total_seconds()
        })
        
        self.logger.info(f"✅ Initial scan completed: {total_files} files scanned, {total_credentials} credentials found in {duration}")
        
        # Generate comprehensive report
        await self.generate_autonomous_report()
    
    async def scan_location_comprehensive(self, path: str, location_name: str, config: Dict) -> tuple:
        """Comprehensive scan of a specific location"""
        files_scanned = 0
        credentials_found = 0
        
        try:
            path_obj = Path(path)
            
            for pattern in self.file_patterns:
                search_path = path_obj.rglob(pattern) if config.get('recursive', True) else path_obj.glob(pattern)
                
                for file_path in search_path:
                    if file_path.is_file() and self._should_scan_file(file_path):
                        files_scanned += 1
                        
                        credential = await self.analyze_file_for_credentials(file_path, location_name)
                        if credential and credential.confidence_score > 0.5:
                            credentials_found += 1
                            self.db.insert_credential(credential)
                            
                            # Log high-risk findings immediately
                            if credential.risk_level in ['high', 'critical']:
                                self.logger.warning(f"🚨 {credential.risk_level.upper()} RISK credential found: {file_path}")
                                await self.alert_high_risk_credential(credential)
            
            return files_scanned, credentials_found
            
        except Exception as e:
            self.logger.error(f"❌ Error scanning {path}: {e}")
            return 0, 0
    
    async def analyze_file_for_credentials(self, file_path: Path, location: str) -> Optional[CredentialFile]:
        """Advanced AI-powered credential analysis of a single file"""
        try:
            # Read file content safely
            content = await self._read_file_safely(file_path)
            if not content:
                return None
            
            # Calculate content hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Analyze content for secrets
            sensitive_data = []
            total_confidence = 0.0
            max_risk_level = "low"
            
            for pattern in self.secret_patterns:
                matches = re.findall(pattern.pattern, content)
                if matches:
                    for match in matches:
                        sensitive_data.append({
                            'pattern_name': pattern.name,
                            'description': pattern.description,
                            'value': match[:20] + "..." if len(match) > 20 else match,
                            'confidence': pattern.confidence,
                            'risk_level': pattern.risk_level
                        })
                        total_confidence += pattern.confidence
                        
                        # Update max risk level
                        if pattern.risk_level == 'critical':
                            max_risk_level = 'critical'
                        elif pattern.risk_level == 'high' and max_risk_level != 'critical':
                            max_risk_level = 'high'
                        elif pattern.risk_level == 'medium' and max_risk_level == 'low':
                            max_risk_level = 'medium'
            
            # Only create credential record if sensitive data found
            if sensitive_data:
                # Calculate overall confidence score
                confidence_score = min(total_confidence / len(self.secret_patterns), 1.0)
                
                return CredentialFile(
                    path=str(file_path),
                    content_hash=content_hash,
                    file_type=self._detect_file_type(file_path),
                    confidence_score=confidence_score,
                    last_modified=datetime.fromtimestamp(file_path.stat().st_mtime),
                    size=file_path.stat().st_size,
                    location=location,
                    sensitive_data=sensitive_data,
                    risk_level=max_risk_level
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing {file_path}: {e}")
            return None
    
    def setup_file_monitoring(self):
        """Setup real-time file system monitoring"""
        class CredentialFileHandler(FileSystemEventHandler):
            def __init__(self, collector):
                self.collector = collector
            
            def on_created(self, event):
                if not event.is_directory:
                    asyncio.run(self.collector.handle_file_event(event.src_path, "created"))
            
            def on_modified(self, event):
                if not event.is_directory:
                    asyncio.run(self.collector.handle_file_event(event.src_path, "modified"))
            
            def on_moved(self, event):
                if not event.is_directory:
                    asyncio.run(self.collector.handle_file_event(event.dest_path, "moved"))
        
        handler = CredentialFileHandler(self)
        
        # Watch high-priority locations
        for location_name, config in self.secret_locations.items():
            if config.get('watch', False) and config.get('priority') in ['high', 'critical']:
                paths = config['path'] if isinstance(config['path'], list) else [config['path']]
                for path in paths:
                    if os.path.exists(path):
                        self.file_observer.schedule(handler, path, recursive=config.get('recursive', True))
                        self.watched_paths.add(path)
                        self.logger.info(f"👁️ Watching {location_name}: {path}")
    
    async def handle_file_event(self, file_path: str, event_type: str):
        """Handle file system events for potential credentials"""
        try:
            file_path_obj = Path(file_path)
            
            # Check if file matches our patterns
            if not self._should_scan_file(file_path_obj):
                return
            
            self.logger.debug(f"🔍 File {event_type}: {file_path}")
            
            # Analyze the file
            credential = await self.analyze_file_for_credentials(file_path_obj, "monitored")
            if credential and credential.confidence_score > 0.5:
                self.db.insert_credential(credential)
                self.logger.info(f"🔐 New credential detected: {file_path} (confidence: {credential.confidence_score:.2f})")
                
                if credential.risk_level in ['high', 'critical']:
                    await self.alert_high_risk_credential(credential)
                    
        except Exception as e:
            self.logger.error(f"❌ Error handling file event {file_path}: {e}")
    
    def schedule_periodic_tasks(self):
        """Schedule periodic maintenance and scanning tasks"""
        # Daily comprehensive scan
        self.scheduler.add_job(
            self.daily_comprehensive_scan,
            CronTrigger(hour=2, minute=0),  # 2 AM daily
            id='daily_scan'
        )
        
        # Hourly quick scan of high-priority locations
        self.scheduler.add_job(
            self.hourly_priority_scan,
            IntervalTrigger(hours=1),
            id='hourly_scan'
        )
        
        # Generate reports every 6 hours
        self.scheduler.add_job(
            self.generate_autonomous_report,
            IntervalTrigger(hours=6),
            id='report_generation'
        )
        
        # Cleanup old logs and backups weekly
        self.scheduler.add_job(
            self.cleanup_old_files,
            CronTrigger(day_of_week=0, hour=3, minute=0),  # Sunday 3 AM
            id='weekly_cleanup'
        )
        
        self.logger.info("📅 Periodic tasks scheduled successfully")
    
    async def daily_comprehensive_scan(self):
        """Daily comprehensive scan of all locations"""
        self.logger.info("🌅 Starting daily comprehensive scan...")
        await self.initial_comprehensive_scan()
    
    async def hourly_priority_scan(self):
        """Hourly scan of high-priority locations only"""
        self.logger.info("⏰ Starting hourly priority scan...")
        
        for location_name, config in self.secret_locations.items():
            if config.get('priority') in ['high', 'critical']:
                paths = config['path'] if isinstance(config['path'], list) else [config['path']]
                for path in paths:
                    if os.path.exists(path):
                        await self.scan_location_comprehensive(path, location_name, config)
    
    async def generate_autonomous_report(self):
        """Generate comprehensive autonomous collection report"""
        try:
            report_dir = self.base_path / "reports" / "autonomous"
            report_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now()
            report_data = {
                'system_info': {
                    'name': 'A6-9V Autonomous Credential Collector',
                    'version': '2.0.0',
                    'generated_at': timestamp.isoformat(),
                    'status': 'running' if self.is_running else 'stopped',
                    'uptime': str(timestamp - self.stats.get('last_scan', timestamp))
                },
                'statistics': self.stats,
                'locations_monitored': {
                    name: {
                        'path': config['path'],
                        'priority': config['priority'],
                        'monitored': config.get('watch', False)
                    }
                    for name, config in self.secret_locations.items()
                },
                'risk_summary': await self._get_risk_summary(),
                'recommendations': await self._generate_recommendations()
            }
            
            # Save JSON report
            with open(report_dir / f"autonomous_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            # Save latest report
            with open(report_dir / "latest_autonomous_report.json", 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            self.logger.info(f"📊 Autonomous report generated: {report_dir}")
            
        except Exception as e:
            self.logger.error(f"❌ Error generating autonomous report: {e}")
    
    async def alert_high_risk_credential(self, credential: CredentialFile):
        """Alert system for high-risk credential discovery"""
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'severity': credential.risk_level,
            'file_path': credential.path,
            'location': credential.location,
            'confidence': credential.confidence_score,
            'sensitive_patterns': [s['pattern_name'] for s in credential.sensitive_data]
        }
        
        # Save alert to file
        alert_dir = self.base_path / "alerts"
        alert_dir.mkdir(exist_ok=True)
        
        alert_file = alert_dir / f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(alert_file, 'w') as f:
            json.dump(alert_data, f, indent=2)
        
        self.logger.critical(f"🚨 HIGH RISK ALERT: {credential.risk_level.upper()} credential found at {credential.path}")
    
    async def _get_risk_summary(self) -> Dict[str, Any]:
        """Get current risk summary from database"""
        # This would query the database for risk statistics
        return {
            'critical_risk': 0,
            'high_risk': 0,
            'medium_risk': 0,
            'low_risk': 0,
            'total_credentials': 0
        }
    
    async def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = [
            "Review all high and critical risk credentials immediately",
            "Rotate any exposed API keys and secrets",
            "Implement proper secret management practices",
            "Remove credentials from tracked files",
            "Set up environment variable management",
            "Regular security audits and monitoring"
        ]
        return recommendations
    
    def _should_scan_file(self, file_path: Path) -> bool:
        """Determine if a file should be scanned"""
        # Skip large files (>50MB)
        try:
            if file_path.stat().st_size > 50 * 1024 * 1024:
                return False
        except:
            return False
        
        # Skip system and temp directories
        path_str = str(file_path).lower()
        skip_dirs = ['system32', 'windows', 'temp', 'cache', '.git', 'node_modules', '__pycache__']
        if any(skip_dir in path_str for skip_dir in skip_dirs):
            return False
        
        # Check if file extension matches our patterns
        name_lower = file_path.name.lower()
        for pattern in self.file_patterns:
            if file_path.match(pattern):
                return True
        
        return False
    
    async def _read_file_safely(self, file_path: Path) -> Optional[str]:
        """Safely read file content with encoding detection"""
        try:
            # Try UTF-8 first
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except UnicodeDecodeError:
                # Try other encodings
                encodings = ['latin-1', 'cp1252', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            return f.read()
                    except UnicodeDecodeError:
                        continue
                
                # If all text encodings fail, try binary and decode as base64
                with open(file_path, 'rb') as f:
                    content = f.read()
                    return base64.b64encode(content).decode('ascii')
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Could not read {file_path}: {e}")
            return None
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detect file type for credential classification"""
        name = file_path.name.lower()
        suffix = file_path.suffix.lower()
        
        type_patterns = {
            'api_key': ['api', 'key', 'token'],
            'certificate': ['.pem', '.key', '.p12', '.pfx', '.jks', '.crt'],
            'environment': ['.env'],
            'config': ['config', '.json', '.yaml', '.yml', '.ini', '.cfg'],
            'secret': ['secret', 'password', 'credential'],
            'database': ['.sql', 'database', 'db'],
            'script': ['.py', '.js', '.sh', '.bat', '.ps1']
        }
        
        for file_type, patterns in type_patterns.items():
            if any(pattern in name or pattern == suffix for pattern in patterns):
                return file_type
        
        return 'unknown'
    
    async def health_check(self):
        """Perform system health check"""
        try:
            # Check if processes are running
            if not self.scheduler.running:
                self.logger.warning("⚠️ Scheduler not running, restarting...")
                self.scheduler.start()
            
            # Check database connectivity
            # Add database health check here
            
            # Check disk space for logs and reports
            # Add disk space check here
            
        except Exception as e:
            self.logger.error(f"❌ Health check failed: {e}")
    
    async def cleanup_old_files(self):
        """Cleanup old logs, reports, and backups"""
        try:
            cutoff_date = datetime.now() - timedelta(days=30)
            
            # Cleanup old logs
            log_dir = self.base_path / "logs"
            if log_dir.exists():
                for log_file in log_dir.glob("*.log"):
                    if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                        log_file.unlink()
                        self.logger.debug(f"🗑️ Removed old log: {log_file}")
            
            self.logger.info("🧹 Cleanup completed")
            
        except Exception as e:
            self.logger.error(f"❌ Cleanup failed: {e}")
    
    async def shutdown(self):
        """Graceful shutdown of the system"""
        self.logger.info("🛑 Shutting down Autonomous Credential Collection System...")
        
        self.is_running = False
        
        if self.scheduler.running:
            self.scheduler.shutdown()
        
        if self.file_observer.is_alive():
            self.file_observer.stop()
            self.file_observer.join()
        
        self.logger.info("✅ Autonomous Credential Collection System stopped")

def create_startup_script():
    """Create Windows startup script"""
    script_dir = Path(__file__).parent
    startup_script = f"""@echo off
cd /d "{script_dir.parent}"
python scripts/autonomous_credential_collector.py
pause
"""
    
    with open(script_dir / "start_autonomous_collector.bat", 'w') as f:
        f.write(startup_script)

def main():
    """Main entry point for autonomous credential collection"""
    import argparse
    
    parser = argparse.ArgumentParser(description='A6-9V Autonomous Credential Collection System')
    parser.add_argument('--base-path', default=None, help='Base path for the collection system')
    parser.add_argument('--create-startup', action='store_true', help='Create startup script')
    
    args = parser.parse_args()
    
    if args.create_startup:
        create_startup_script()
        print("✅ Startup script created: start_autonomous_collector.bat")
        return
    
    # Run the autonomous collector
    collector = AutonomousCredentialCollector(args.base_path)
    
    try:
        print("🚀 Starting A6-9V Autonomous Credential Collection System...")
        print("Press Ctrl+C to stop")
        
        asyncio.run(collector.start_autonomous_collection())
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        asyncio.run(collector.shutdown())
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()