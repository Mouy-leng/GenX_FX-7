"""
Metrics Collector - Advanced metrics and monitoring
Handles performance tracking, alerts, and system health monitoring
"""

import asyncio
import logging
import json
import sqlite3
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import numpy as np
import pandas as pd
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MetricType(Enum):
    """Metric types"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertLevel(Enum):
    """Alert levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Metric:
    """Metric data structure"""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = None
    metric_type: MetricType = MetricType.GAUGE


@dataclass
class Alert:
    """Alert data structure"""
    id: str
    level: AlertLevel
    message: str
    timestamp: datetime
    source: str
    metadata: Dict[str, Any] = None


@dataclass
class MetricsConfig:
    """Metrics configuration"""
    storage_path: str = "metrics"
    retention_days: int = 30
    alert_thresholds: Dict[str, float] = None
    email_alerts: bool = True
    email_recipients: List[str] = None
    dashboard_enabled: bool = True


class MetricsCollector:
    """
    Advanced metrics collection and monitoring system
    """
    
    def __init__(self, config: MetricsConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Storage management
        self.storage_path = Path(config.storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Database connection
        self.db_path = self.storage_path / "metrics.db"
        self.db_connection = None
        
        # Metrics storage
        self.metrics_buffer = []
        self.alerts = []
        
        # Performance tracking
        self.performance_metrics = {}
        self.system_health = {}
        
        # Background tasks
        self.is_running = False
        
        # Alert thresholds (default)
        if self.config.alert_thresholds is None:
            self.config.alert_thresholds = {
                'portfolio_drawdown': 0.1,
                'daily_loss': 0.05,
                'model_accuracy': 0.7,
                'system_uptime': 0.95
            }
        
        # Email configuration
        if self.config.email_recipients is None:
            self.config.email_recipients = []
    
    async def initialize(self) -> bool:
        """Initialize metrics collector"""
        try:
            self.logger.info("Initializing metrics collector...")
            
            # Initialize database
            await self._initialize_database()
            
            # Start background tasks
            self.is_running = True
            asyncio.create_task(self._metrics_processing_loop())
            asyncio.create_task(self._health_monitoring_loop())
            asyncio.create_task(self._alert_processing_loop())
            
            self.logger.info("Metrics collector initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize metrics collector: {e}")
            return False
    
    async def record_metric(self, name: str, value: float, tags: Dict[str, str] = None, metric_type: MetricType = MetricType.GAUGE) -> None:
        """Record a metric"""
        try:
            metric = Metric(
                name=name,
                value=value,
                timestamp=datetime.now(),
                tags=tags or {},
                metric_type=metric_type
            )
            
            # Add to buffer
            self.metrics_buffer.append(metric)
            
            # Check alert thresholds
            await self._check_alert_thresholds(metric)
            
        except Exception as e:
            self.logger.error(f"Error recording metric {name}: {e}")
    
    async def record_trade(self, trade_result: Dict[str, Any]) -> None:
        """Record trade execution"""
        try:
            # Record trade metrics
            await self.record_metric('trades_executed', 1, {'symbol': trade_result.get('symbol', 'unknown')})
            await self.record_metric('trade_pnl', trade_result.get('pnl', 0), {'symbol': trade_result.get('symbol', 'unknown')})
            await self.record_metric('trade_volume', trade_result.get('volume', 0), {'symbol': trade_result.get('symbol', 'unknown')})
            
            # Update performance metrics
            await self._update_performance_metrics(trade_result)
            
        except Exception as e:
            self.logger.error(f"Error recording trade: {e}")
    
    async def record_signals(self, signals: List[Dict[str, Any]]) -> None:
        """Record trading signals"""
        try:
            await self.record_metric('signals_generated', len(signals))
            
            # Record signal metrics by strategy
            strategy_counts = {}
            for signal in signals:
                strategy = signal.get('strategy', 'unknown')
                strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            
            for strategy, count in strategy_counts.items():
                await self.record_metric('signals_by_strategy', count, {'strategy': strategy})
            
        except Exception as e:
            self.logger.error(f"Error recording signals: {e}")
    
    async def record_model_registration(self, metadata: Any) -> None:
        """Record model registration"""
        try:
            await self.record_metric('models_registered', 1, {'model_type': metadata.model_type.value})
            await self.record_metric('model_accuracy', metadata.performance_metrics.get('accuracy', 0), {'model_id': metadata.model_id})
            
        except Exception as e:
            self.logger.error(f"Error recording model registration: {e}")
    
    async def record_model_deployment(self, metadata: Any) -> None:
        """Record model deployment"""
        try:
            await self.record_metric('models_deployed', 1, {'model_type': metadata.model_type.value})
            
        except Exception as e:
            self.logger.error(f"Error recording model deployment: {e}")
    
    async def record_risk_event(self, event: Any, metadata: Dict[str, Any]) -> None:
        """Record risk event"""
        try:
            await self.record_metric('risk_events', 1, {'event_type': event.value})
            
            # Record specific risk metrics
            if 'portfolio_value' in metadata:
                await self.record_metric('portfolio_value', metadata['portfolio_value'])
            if 'daily_pnl' in metadata:
                await self.record_metric('daily_pnl', metadata['daily_pnl'])
            
        except Exception as e:
            self.logger.error(f"Error recording risk event: {e}")
    
    async def record_improvement(self, improvement: Any, result: Dict[str, Any]) -> None:
        """Record self-improvement"""
        try:
            await self.record_metric('improvements_applied', 1, {'improvement_type': improvement.type.value})
            
            if result.get('success'):
                await self.record_metric('improvement_success_rate', 1, {'improvement_type': improvement.type.value})
            else:
                await self.record_metric('improvement_failure_rate', 1, {'improvement_type': improvement.type.value})
            
        except Exception as e:
            self.logger.error(f"Error recording improvement: {e}")
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        try:
            # Get recent metrics
            recent_metrics = await self._get_recent_metrics(hours=24)
            
            # Calculate performance metrics
            performance = {
                'total_trades': self._get_metric_sum(recent_metrics, 'trades_executed'),
                'total_pnl': self._get_metric_sum(recent_metrics, 'trade_pnl'),
                'win_rate': self._calculate_win_rate(recent_metrics),
                'sharpe_ratio': self._calculate_sharpe_ratio(recent_metrics),
                'max_drawdown': self._calculate_max_drawdown(recent_metrics),
                'signals_generated': self._get_metric_sum(recent_metrics, 'signals_generated'),
                'models_deployed': self._get_metric_sum(recent_metrics, 'models_deployed'),
                'improvements_applied': self._get_metric_sum(recent_metrics, 'improvements_applied')
            }
            
            return performance
            
        except Exception as e:
            self.logger.error(f"Error getting performance summary: {e}")
            return {}
    
    async def get_current_return(self) -> float:
        """Get current return"""
        try:
            recent_metrics = await self._get_recent_metrics(hours=24)
            return self._get_metric_sum(recent_metrics, 'trade_pnl')
            
        except Exception as e:
            self.logger.error(f"Error getting current return: {e}")
            return 0.0
    
    async def get_sharpe_ratio(self) -> float:
        """Get Sharpe ratio"""
        try:
            recent_metrics = await self._get_recent_metrics(hours=24)
            return self._calculate_sharpe_ratio(recent_metrics)
            
        except Exception as e:
            self.logger.error(f"Error getting Sharpe ratio: {e}")
            return 0.0
    
    async def get_max_drawdown(self) -> float:
        """Get maximum drawdown"""
        try:
            recent_metrics = await self._get_recent_metrics(hours=24)
            return self._calculate_max_drawdown(recent_metrics)
            
        except Exception as e:
            self.logger.error(f"Error getting max drawdown: {e}")
            return 0.0
    
    async def get_win_rate(self) -> float:
        """Get win rate"""
        try:
            recent_metrics = await self._get_recent_metrics(hours=24)
            return self._calculate_win_rate(recent_metrics)
            
        except Exception as e:
            self.logger.error(f"Error getting win rate: {e}")
            return 0.0
    
    async def get_total_trades(self) -> int:
        """Get total trades"""
        try:
            recent_metrics = await self._get_recent_metrics(hours=24)
            return int(self._get_metric_sum(recent_metrics, 'trades_executed'))
            
        except Exception as e:
            self.logger.error(f"Error getting total trades: {e}")
            return 0
    
    async def get_recent_trades(self) -> List[Dict[str, Any]]:
        """Get recent trades"""
        try:
            # This would typically query the database for recent trades
            # For now, return empty list
            return []
            
        except Exception as e:
            self.logger.error(f"Error getting recent trades: {e}")
            return []
    
    async def get_recent_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """Get recent metrics"""
        try:
            return await self._get_recent_metrics(hours)
            
        except Exception as e:
            self.logger.error(f"Error getting recent metrics: {e}")
            return {}
    
    async def get_performance_data(self) -> Dict[str, Any]:
        """Get performance data for analysis"""
        try:
            recent_metrics = await self._get_recent_metrics(hours=168)  # Last week
            
            return {
                'returns': self._extract_metric_values(recent_metrics, 'trade_pnl'),
                'trades': self._extract_metric_values(recent_metrics, 'trades_executed'),
                'signals': self._extract_metric_values(recent_metrics, 'signals_generated'),
                'models': self._extract_metric_values(recent_metrics, 'models_deployed')
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance data: {e}")
            return {}
    
    async def send_alert(self, alert_type: str, message: str, level: AlertLevel = AlertLevel.INFO) -> None:
        """Send alert"""
        try:
            alert = Alert(
                id=f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                level=level,
                message=message,
                timestamp=datetime.now(),
                source=alert_type
            )
            
            # Add to alerts
            self.alerts.append(alert)
            
            # Send email if configured
            if self.config.email_alerts and self.config.email_recipients:
                await self._send_email_alert(alert)
            
            # Log alert
            if level == AlertLevel.CRITICAL:
                self.logger.critical(f"CRITICAL ALERT: {message}")
            elif level == AlertLevel.ERROR:
                self.logger.error(f"ERROR ALERT: {message}")
            elif level == AlertLevel.WARNING:
                self.logger.warning(f"WARNING ALERT: {message}")
            else:
                self.logger.info(f"INFO ALERT: {message}")
            
        except Exception as e:
            self.logger.error(f"Error sending alert: {e}")
    
    async def _initialize_database(self) -> None:
        """Initialize metrics database"""
        try:
            self.db_connection = sqlite3.connect(self.db_path)
            cursor = self.db_connection.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    timestamp DATETIME NOT NULL,
                    tags TEXT,
                    metric_type TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id TEXT PRIMARY KEY,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    source TEXT NOT NULL,
                    metadata TEXT
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_name_timestamp ON metrics(name, timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)')
            
            self.db_connection.commit()
            self.logger.info("Metrics database initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    async def _metrics_processing_loop(self) -> None:
        """Process metrics buffer"""
        while self.is_running:
            try:
                if self.metrics_buffer:
                    # Process metrics in batches
                    batch_size = 100
                    batch = self.metrics_buffer[:batch_size]
                    self.metrics_buffer = self.metrics_buffer[batch_size:]
                    
                    # Store metrics
                    await self._store_metrics(batch)
                
                await asyncio.sleep(10)  # Process every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error in metrics processing loop: {e}")
                await asyncio.sleep(10)
    
    async def _health_monitoring_loop(self) -> None:
        """Monitor system health"""
        while self.is_running:
            try:
                # Check system health
                health_status = await self._check_system_health()
                
                if not health_status['healthy']:
                    await self.send_alert('SYSTEM_HEALTH', f"System health issues: {health_status['issues']}", AlertLevel.WARNING)
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in health monitoring loop: {e}")
                await asyncio.sleep(60)
    
    async def _alert_processing_loop(self) -> None:
        """Process alerts"""
        while self.is_running:
            try:
                if self.alerts:
                    # Store alerts in database
                    await self._store_alerts(self.alerts)
                    self.alerts = []
                
                await asyncio.sleep(30)  # Process every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in alert processing loop: {e}")
                await asyncio.sleep(30)
    
    async def _store_metrics(self, metrics: List[Metric]) -> None:
        """Store metrics in database"""
        try:
            cursor = self.db_connection.cursor()
            
            for metric in metrics:
                cursor.execute('''
                    INSERT INTO metrics (name, value, timestamp, tags, metric_type)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    metric.name,
                    metric.value,
                    metric.timestamp.isoformat(),
                    json.dumps(metric.tags) if metric.tags else None,
                    metric.metric_type.value
                ))
            
            self.db_connection.commit()
            
        except Exception as e:
            self.logger.error(f"Error storing metrics: {e}")
    
    async def _store_alerts(self, alerts: List[Alert]) -> None:
        """Store alerts in database"""
        try:
            cursor = self.db_connection.cursor()
            
            for alert in alerts:
                cursor.execute('''
                    INSERT OR REPLACE INTO alerts (id, level, message, timestamp, source, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    alert.id,
                    alert.level.value,
                    alert.message,
                    alert.timestamp.isoformat(),
                    alert.source,
                    json.dumps(alert.metadata) if alert.metadata else None
                ))
            
            self.db_connection.commit()
            
        except Exception as e:
            self.logger.error(f"Error storing alerts: {e}")
    
    async def _get_recent_metrics(self, hours: int) -> List[Metric]:
        """Get recent metrics from database"""
        try:
            cursor = self.db_connection.cursor()
            
            start_time = datetime.now() - timedelta(hours=hours)
            
            cursor.execute('''
                SELECT name, value, timestamp, tags, metric_type
                FROM metrics
                WHERE timestamp >= ?
                ORDER BY timestamp
            ''', (start_time.isoformat(),))
            
            rows = cursor.fetchall()
            
            metrics = []
            for row in rows:
                metric = Metric(
                    name=row[0],
                    value=row[1],
                    timestamp=datetime.fromisoformat(row[2]),
                    tags=json.loads(row[3]) if row[3] else {},
                    metric_type=MetricType(row[4])
                )
                metrics.append(metric)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error getting recent metrics: {e}")
            return []
    
    async def _check_alert_thresholds(self, metric: Metric) -> None:
        """Check if metric exceeds alert thresholds"""
        try:
            threshold = self.config.alert_thresholds.get(metric.name)
            if threshold is not None:
                if metric.value > threshold:
                    await self.send_alert(
                        'THRESHOLD_EXCEEDED',
                        f"Metric {metric.name} exceeded threshold: {metric.value} > {threshold}",
                        AlertLevel.WARNING
                    )
            
        except Exception as e:
            self.logger.error(f"Error checking alert thresholds: {e}")
    
    async def _update_performance_metrics(self, trade_result: Dict[str, Any]) -> None:
        """Update performance metrics"""
        try:
            # Update cumulative metrics
            if 'pnl' in trade_result:
                current_pnl = self.performance_metrics.get('total_pnl', 0)
                self.performance_metrics['total_pnl'] = current_pnl + trade_result['pnl']
            
            if 'volume' in trade_result:
                current_volume = self.performance_metrics.get('total_volume', 0)
                self.performance_metrics['total_volume'] = current_volume + trade_result['volume']
            
        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")
    
    async def _check_system_health(self) -> Dict[str, Any]:
        """Check system health"""
        try:
            health_status = {
                'healthy': True,
                'issues': []
            }
            
            # Check database connection
            if not self.db_connection:
                health_status['healthy'] = False
                health_status['issues'].append('Database connection lost')
            
            # Check metrics buffer size
            if len(self.metrics_buffer) > 1000:
                health_status['healthy'] = False
                health_status['issues'].append('Metrics buffer overflow')
            
            # Check alert count
            if len(self.alerts) > 100:
                health_status['healthy'] = False
                health_status['issues'].append('Too many pending alerts')
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Error checking system health: {e}")
            return {'healthy': False, 'issues': [str(e)]}
    
    async def _send_email_alert(self, alert: Alert) -> None:
        """Send email alert"""
        try:
            # This is a simplified implementation
            # In practice, you'd implement proper email sending
            self.logger.info(f"Email alert would be sent: {alert.message}")
            
        except Exception as e:
            self.logger.error(f"Error sending email alert: {e}")
    
    def _get_metric_sum(self, metrics: List[Metric], name: str) -> float:
        """Get sum of metric values"""
        try:
            return sum(metric.value for metric in metrics if metric.name == name)
        except Exception:
            return 0.0
    
    def _extract_metric_values(self, metrics: List[Metric], name: str) -> List[float]:
        """Extract metric values"""
        try:
            return [metric.value for metric in metrics if metric.name == name]
        except Exception:
            return []
    
    def _calculate_win_rate(self, metrics: List[Metric]) -> float:
        """Calculate win rate"""
        try:
            pnl_values = [metric.value for metric in metrics if metric.name == 'trade_pnl']
            if not pnl_values:
                return 0.0
            
            wins = sum(1 for pnl in pnl_values if pnl > 0)
            return wins / len(pnl_values) if pnl_values else 0.0
            
        except Exception:
            return 0.0
    
    def _calculate_sharpe_ratio(self, metrics: List[Metric]) -> float:
        """Calculate Sharpe ratio"""
        try:
            pnl_values = [metric.value for metric in metrics if metric.name == 'trade_pnl']
            if len(pnl_values) < 2:
                return 0.0
            
            returns = np.array(pnl_values)
            if np.std(returns) == 0:
                return 0.0
            
            return np.mean(returns) / np.std(returns) * np.sqrt(252)  # Annualized
            
        except Exception:
            return 0.0
    
    def _calculate_max_drawdown(self, metrics: List[Metric]) -> float:
        """Calculate maximum drawdown"""
        try:
            pnl_values = [metric.value for metric in metrics if metric.name == 'trade_pnl']
            if not pnl_values:
                return 0.0
            
            cumulative = np.cumsum(pnl_values)
            running_max = np.maximum.accumulate(cumulative)
            drawdown = cumulative - running_max
            
            return abs(np.min(drawdown)) if len(drawdown) > 0 else 0.0
            
        except Exception:
            return 0.0
    
    async def shutdown(self) -> None:
        """Shutdown metrics collector"""
        try:
            self.is_running = False
            
            # Process remaining metrics
            if self.metrics_buffer:
                await self._store_metrics(self.metrics_buffer)
                self.metrics_buffer = []
            
            # Store remaining alerts
            if self.alerts:
                await self._store_alerts(self.alerts)
                self.alerts = []
            
            # Close database connection
            if self.db_connection:
                self.db_connection.close()
            
            self.logger.info("Metrics collector shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get metrics collector status"""
        return {
            'is_running': self.is_running,
            'metrics_buffer_size': len(self.metrics_buffer),
            'alerts_count': len(self.alerts),
            'performance_metrics': self.performance_metrics,
            'config': self.config.__dict__
        }
