"""
Risk Manager - Advanced risk management and position sizing
Handles risk controls, position limits, and portfolio risk management
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import math

# Import statements moved to avoid circular imports


class RiskLevel(Enum):
    """Risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskEvent(Enum):
    """Risk events"""
    POSITION_LIMIT_EXCEEDED = "position_limit_exceeded"
    DAILY_LOSS_LIMIT_EXCEEDED = "daily_loss_limit_exceeded"
    DRAWDOWN_LIMIT_EXCEEDED = "drawdown_limit_exceeded"
    CORRELATION_LIMIT_EXCEEDED = "correlation_limit_exceeded"
    VOLATILITY_LIMIT_EXCEEDED = "volatility_limit_exceeded"
    EMERGENCY_STOP = "emergency_stop"


@dataclass
class RiskLimits:
    """Risk limits configuration"""
    max_position_size: float = 0.1  # 10% of portfolio
    max_daily_loss: float = 0.05  # 5% daily loss limit
    max_drawdown: float = 0.15  # 15% max drawdown
    max_correlation: float = 0.7  # Max correlation between positions
    max_volatility: float = 0.3  # Max portfolio volatility
    max_leverage: float = 2.0  # Max leverage
    max_positions: int = 10  # Max number of positions
    emergency_stop_loss: float = 0.2  # Emergency stop at 20% loss


@dataclass
class Position:
    """Trading position"""
    symbol: str
    side: str  # 'long' or 'short'
    size: float
    entry_price: float
    current_price: float
    stop_loss: float
    take_profit: float
    timestamp: datetime
    unrealized_pnl: float = 0.0
    risk_metrics: Dict[str, float] = None


@dataclass
class RiskMetrics:
    """Portfolio risk metrics"""
    total_exposure: float
    portfolio_value: float
    daily_pnl: float
    total_pnl: float
    drawdown: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    var_95: float  # Value at Risk 95%
    cvar_95: float  # Conditional Value at Risk 95%


class RiskManager:
    """
    Advanced risk management system
    Handles position sizing, risk limits, and portfolio risk management
    """
    
    def __init__(self, config: RiskLimits):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.broker = None
        self.metrics = None
        
        # State management
        self.positions = {}
        self.risk_events = []
        self.daily_pnl = 0.0
        self.total_pnl = 0.0
        self.portfolio_value = 100000.0  # Starting portfolio value
        self.peak_value = self.portfolio_value
        
        # Risk monitoring
        self.is_monitoring = False
        self.last_risk_check = datetime.now()
        
        # Emergency controls
        self.emergency_stop = False
        self.risk_alerts = []
        
    async def initialize(self, broker=None, metrics=None) -> bool:
        """Initialize risk manager"""
        try:
            self.logger.info("Initializing risk manager...")
            
            # Set components if provided
            if broker:
                self.broker = broker
            if metrics:
                self.metrics = metrics
            
            # Load current positions
            await self._load_positions()
            
            # Start risk monitoring
            asyncio.create_task(self._risk_monitoring_loop())
            
            self.logger.info("Risk manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize risk manager: {e}")
            return False
    
    async def filter_signals(self, signals: List[Dict]) -> List[Dict]:
        """Filter trading signals based on risk criteria"""
        filtered_signals = []
        
        for signal in signals:
            try:
                # Check if signal passes risk filters
                if await self._check_signal_risk(signal):
                    # Calculate optimal position size
                    signal['position_size'] = await self._calculate_position_size(signal)
                    filtered_signals.append(signal)
                else:
                    self.logger.warning(f"Signal filtered by risk manager: {signal.get('symbol', 'unknown')}")
                    
            except Exception as e:
                self.logger.error(f"Error filtering signal: {e}")
        
        return filtered_signals
    
    async def check_risk_limits(self, signal: Dict) -> bool:
        """Check if signal violates risk limits"""
        try:
            # Check emergency stop
            if self.emergency_stop:
                return False
            
            # Check daily loss limit
            if self.daily_pnl <= -self.config.max_daily_loss * self.portfolio_value:
                await self._trigger_risk_event(RiskEvent.DAILY_LOSS_LIMIT_EXCEEDED)
                return False
            
            # Check drawdown limit
            current_drawdown = (self.peak_value - self.portfolio_value) / self.peak_value
            if current_drawdown >= self.config.max_drawdown:
                await self._trigger_risk_event(RiskEvent.DRAWDOWN_LIMIT_EXCEEDED)
                return False
            
            # Check position limits
            if len(self.positions) >= self.config.max_positions:
                await self._trigger_risk_event(RiskEvent.POSITION_LIMIT_EXCEEDED)
                return False
            
            # Check position size
            position_size = signal.get('position_size', 0)
            if position_size > self.config.max_position_size * self.portfolio_value:
                return False
            
            # Check correlation limits
            if await self._check_correlation_limits(signal):
                return False
            
            # Check volatility limits
            if await self._check_volatility_limits(signal):
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking risk limits: {e}")
            return False
    
    async def _check_signal_risk(self, signal: Dict) -> bool:
        """Check if signal meets risk criteria"""
        # Check basic risk limits
        if not await self.check_risk_limits(signal):
            return False
        
        # Check signal-specific risk
        symbol = signal.get('symbol', '')
        confidence = signal.get('confidence', 0)
        
        # Minimum confidence threshold
        if confidence < 0.6:
            return False
        
        # Check if we already have a position in this symbol
        if symbol in self.positions:
            existing_position = self.positions[symbol]
            # Don't add to losing positions
            if existing_position.unrealized_pnl < -0.02 * self.portfolio_value:
                return False
        
        return True
    
    async def _calculate_position_size(self, signal: Dict) -> float:
        """Calculate optimal position size using Kelly Criterion and risk management"""
        try:
            symbol = signal.get('symbol', '')
            confidence = signal.get('confidence', 0.5)
            entry_price = signal.get('entry_price', 0)
            stop_loss = signal.get('stop_loss', entry_price)
            
            if entry_price == 0:
                return 0
            
            # Calculate risk per trade
            risk_per_trade = min(
                self.config.max_position_size * self.portfolio_value,
                self.config.max_daily_loss * self.portfolio_value * 0.1  # 10% of daily loss limit
            )
            
            # Calculate stop loss distance
            stop_distance = abs(entry_price - stop_loss) / entry_price
            
            if stop_distance == 0:
                return 0
            
            # Kelly Criterion position sizing
            win_probability = confidence
            win_loss_ratio = 2.0  # Assume 2:1 reward to risk ratio
            
            kelly_fraction = (win_probability * win_loss_ratio - (1 - win_probability)) / win_loss_ratio
            kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
            
            # Calculate position size
            position_size = (risk_per_trade / stop_distance) * kelly_fraction
            
            # Apply additional risk controls
            max_position_value = self.config.max_position_size * self.portfolio_value
            position_size = min(position_size, max_position_value / entry_price)
            
            # Apply confidence scaling
            position_size *= confidence
            
            return max(0, position_size)
            
        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0
    
    async def _check_correlation_limits(self, signal: Dict) -> bool:
        """Check if signal violates correlation limits"""
        try:
            symbol = signal.get('symbol', '')
            
            if len(self.positions) < 2:
                return False
            
            # Calculate correlation with existing positions
            for existing_symbol, position in self.positions.items():
                correlation = await self._calculate_correlation(symbol, existing_symbol)
                
                if correlation > self.config.max_correlation:
                    self.logger.warning(f"High correlation detected: {symbol} vs {existing_symbol} ({correlation:.2f})")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking correlation limits: {e}")
            return False
    
    async def _check_volatility_limits(self, signal: Dict) -> bool:
        """Check if signal violates volatility limits"""
        try:
            # Calculate portfolio volatility with new position
            current_volatility = await self._calculate_portfolio_volatility()
            
            # Estimate volatility impact of new position
            symbol = signal.get('symbol', '')
            position_size = signal.get('position_size', 0)
            
            # Simplified volatility calculation
            estimated_volatility = await self._estimate_symbol_volatility(symbol)
            new_volatility = current_volatility + (estimated_volatility * position_size)
            
            if new_volatility > self.config.max_volatility:
                self.logger.warning(f"Volatility limit would be exceeded: {new_volatility:.2f}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking volatility limits: {e}")
            return False
    
    async def _calculate_correlation(self, symbol1: str, symbol2: str) -> float:
        """Calculate correlation between two symbols"""
        try:
            # This is a simplified implementation
            # In practice, you'd use historical price data
            return 0.3  # Placeholder correlation
            
        except Exception as e:
            self.logger.error(f"Error calculating correlation: {e}")
            return 0
    
    async def _calculate_portfolio_volatility(self) -> float:
        """Calculate current portfolio volatility"""
        try:
            if not self.positions:
                return 0
            
            # Simplified volatility calculation
            total_exposure = sum(pos.size * pos.current_price for pos in self.positions.values())
            portfolio_volatility = 0.15  # Placeholder volatility
            
            return portfolio_volatility * (total_exposure / self.portfolio_value)
            
        except Exception as e:
            self.logger.error(f"Error calculating portfolio volatility: {e}")
            return 0
    
    async def _estimate_symbol_volatility(self, symbol: str) -> float:
        """Estimate volatility for a symbol"""
        try:
            # This is a simplified implementation
            # In practice, you'd calculate historical volatility
            return 0.2  # Placeholder volatility
            
        except Exception as e:
            self.logger.error(f"Error estimating symbol volatility: {e}")
            return 0.2
    
    async def update_position(self, symbol: str, position_data: Dict) -> None:
        """Update position information"""
        try:
            position = Position(
                symbol=symbol,
                side=position_data.get('side', 'long'),
                size=position_data.get('size', 0),
                entry_price=position_data.get('entry_price', 0),
                current_price=position_data.get('current_price', 0),
                stop_loss=position_data.get('stop_loss', 0),
                take_profit=position_data.get('take_profit', 0),
                timestamp=datetime.now()
            )
            
            # Calculate unrealized PnL
            if position.side == 'long':
                position.unrealized_pnl = (position.current_price - position.entry_price) * position.size
            else:
                position.unrealized_pnl = (position.entry_price - position.current_price) * position.size
            
            self.positions[symbol] = position
            
            # Update portfolio metrics
            await self._update_portfolio_metrics()
            
        except Exception as e:
            self.logger.error(f"Error updating position: {e}")
    
    async def close_position(self, symbol: str) -> Dict[str, Any]:
        """Close a position and update metrics"""
        try:
            if symbol not in self.positions:
                return {'success': False, 'error': 'Position not found'}
            
            position = self.positions[symbol]
            
            # Calculate realized PnL
            realized_pnl = position.unrealized_pnl
            self.total_pnl += realized_pnl
            self.daily_pnl += realized_pnl
            
            # Update portfolio value
            self.portfolio_value += realized_pnl
            
            # Remove position
            del self.positions[symbol]
            
            # Update metrics
            await self._update_portfolio_metrics()
            
            self.logger.info(f"Position closed: {symbol}, PnL: {realized_pnl:.2f}")
            
            return {
                'success': True,
                'realized_pnl': realized_pnl,
                'symbol': symbol
            }
            
        except Exception as e:
            self.logger.error(f"Error closing position: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _update_portfolio_metrics(self) -> None:
        """Update portfolio risk metrics"""
        try:
            # Calculate total exposure
            total_exposure = sum(pos.size * pos.current_price for pos in self.positions.values())
            
            # Update peak value
            if self.portfolio_value > self.peak_value:
                self.peak_value = self.portfolio_value
            
            # Calculate drawdown
            drawdown = (self.peak_value - self.portfolio_value) / self.peak_value
            
            # Check for risk events
            if drawdown >= self.config.max_drawdown:
                await self._trigger_risk_event(RiskEvent.DRAWDOWN_LIMIT_EXCEEDED)
            
            if self.daily_pnl <= -self.config.max_daily_loss * self.portfolio_value:
                await self._trigger_risk_event(RiskEvent.DAILY_LOSS_LIMIT_EXCEEDED)
            
            # Check emergency stop
            if self.total_pnl <= -self.config.emergency_stop_loss * self.portfolio_value:
                await self._trigger_risk_event(RiskEvent.EMERGENCY_STOP)
            
        except Exception as e:
            self.logger.error(f"Error updating portfolio metrics: {e}")
    
    async def _trigger_risk_event(self, event: RiskEvent) -> None:
        """Trigger a risk event"""
        try:
            self.risk_events.append({
                'event': event.value,
                'timestamp': datetime.now(),
                'portfolio_value': self.portfolio_value,
                'daily_pnl': self.daily_pnl,
                'total_pnl': self.total_pnl
            })
            
            self.logger.warning(f"Risk event triggered: {event.value}")
            
            # Handle emergency stop
            if event == RiskEvent.EMERGENCY_STOP:
                await self._emergency_stop()
            
            # Record risk alert
            await self.metrics.record_risk_event(event, {
                'portfolio_value': self.portfolio_value,
                'daily_pnl': self.daily_pnl,
                'total_pnl': self.total_pnl
            })
            
        except Exception as e:
            self.logger.error(f"Error triggering risk event: {e}")
    
    async def _emergency_stop(self) -> None:
        """Emergency stop all trading"""
        try:
            self.emergency_stop = True
            self.logger.critical("EMERGENCY STOP TRIGGERED!")
            
            # Close all positions
            for symbol in list(self.positions.keys()):
                await self.close_position(symbol)
            
            # Send emergency alert
            await self.metrics.send_alert("EMERGENCY_STOP", "All positions closed due to risk limits")
            
        except Exception as e:
            self.logger.error(f"Error in emergency stop: {e}")
    
    async def _risk_monitoring_loop(self) -> None:
        """Continuous risk monitoring loop"""
        while True:
            try:
                if not self.emergency_stop:
                    # Update position prices
                    await self._update_position_prices()
                    
                    # Check risk limits
                    await self._check_all_risk_limits()
                    
                    # Update portfolio metrics
                    await self._update_portfolio_metrics()
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error in risk monitoring loop: {e}")
                await asyncio.sleep(10)
    
    async def _update_position_prices(self) -> None:
        """Update current prices for all positions"""
        try:
            for symbol, position in self.positions.items():
                # Get current price from broker
                current_price = await self.broker.get_current_price(symbol)
                if current_price:
                    position.current_price = current_price
                    
                    # Update unrealized PnL
                    if position.side == 'long':
                        position.unrealized_pnl = (position.current_price - position.entry_price) * position.size
                    else:
                        position.unrealized_pnl = (position.entry_price - position.current_price) * position.size
                        
        except Exception as e:
            self.logger.error(f"Error updating position prices: {e}")
    
    async def _check_all_risk_limits(self) -> None:
        """Check all risk limits"""
        try:
            # Check position limits
            if len(self.positions) > self.config.max_positions:
                await self._trigger_risk_event(RiskEvent.POSITION_LIMIT_EXCEEDED)
            
            # Check daily loss limit
            if self.daily_pnl <= -self.config.max_daily_loss * self.portfolio_value:
                await self._trigger_risk_event(RiskEvent.DAILY_LOSS_LIMIT_EXCEEDED)
            
            # Check drawdown limit
            current_drawdown = (self.peak_value - self.portfolio_value) / self.peak_value
            if current_drawdown >= self.config.max_drawdown:
                await self._trigger_risk_event(RiskEvent.DRAWDOWN_LIMIT_EXCEEDED)
            
        except Exception as e:
            self.logger.error(f"Error checking risk limits: {e}")
    
    async def _load_positions(self) -> None:
        """Load current positions from broker"""
        try:
            positions = await self.broker.get_positions()
            
            for symbol, position_data in positions.items():
                await self.update_position(symbol, position_data)
            
            self.logger.info(f"Loaded {len(positions)} positions")
            
        except Exception as e:
            self.logger.error(f"Error loading positions: {e}")
    
    async def calculate_optimal_parameters(self, recent_trades: List[Dict]) -> Dict[str, Any]:
        """Calculate optimal risk parameters based on recent performance"""
        try:
            if not recent_trades:
                return self.config.__dict__
            
            # Analyze recent performance
            returns = [trade.get('return', 0) for trade in recent_trades]
            win_rate = sum(1 for r in returns if r > 0) / len(returns) if returns else 0.5
            avg_return = np.mean(returns) if returns else 0
            volatility = np.std(returns) if returns else 0.1
            
            # Calculate optimal parameters
            optimal_params = {}
            
            # Adjust position size based on win rate
            if win_rate > 0.6:
                optimal_params['max_position_size'] = min(0.15, self.config.max_position_size * 1.2)
            elif win_rate < 0.4:
                optimal_params['max_position_size'] = max(0.05, self.config.max_position_size * 0.8)
            
            # Adjust daily loss limit based on volatility
            if volatility > 0.2:
                optimal_params['max_daily_loss'] = max(0.02, self.config.max_daily_loss * 0.8)
            elif volatility < 0.1:
                optimal_params['max_daily_loss'] = min(0.08, self.config.max_daily_loss * 1.2)
            
            # Adjust drawdown limit based on performance
            if avg_return > 0.02:
                optimal_params['max_drawdown'] = min(0.20, self.config.max_drawdown * 1.1)
            elif avg_return < -0.01:
                optimal_params['max_drawdown'] = max(0.10, self.config.max_drawdown * 0.9)
            
            return optimal_params
            
        except Exception as e:
            self.logger.error(f"Error calculating optimal parameters: {e}")
            return self.config.__dict__
    
    async def update_parameters(self, new_params: Dict[str, Any]) -> None:
        """Update risk management parameters"""
        try:
            # Update configuration
            for key, value in new_params.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            
            self.logger.info(f"Updated risk parameters: {new_params}")
            
        except Exception as e:
            self.logger.error(f"Error updating risk parameters: {e}")
    
    def get_risk_metrics(self) -> RiskMetrics:
        """Get current risk metrics"""
        try:
            total_exposure = sum(pos.size * pos.current_price for pos in self.positions.values())
            current_drawdown = (self.peak_value - self.portfolio_value) / self.peak_value if self.peak_value > 0 else 0
            
            # Calculate VaR (simplified)
            var_95 = -1.645 * 0.15 * self.portfolio_value  # Simplified VaR calculation
            
            return RiskMetrics(
                total_exposure=total_exposure,
                portfolio_value=self.portfolio_value,
                daily_pnl=self.daily_pnl,
                total_pnl=self.total_pnl,
                drawdown=current_drawdown,
                volatility=0.15,  # Placeholder
                sharpe_ratio=0.5,  # Placeholder
                max_drawdown=current_drawdown,
                var_95=var_95,
                cvar_95=var_95 * 1.2  # Simplified CVaR
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating risk metrics: {e}")
            return RiskMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    def get_status(self) -> Dict[str, Any]:
        """Get risk manager status"""
        return {
            'emergency_stop': self.emergency_stop,
            'positions_count': len(self.positions),
            'portfolio_value': self.portfolio_value,
            'daily_pnl': self.daily_pnl,
            'total_pnl': self.total_pnl,
            'risk_events_count': len(self.risk_events),
            'config': self.config.__dict__
        }
