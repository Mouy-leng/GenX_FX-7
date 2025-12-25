"""
Health Checker for Python Management System
Lightweight health monitoring to reduce system overhead
"""

import time
import psutil
import requests
import logging
from datetime import datetime
from pathlib import Path


class HealthChecker:
    """Lightweight health checker for better system performance"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def check_system_health(self) -> dict:
        """Quick system health check with minimal overhead"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)  # Quick check
            memory = psutil.virtual_memory()
            
            health = {
                'timestamp': datetime.now().isoformat(),
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'status': 'healthy'
            }
            
            # Simple health thresholds
            if cpu_percent > 85 or memory.percent > 85:
                health['status'] = 'warning'
            
            if cpu_percent > 95 or memory.percent > 95:
                health['status'] = 'critical'
            
            return health
            
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    def check_service_health(self, url: str) -> dict:
        """Quick service health check"""
        try:
            response = requests.get(url, timeout=5)
            return {
                'service_url': url,
                'status_code': response.status_code,
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                'service_url': url,
                'status': 'unhealthy',
                'error': str(e)
            }


if __name__ == "__main__":
    checker = HealthChecker()
    
    print("=== A6-9V System Health Check ===")
    
    # System health
    system_health = checker.check_system_health()
    print(f"System Status: {system_health['status'].upper()}")
    print(f"CPU Usage: {system_health['cpu_usage']:.1f}%")
    print(f"Memory Usage: {system_health['memory_usage']:.1f}%")
    
    # Service health (if enabled)
    service_health = checker.check_service_health('http://localhost:5000/health')
    print(f"Local Server: {service_health['status'].upper()}")
    
    print("=" * 35)