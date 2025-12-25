"""
Self-Management System - Autonomous code and configuration management
Handles self-improvement, updates, and autonomous decision making
"""

import asyncio
import logging
import json
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import git
import subprocess
import os
from pathlib import Path

# Import statements moved to avoid circular imports


class ImprovementType(Enum):
    """Types of self-improvements"""
    CODE_UPDATE = "code_update"
    CONFIG_UPDATE = "config_update"
    MODEL_UPDATE = "model_update"
    STRATEGY_UPDATE = "strategy_update"
    RISK_UPDATE = "risk_update"


class RiskLevel(Enum):
    """Risk levels for improvements"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Improvement:
    """Self-improvement proposal"""
    id: str
    type: ImprovementType
    description: str
    confidence: float
    risk_level: RiskLevel
    expected_benefit: float
    implementation_plan: List[str]
    rollback_plan: List[str]
    dependencies: List[str]
    created_at: datetime
    status: str = "pending"


@dataclass
class SelfManagerConfig:
    """Configuration for self-manager"""
    auto_apply_low_risk: bool = True
    require_approval_high_risk: bool = True
    max_improvements_per_day: int = 5
    improvement_threshold: float = 0.7
    rollback_threshold: float = 0.3
    backup_frequency: int = 3600  # seconds
    validation_timeout: int = 300  # seconds


class SelfManager:
    """
    Advanced self-management system for autonomous trading agent
    Handles code updates, configuration changes, and self-improvement
    """
    
    def __init__(self, config: SelfManagerConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.model_registry = None
        self.metrics = None
        
        # State management
        self.improvements_queue = []
        self.applied_improvements = []
        self.failed_improvements = []
        self.current_state = {}
        
        # Git repository management
        self.repo_path = Path(__file__).parent.parent.parent
        self.repo = None
        self._init_git_repo()
        
        # Backup management
        self.backup_path = self.repo_path / "backups"
        self.backup_path.mkdir(exist_ok=True)
        
        # Performance tracking
        self.daily_improvements = 0
        self.last_backup = datetime.now()
        
    def _init_git_repo(self):
        """Initialize git repository for version control"""
        try:
            self.repo = git.Repo(self.repo_path)
            self.logger.info("Git repository initialized")
        except git.InvalidGitRepositoryError:
            # Initialize new git repository
            self.repo = git.Repo.init(self.repo_path)
            self.logger.info("New git repository initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize git repository: {e}")
    
    async def initialize(self, model_registry=None, metrics=None) -> bool:
        """Initialize self-manager"""
        try:
            self.logger.info("Initializing self-manager...")
            
            # Set components if provided
            if model_registry:
                self.model_registry = model_registry
            if metrics:
                self.metrics = metrics
            
            # Load current state
            await self._load_state()
            
            # Start background tasks
            asyncio.create_task(self._backup_loop())
            asyncio.create_task(self._improvement_processor())
            asyncio.create_task(self._health_monitor())
            
            self.logger.info("Self-manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize self-manager: {e}")
            return False
    
    async def get_available_improvements(self) -> List[Improvement]:
        """Get available self-improvements"""
        improvements = []
        
        # Analyze current performance
        performance_analysis = await self._analyze_performance()
        
        # Generate improvement suggestions
        if performance_analysis['needs_model_update']:
            improvements.append(await self._create_model_improvement())
        
        if performance_analysis['needs_config_update']:
            improvements.append(await self._create_config_improvement())
        
        if performance_analysis['needs_strategy_update']:
            improvements.append(await self._create_strategy_improvement())
        
        if performance_analysis['needs_risk_update']:
            improvements.append(await self._create_risk_improvement())
        
        return improvements
    
    async def _analyze_performance(self) -> Dict[str, bool]:
        """Analyze current performance for improvement opportunities"""
        # Get recent performance metrics
        recent_metrics = await self.metrics.get_recent_metrics(hours=24)
        
        analysis = {
            'needs_model_update': False,
            'needs_config_update': False,
            'needs_strategy_update': False,
            'needs_risk_update': False
        }
        
        # Check model performance
        if recent_metrics.get('model_accuracy', 1.0) < 0.7:
            analysis['needs_model_update'] = True
        
        # Check configuration effectiveness
        if recent_metrics.get('config_effectiveness', 1.0) < 0.8:
            analysis['needs_config_update'] = True
        
        # Check strategy performance
        if recent_metrics.get('strategy_performance', 0.0) < 0.05:
            analysis['needs_strategy_update'] = True
        
        # Check risk management
        if recent_metrics.get('risk_management_score', 1.0) < 0.9:
            analysis['needs_risk_update'] = True
        
        return analysis
    
    async def _create_model_improvement(self) -> Improvement:
        """Create model improvement suggestion"""
        return Improvement(
            id=f"model_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type=ImprovementType.MODEL_UPDATE,
            description="Retrain models with latest data and improved features",
            confidence=0.85,
            risk_level=RiskLevel.MEDIUM,
            expected_benefit=0.15,
            implementation_plan=[
                "Collect latest training data",
                "Feature engineering improvements",
                "Model retraining with new data",
                "Validation and testing",
                "Model deployment"
            ],
            rollback_plan=[
                "Revert to previous model version",
                "Restore previous configuration",
                "Validate system stability"
            ],
            dependencies=["data_pipeline", "model_registry"],
            created_at=datetime.now()
        )
    
    async def _create_config_improvement(self) -> Improvement:
        """Create configuration improvement suggestion"""
        return Improvement(
            id=f"config_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type=ImprovementType.CONFIG_UPDATE,
            description="Optimize configuration parameters based on recent performance",
            confidence=0.75,
            risk_level=RiskLevel.LOW,
            expected_benefit=0.10,
            implementation_plan=[
                "Analyze current configuration",
                "Calculate optimal parameters",
                "Update configuration files",
                "Validate changes",
                "Deploy new configuration"
            ],
            rollback_plan=[
                "Restore previous configuration",
                "Validate system stability"
            ],
            dependencies=["config_manager"],
            created_at=datetime.now()
        )
    
    async def _create_strategy_improvement(self) -> Improvement:
        """Create strategy improvement suggestion"""
        return Improvement(
            id=f"strategy_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type=ImprovementType.STRATEGY_UPDATE,
            description="Update trading strategy based on market conditions",
            confidence=0.80,
            risk_level=RiskLevel.HIGH,
            expected_benefit=0.20,
            implementation_plan=[
                "Analyze market conditions",
                "Update strategy parameters",
                "Backtest new strategy",
                "Deploy strategy changes",
                "Monitor performance"
            ],
            rollback_plan=[
                "Revert to previous strategy",
                "Close new positions",
                "Restore previous parameters"
            ],
            dependencies=["strategy_engine", "backtesting"],
            created_at=datetime.now()
        )
    
    async def _create_risk_improvement(self) -> Improvement:
        """Create risk management improvement suggestion"""
        return Improvement(
            id=f"risk_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type=ImprovementType.RISK_UPDATE,
            description="Optimize risk management parameters",
            confidence=0.90,
            risk_level=RiskLevel.MEDIUM,
            expected_benefit=0.12,
            implementation_plan=[
                "Analyze risk metrics",
                "Calculate optimal risk parameters",
                "Update risk management rules",
                "Test risk controls",
                "Deploy risk updates"
            ],
            rollback_plan=[
                "Restore previous risk parameters",
                "Validate risk controls"
            ],
            dependencies=["risk_manager"],
            created_at=datetime.now()
        )
    
    async def apply_improvement(self, improvement: Improvement) -> Dict[str, Any]:
        """Apply a self-improvement"""
        try:
            self.logger.info(f"Applying improvement: {improvement.id}")
            
            # Check if we can apply more improvements today
            if self.daily_improvements >= self.config.max_improvements_per_day:
                return {
                    'success': False,
                    'error': 'Daily improvement limit reached'
                }
            
            # Check risk level and approval requirements
            if (improvement.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] and 
                self.config.require_approval_high_risk):
                return {
                    'success': False,
                    'error': 'High risk improvement requires human approval'
                }
            
            # Create backup before applying
            backup_id = await self._create_backup(f"before_{improvement.id}")
            
            # Apply the improvement
            result = await self._execute_improvement(improvement)
            
            if result['success']:
                # Validate the improvement
                validation_result = await self._validate_improvement(improvement)
                
                if validation_result['passed']:
                    # Mark as applied
                    improvement.status = "applied"
                    self.applied_improvements.append(improvement)
                    self.daily_improvements += 1
                    
                    # Record metrics
                    await self.metrics.record_improvement(improvement, result)
                    
                    self.logger.info(f"Improvement applied successfully: {improvement.id}")
                    return {'success': True, 'backup_id': backup_id}
                else:
                    # Rollback if validation failed
                    await self._rollback_improvement(improvement, backup_id)
                    return {
                        'success': False,
                        'error': f"Validation failed: {validation_result['issues']}"
                    }
            else:
                return {
                    'success': False,
                    'error': result['error']
                }
                
        except Exception as e:
            self.logger.error(f"Error applying improvement: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_improvement(self, improvement: Improvement) -> Dict[str, Any]:
        """Execute the improvement implementation"""
        try:
            if improvement.type == ImprovementType.MODEL_UPDATE:
                return await self._execute_model_update(improvement)
            elif improvement.type == ImprovementType.CONFIG_UPDATE:
                return await self._execute_config_update(improvement)
            elif improvement.type == ImprovementType.STRATEGY_UPDATE:
                return await self._execute_strategy_update(improvement)
            elif improvement.type == ImprovementType.RISK_UPDATE:
                return await self._execute_risk_update(improvement)
            else:
                return {'success': False, 'error': 'Unknown improvement type'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _execute_model_update(self, improvement: Improvement) -> Dict[str, Any]:
        """Execute model update improvement"""
        try:
            # Get latest training data
            training_data = await self._get_latest_training_data()
            
            # Retrain models
            new_models = await self._retrain_models(training_data)
            
            # Register new models
            await self.model_registry.register_models(new_models)
            
            return {'success': True, 'models_updated': len(new_models)}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _execute_config_update(self, improvement: Improvement) -> Dict[str, Any]:
        """Execute configuration update improvement"""
        try:
            # Analyze current performance
            performance_data = await self.metrics.get_performance_data()
            
            # Calculate optimal configuration
            optimal_config = await self._calculate_optimal_config(performance_data)
            
            # Update configuration files
            await self._update_configuration_files(optimal_config)
            
            return {'success': True, 'config_updated': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _execute_strategy_update(self, improvement: Improvement) -> Dict[str, Any]:
        """Execute strategy update improvement"""
        try:
            # Analyze market conditions
            market_conditions = await self._analyze_market_conditions()
            
            # Calculate optimal strategy parameters
            optimal_strategy = await self._calculate_optimal_strategy(market_conditions)
            
            # Update strategy configuration
            await self._update_strategy_configuration(optimal_strategy)
            
            return {'success': True, 'strategy_updated': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _execute_risk_update(self, improvement: Improvement) -> Dict[str, Any]:
        """Execute risk management update improvement"""
        try:
            # Analyze risk metrics
            risk_metrics = await self._analyze_risk_metrics()
            
            # Calculate optimal risk parameters
            optimal_risk = await self._calculate_optimal_risk_parameters(risk_metrics)
            
            # Update risk management configuration
            await self._update_risk_configuration(optimal_risk)
            
            return {'success': True, 'risk_updated': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _validate_improvement(self, improvement: Improvement) -> Dict[str, Any]:
        """Validate that improvement is working correctly"""
        try:
            validation_results = {
                'passed': True,
                'issues': []
            }
            
            # Run system health checks
            health_checks = await self._run_health_checks()
            if not health_checks['overall_healthy']:
                validation_results['passed'] = False
                validation_results['issues'].extend(health_checks['issues'])
            
            # Check performance metrics
            performance_check = await self._check_performance_improvement()
            if not performance_check['improved']:
                validation_results['passed'] = False
                validation_results['issues'].append("Performance did not improve")
            
            # Check for errors
            error_check = await self._check_for_errors()
            if error_check['has_errors']:
                validation_results['passed'] = False
                validation_results['issues'].extend(error_check['errors'])
            
            return validation_results
            
        except Exception as e:
            return {
                'passed': False,
                'issues': [f"Validation error: {str(e)}"]
            }
    
    async def rollback_improvement(self, improvement: Improvement) -> Dict[str, Any]:
        """Rollback a failed improvement"""
        try:
            self.logger.info(f"Rolling back improvement: {improvement.id}")
            
            # Find the backup for this improvement
            backup_id = f"before_{improvement.id}"
            backup_path = self.backup_path / f"{backup_id}.tar.gz"
            
            if backup_path.exists():
                # Restore from backup
                await self._restore_from_backup(backup_id)
                
                # Mark improvement as failed
                improvement.status = "failed"
                self.failed_improvements.append(improvement)
                
                self.logger.info(f"Improvement rolled back successfully: {improvement.id}")
                return {'success': True}
            else:
                return {'success': False, 'error': 'Backup not found'}
                
        except Exception as e:
            self.logger.error(f"Error rolling back improvement: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _create_backup(self, backup_id: str) -> str:
        """Create system backup"""
        try:
            backup_path = self.backup_path / f"{backup_id}.tar.gz"
            
            # Create tar backup
            subprocess.run([
                'tar', '-czf', str(backup_path),
                '-C', str(self.repo_path),
                '.'
            ], check=True)
            
            self.last_backup = datetime.now()
            self.logger.info(f"Backup created: {backup_id}")
            return backup_id
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            raise
    
    async def _restore_from_backup(self, backup_id: str) -> None:
        """Restore system from backup"""
        try:
            backup_path = self.backup_path / f"{backup_id}.tar.gz"
            
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup not found: {backup_id}")
            
            # Extract backup
            subprocess.run([
                'tar', '-xzf', str(backup_path),
                '-C', str(self.repo_path)
            ], check=True)
            
            self.logger.info(f"System restored from backup: {backup_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to restore from backup: {e}")
            raise
    
    async def _backup_loop(self) -> None:
        """Periodic backup loop"""
        while True:
            try:
                if datetime.now() - self.last_backup > timedelta(seconds=self.config.backup_frequency):
                    backup_id = f"periodic_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    await self._create_backup(backup_id)
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in backup loop: {e}")
                await asyncio.sleep(60)
    
    async def _improvement_processor(self) -> None:
        """Process improvement queue"""
        while True:
            try:
                if self.improvements_queue:
                    improvement = self.improvements_queue.pop(0)
                    
                    # Check if improvement should be applied
                    if await self._should_apply_improvement(improvement):
                        result = await self.apply_improvement(improvement)
                        
                        if not result['success']:
                            self.logger.warning(f"Failed to apply improvement: {result['error']}")
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error in improvement processor: {e}")
                await asyncio.sleep(10)
    
    async def _health_monitor(self) -> None:
        """Monitor system health"""
        while True:
            try:
                # Check system health
                health_status = await self._check_system_health()
                
                if not health_status['healthy']:
                    self.logger.warning(f"System health issues detected: {health_status['issues']}")
                    
                    # Trigger emergency procedures if necessary
                    if health_status['critical']:
                        await self._trigger_emergency_procedures()
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in health monitor: {e}")
                await asyncio.sleep(30)
    
    async def _should_apply_improvement(self, improvement: Improvement) -> bool:
        """Determine if improvement should be applied"""
        # Check confidence threshold
        if improvement.confidence < self.config.improvement_threshold:
            return False
        
        # Check daily limit
        if self.daily_improvements >= self.config.max_improvements_per_day:
            return False
        
        # Check risk level
        if (improvement.risk_level == RiskLevel.CRITICAL and 
            self.config.require_approval_high_risk):
            return False
        
        return True
    
    async def _load_state(self) -> None:
        """Load self-manager state"""
        try:
            state_file = self.repo_path / "self_manager_state.json"
            
            if state_file.exists():
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                self.daily_improvements = state.get('daily_improvements', 0)
                self.last_backup = datetime.fromisoformat(state.get('last_backup', datetime.now().isoformat()))
                
                self.logger.info("Self-manager state loaded")
            
        except Exception as e:
            self.logger.error(f"Failed to load state: {e}")
    
    async def save_state(self, state: Dict[str, Any]) -> None:
        """Save self-manager state"""
        try:
            state_file = self.repo_path / "self_manager_state.json"
            
            current_state = {
                'daily_improvements': self.daily_improvements,
                'last_backup': self.last_backup.isoformat(),
                'applied_improvements': len(self.applied_improvements),
                'failed_improvements': len(self.failed_improvements),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(state_file, 'w') as f:
                json.dump(current_state, f, indent=2)
            
            self.logger.info("Self-manager state saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get self-manager status"""
        return {
            'daily_improvements': self.daily_improvements,
            'applied_improvements': len(self.applied_improvements),
            'failed_improvements': len(self.failed_improvements),
            'improvements_queue': len(self.improvements_queue),
            'last_backup': self.last_backup.isoformat(),
            'config': self.config.__dict__
        }
