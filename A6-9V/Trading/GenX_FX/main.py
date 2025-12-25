"""
GenX-FX Autonomous Trading System
Main application entry point
"""

import asyncio
import logging
import signal
import sys
from typing import Dict, Any
from datetime import datetime

from core.autonomous_agent import AutonomousAgent, AgentConfig
from core.self_manager import SelfManager, SelfManagerConfig
from core.decision_engine import DecisionEngine, DecisionEngineConfig
from core.risk_manager import RiskManager, RiskLimits
from ml.model_registry import ModelRegistry, ModelRegistryConfig
from data.market_data import MarketDataManager, MarketDataConfig
from execution.broker_adapter import BrokerAdapter, BrokerConfig, BrokerType
from observability.metrics import MetricsCollector, MetricsConfig


class GenXTradingSystem:
    """
    Main GenX-FX Autonomous Trading System
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        
        # Initialize components
        self.agent = None
        self.self_manager = None
        self.decision_engine = None
        self.risk_manager = None
        self.model_registry = None
        self.market_data = None
        self.broker = None
        self.metrics = None
        
    async def initialize(self) -> bool:
        """Initialize the trading system"""
        try:
            self.logger.info("Initializing GenX-FX Autonomous Trading System...")
            
            # Initialize configurations
            await self._initialize_configurations()
            
            # Initialize core components
            await self._initialize_core_components()
            
            # Initialize trading components
            await self._initialize_trading_components()
            
            # Initialize observability
            await self._initialize_observability()
            
            self.logger.info("GenX-FX Trading System initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize trading system: {e}")
            return False
    
    async def _initialize_configurations(self) -> None:
        """Initialize system configurations"""
        # Agent configuration
        self.agent_config = AgentConfig(
            max_risk_per_trade=0.02,
            max_daily_loss=0.05,
            learning_rate=0.001,
            update_frequency=300,
            self_improvement_threshold=0.1,
            emergency_stop_loss=0.1,
            auto_update_enabled=True,
            human_approval_required=True
        )
        
        # Self-manager configuration
        self.self_manager_config = SelfManagerConfig(
            auto_apply_low_risk=True,
            require_approval_high_risk=True,
            max_improvements_per_day=5,
            improvement_threshold=0.7,
            rollback_threshold=0.3,
            backup_frequency=3600,
            validation_timeout=300
        )
        
        # Decision engine configuration
        self.decision_engine_config = DecisionEngineConfig(
            max_signals_per_cycle=10,
            min_confidence=0.6,
            max_position_size=0.1,
            risk_per_trade=0.02,
            lookback_period=100,
            feature_window=20,
            model_ensemble_size=5,
            adaptive_learning=True
        )
        
        # Risk management configuration
        self.risk_limits = RiskLimits(
            max_position_size=0.1,
            max_daily_loss=0.05,
            max_drawdown=0.15,
            max_correlation=0.7,
            max_volatility=0.3,
            max_leverage=2.0,
            max_positions=10,
            emergency_stop_loss=0.2
        )
        
        # Model registry configuration
        self.model_registry_config = ModelRegistryConfig(
            storage_path="models",
            max_models_per_type=10,
            auto_cleanup=True,
            validation_threshold=0.7,
            deployment_threshold=0.8,
            backup_frequency=3600
        )
        
        # Market data configuration
        self.market_data_config = MarketDataConfig(
            symbols=['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'],
            data_sources=[],
            update_frequency=1,
            history_days=365,
            storage_path="market_data",
            real_time_enabled=True,
            backup_enabled=True
        )
        
        # Broker configuration
        self.broker_config = BrokerConfig(
            broker_type=BrokerType.ALPACA,
            api_key="your_api_key_here",
            secret_key="your_secret_key_here",
            base_url="https://paper-api.alpaca.markets",
            sandbox=True,
            timeout=30,
            retry_attempts=3
        )
        
        # Metrics configuration
        self.metrics_config = MetricsConfig(
            storage_path="metrics",
            retention_days=30,
            alert_thresholds={
                'portfolio_drawdown': 0.1,
                'daily_loss': 0.05,
                'model_accuracy': 0.7,
                'system_uptime': 0.95
            },
            email_alerts=True,
            email_recipients=[],
            dashboard_enabled=True
        )
    
    async def _initialize_core_components(self) -> None:
        """Initialize core system components"""
        # Initialize metrics collector
        self.metrics = MetricsCollector(self.metrics_config)
        await self.metrics.initialize()
        
        # Initialize model registry
        self.model_registry = ModelRegistry(self.model_registry_config)
        await self.model_registry.initialize(metrics=self.metrics)
        
        # Initialize self-manager
        self.self_manager = SelfManager(self.self_manager_config)
        await self.self_manager.initialize(
            model_registry=self.model_registry,
            metrics=self.metrics
        )
        
        # Initialize risk manager
        self.risk_manager = RiskManager(self.risk_limits)
        await self.risk_manager.initialize(
            broker=self.broker,
            metrics=self.metrics
        )
    
    async def _initialize_trading_components(self) -> None:
        """Initialize trading components"""
        # Initialize market data manager
        self.market_data = MarketDataManager(self.market_data_config)
        await self.market_data.initialize(metrics=self.metrics)
        
        # Initialize broker adapter
        self.broker = BrokerAdapter(self.broker_config)
        await self.broker.initialize(metrics=self.metrics)
        
        # Initialize decision engine
        self.decision_engine = DecisionEngine(self.decision_engine_config)
        await self.decision_engine.initialize(
            model_registry=self.model_registry,
            market_data=self.market_data,
            metrics=self.metrics
        )
    
    async def _initialize_observability(self) -> None:
        """Initialize observability components"""
        # Initialize autonomous agent (this will initialize all components)
        self.agent = AutonomousAgent(self.agent_config)
        await self.agent.initialize(
            market_data=self.market_data,
            broker=self.broker,
            model_registry=self.model_registry,
            decision_engine=self.decision_engine,
            self_manager=self.self_manager,
            metrics=self.metrics
        )
    
    async def start_trading(self) -> None:
        """Start autonomous trading"""
        try:
            if not self.agent:
                raise RuntimeError("System not initialized")
            
            self.logger.info("Starting autonomous trading...")
            self.is_running = True
            
            # Start trading
            await self.agent.start_trading()
            
        except Exception as e:
            self.logger.error(f"Error starting trading: {e}")
            await self.shutdown()
    
    async def pause_trading(self) -> None:
        """Pause trading"""
        try:
            if self.agent:
                await self.agent.pause_trading()
                self.logger.info("Trading paused")
            
        except Exception as e:
            self.logger.error(f"Error pausing trading: {e}")
    
    async def resume_trading(self) -> None:
        """Resume trading"""
        try:
            if self.agent:
                await self.agent.resume_trading()
                self.logger.info("Trading resumed")
            
        except Exception as e:
            self.logger.error(f"Error resuming trading: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        try:
            status = {
                'timestamp': datetime.now().isoformat(),
                'is_running': self.is_running,
                'components': {}
            }
            
            # Get component statuses
            if self.agent:
                status['components']['agent'] = self.agent.get_status()
            
            if self.self_manager:
                status['components']['self_manager'] = self.self_manager.get_status()
            
            if self.decision_engine:
                status['components']['decision_engine'] = self.decision_engine.get_status()
            
            if self.risk_manager:
                status['components']['risk_manager'] = self.risk_manager.get_status()
            
            if self.model_registry:
                status['components']['model_registry'] = self.model_registry.get_status()
            
            if self.market_data:
                status['components']['market_data'] = self.market_data.get_status()
            
            if self.broker:
                status['components']['broker'] = self.broker.get_status()
            
            if self.metrics:
                status['components']['metrics'] = self.metrics.get_status()
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
    
    async def shutdown(self) -> None:
        """Shutdown the trading system"""
        try:
            self.logger.info("Shutting down GenX-FX Trading System...")
            self.is_running = False
            
            # Shutdown components
            if self.agent:
                await self.agent.shutdown()
            
            if self.market_data:
                await self.market_data.shutdown()
            
            if self.broker:
                await self.broker.shutdown()
            
            if self.metrics:
                await self.metrics.shutdown()
            
            self.logger.info("GenX-FX Trading System shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")


async def main():
    """Main application entry point"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('genx_trading.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting GenX-FX Autonomous Trading System...")
    
    # Create trading system
    trading_system = GenXTradingSystem()
    
    # Initialize system
    if not await trading_system.initialize():
        logger.error("Failed to initialize trading system")
        sys.exit(1)
    
    # Set up signal handlers
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(trading_system.shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start trading
        await trading_system.start_trading()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        await trading_system.shutdown()
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await trading_system.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
