"""
Decision Engine - Advanced AI-powered trading decision making
Handles signal generation, strategy execution, and adaptive learning
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

# Import statements moved to avoid circular imports


class SignalType(Enum):
    """Types of trading signals"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    CLOSE = "close"


class StrategyType(Enum):
    """Types of trading strategies"""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    BREAKOUT = "breakout"
    ARBITRAGE = "arbitrage"
    ML_PREDICTION = "ml_prediction"


@dataclass
class TradingSignal:
    """Trading signal with metadata"""
    symbol: str
    signal_type: SignalType
    confidence: float
    strength: float
    entry_price: float
    stop_loss: float
    take_profit: float
    position_size: float
    strategy: StrategyType
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class DecisionEngineConfig:
    """Configuration for decision engine"""
    max_signals_per_cycle: int = 10
    min_confidence: float = 0.6
    max_position_size: float = 0.1
    risk_per_trade: float = 0.02
    lookback_period: int = 100
    feature_window: int = 20
    model_ensemble_size: int = 5
    adaptive_learning: bool = True
    strategy_weights: Dict[StrategyType, float] = None


class DecisionEngine:
    """
    Advanced decision engine with AI/ML capabilities
    Generates trading signals using multiple strategies and models
    """
    
    def __init__(self, config: DecisionEngineConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.model_registry = None
        self.market_data = None
        self.metrics = None
        
        # Strategy weights (default)
        if self.config.strategy_weights is None:
            self.config.strategy_weights = {
                StrategyType.ML_PREDICTION: 0.4,
                StrategyType.MOMENTUM: 0.2,
                StrategyType.MEAN_REVERSION: 0.2,
                StrategyType.BREAKOUT: 0.1,
                StrategyType.ARBITRAGE: 0.1
            }
        
        # Models and scalers
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        
        # Performance tracking
        self.signal_history = []
        self.strategy_performance = {}
        self.adaptive_weights = {}
        
        # Learning state
        self.is_learning = False
        self.last_retrain = datetime.now()
        
    async def initialize(self, model_registry=None, market_data=None, metrics=None) -> bool:
        """Initialize decision engine"""
        try:
            self.logger.info("Initializing decision engine...")
            
            # Set components if provided
            if model_registry:
                self.model_registry = model_registry
            if market_data:
                self.market_data = market_data
            if metrics:
                self.metrics = metrics
            
            # Load models
            await self._load_models()
            
            # Initialize strategies
            await self._initialize_strategies()
            
            # Start adaptive learning
            if self.config.adaptive_learning:
                asyncio.create_task(self._adaptive_learning_loop())
            
            self.logger.info("Decision engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize decision engine: {e}")
            return False
    
    async def generate_signals(self, market_data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate trading signals from market data"""
        try:
            signals = []
            
            # Get symbols to analyze
            symbols = market_data.get('symbols', [])
            
            for symbol in symbols:
                # Get symbol data
                symbol_data = market_data.get(symbol, {})
                
                # Generate signals for each strategy
                strategy_signals = await self._generate_strategy_signals(symbol, symbol_data)
                signals.extend(strategy_signals)
            
            # Filter and rank signals
            filtered_signals = await self._filter_signals(signals)
            ranked_signals = await self._rank_signals(filtered_signals)
            
            # Limit number of signals
            final_signals = ranked_signals[:self.config.max_signals_per_cycle]
            
            # Record signals
            self.signal_history.extend(final_signals)
            await self.metrics.record_signals(final_signals)
            
            return final_signals
            
        except Exception as e:
            self.logger.error(f"Error generating signals: {e}")
            return []
    
    async def _generate_strategy_signals(self, symbol: str, data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate signals for a symbol using all strategies"""
        signals = []
        
        try:
            # ML Prediction signals
            if StrategyType.ML_PREDICTION in self.config.strategy_weights:
                ml_signals = await self._generate_ml_signals(symbol, data)
                signals.extend(ml_signals)
            
            # Momentum signals
            if StrategyType.MOMENTUM in self.config.strategy_weights:
                momentum_signals = await self._generate_momentum_signals(symbol, data)
                signals.extend(momentum_signals)
            
            # Mean reversion signals
            if StrategyType.MEAN_REVERSION in self.config.strategy_weights:
                mean_reversion_signals = await self._generate_mean_reversion_signals(symbol, data)
                signals.extend(mean_reversion_signals)
            
            # Breakout signals
            if StrategyType.BREAKOUT in self.config.strategy_weights:
                breakout_signals = await self._generate_breakout_signals(symbol, data)
                signals.extend(breakout_signals)
            
            # Arbitrage signals
            if StrategyType.ARBITRAGE in self.config.strategy_weights:
                arbitrage_signals = await self._generate_arbitrage_signals(symbol, data)
                signals.extend(arbitrage_signals)
            
        except Exception as e:
            self.logger.error(f"Error generating strategy signals for {symbol}: {e}")
        
        return signals
    
    async def _generate_ml_signals(self, symbol: str, data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate ML-based trading signals"""
        signals = []
        
        try:
            # Prepare features
            features = await self._prepare_features(symbol, data)
            
            if features is None or len(features) == 0:
                return signals
            
            # Get predictions from ensemble models
            predictions = []
            confidences = []
            
            for model_name, model in self.models.items():
                if model_name.startswith('ensemble_'):
                    try:
                        # Scale features
                        scaled_features = self.scalers.get(f"{model_name}_scaler", StandardScaler()).transform(features)
                        
                        # Get prediction
                        prediction = model.predict(scaled_features)
                        confidence = model.predict_proba(scaled_features) if hasattr(model, 'predict_proba') else [0.5]
                        
                        predictions.append(prediction[0])
                        confidences.append(confidence[0] if isinstance(confidence[0], (list, np.ndarray)) else confidence[0])
                        
                    except Exception as e:
                        self.logger.warning(f"Error with model {model_name}: {e}")
                        continue
            
            if predictions:
                # Ensemble prediction
                avg_prediction = np.mean(predictions)
                avg_confidence = np.mean(confidences)
                
                # Generate signal based on prediction
                if avg_confidence > self.config.min_confidence:
                    signal_type = SignalType.BUY if avg_prediction > 0.5 else SignalType.SELL
                    
                    signal = TradingSignal(
                        symbol=symbol,
                        signal_type=signal_type,
                        confidence=avg_confidence,
                        strength=abs(avg_prediction - 0.5) * 2,
                        entry_price=data.get('close', 0),
                        stop_loss=self._calculate_stop_loss(data, signal_type),
                        take_profit=self._calculate_take_profit(data, signal_type),
                        position_size=self._calculate_position_size(avg_confidence),
                        strategy=StrategyType.ML_PREDICTION,
                        timestamp=datetime.now(),
                        metadata={
                            'prediction': avg_prediction,
                            'model_count': len(predictions),
                            'features_used': len(features[0]) if features else 0
                        }
                    )
                    
                    signals.append(signal)
        
        except Exception as e:
            self.logger.error(f"Error generating ML signals for {symbol}: {e}")
        
        return signals
    
    async def _generate_momentum_signals(self, symbol: str, data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate momentum-based signals"""
        signals = []
        
        try:
            # Calculate momentum indicators
            rsi = self._calculate_rsi(data.get('close', []))
            macd = self._calculate_macd(data.get('close', []))
            sma_20 = self._calculate_sma(data.get('close', []), 20)
            sma_50 = self._calculate_sma(data.get('close', []), 50)
            
            current_price = data.get('close', [0])[-1] if data.get('close') else 0
            
            # Momentum conditions
            bullish_momentum = (
                rsi > 30 and rsi < 70 and  # Not overbought/oversold
                macd > 0 and  # MACD above zero line
                current_price > sma_20 > sma_50  # Price above moving averages
            )
            
            bearish_momentum = (
                rsi < 70 and rsi > 30 and  # Not overbought/oversold
                macd < 0 and  # MACD below zero line
                current_price < sma_20 < sma_50  # Price below moving averages
            )
            
            if bullish_momentum:
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type=SignalType.BUY,
                    confidence=min(rsi / 100, 0.8),
                    strength=abs(macd) / 100,
                    entry_price=current_price,
                    stop_loss=current_price * 0.98,
                    take_profit=current_price * 1.05,
                    position_size=self.config.max_position_size * 0.5,
                    strategy=StrategyType.MOMENTUM,
                    timestamp=datetime.now(),
                    metadata={
                        'rsi': rsi,
                        'macd': macd,
                        'sma_20': sma_20,
                        'sma_50': sma_50
                    }
                )
                signals.append(signal)
            
            elif bearish_momentum:
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type=SignalType.SELL,
                    confidence=min((100 - rsi) / 100, 0.8),
                    strength=abs(macd) / 100,
                    entry_price=current_price,
                    stop_loss=current_price * 1.02,
                    take_profit=current_price * 0.95,
                    position_size=self.config.max_position_size * 0.5,
                    strategy=StrategyType.MOMENTUM,
                    timestamp=datetime.now(),
                    metadata={
                        'rsi': rsi,
                        'macd': macd,
                        'sma_20': sma_20,
                        'sma_50': sma_50
                    }
                )
                signals.append(signal)
        
        except Exception as e:
            self.logger.error(f"Error generating momentum signals for {symbol}: {e}")
        
        return signals
    
    async def _generate_mean_reversion_signals(self, symbol: str, data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate mean reversion signals"""
        signals = []
        
        try:
            # Calculate mean reversion indicators
            bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(data.get('close', []))
            rsi = self._calculate_rsi(data.get('close', []))
            
            current_price = data.get('close', [0])[-1] if data.get('close') else 0
            
            # Mean reversion conditions
            oversold = current_price <= bb_lower and rsi < 30
            overbought = current_price >= bb_upper and rsi > 70
            
            if oversold:
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type=SignalType.BUY,
                    confidence=0.7,
                    strength=0.8,
                    entry_price=current_price,
                    stop_loss=bb_lower * 0.99,
                    take_profit=bb_middle,
                    position_size=self.config.max_position_size * 0.3,
                    strategy=StrategyType.MEAN_REVERSION,
                    timestamp=datetime.now(),
                    metadata={
                        'bb_upper': bb_upper,
                        'bb_middle': bb_middle,
                        'bb_lower': bb_lower,
                        'rsi': rsi
                    }
                )
                signals.append(signal)
            
            elif overbought:
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type=SignalType.SELL,
                    confidence=0.7,
                    strength=0.8,
                    entry_price=current_price,
                    stop_loss=bb_upper * 1.01,
                    take_profit=bb_middle,
                    position_size=self.config.max_position_size * 0.3,
                    strategy=StrategyType.MEAN_REVERSION,
                    timestamp=datetime.now(),
                    metadata={
                        'bb_upper': bb_upper,
                        'bb_middle': bb_middle,
                        'bb_lower': bb_lower,
                        'rsi': rsi
                    }
                )
                signals.append(signal)
        
        except Exception as e:
            self.logger.error(f"Error generating mean reversion signals for {symbol}: {e}")
        
        return signals
    
    async def _generate_breakout_signals(self, symbol: str, data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate breakout signals"""
        signals = []
        
        try:
            # Calculate breakout indicators
            high_20 = max(data.get('high', [0])[-20:]) if len(data.get('high', [])) >= 20 else 0
            low_20 = min(data.get('low', [0])[-20:]) if len(data.get('low', [])) >= 20 else 0
            current_price = data.get('close', [0])[-1] if data.get('close') else 0
            volume = data.get('volume', [0])[-1] if data.get('volume') else 0
            avg_volume = np.mean(data.get('volume', [0])[-20:]) if len(data.get('volume', [])) >= 20 else volume
            
            # Breakout conditions
            bullish_breakout = (
                current_price > high_20 and  # Price breaks above 20-day high
                volume > avg_volume * 1.5  # Volume confirmation
            )
            
            bearish_breakout = (
                current_price < low_20 and  # Price breaks below 20-day low
                volume > avg_volume * 1.5  # Volume confirmation
            )
            
            if bullish_breakout:
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type=SignalType.BUY,
                    confidence=0.8,
                    strength=0.9,
                    entry_price=current_price,
                    stop_loss=high_20 * 0.98,
                    take_profit=current_price * 1.08,
                    position_size=self.config.max_position_size * 0.7,
                    strategy=StrategyType.BREAKOUT,
                    timestamp=datetime.now(),
                    metadata={
                        'high_20': high_20,
                        'low_20': low_20,
                        'volume': volume,
                        'avg_volume': avg_volume
                    }
                )
                signals.append(signal)
            
            elif bearish_breakout:
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type=SignalType.SELL,
                    confidence=0.8,
                    strength=0.9,
                    entry_price=current_price,
                    stop_loss=low_20 * 1.02,
                    take_profit=current_price * 0.92,
                    position_size=self.config.max_position_size * 0.7,
                    strategy=StrategyType.BREAKOUT,
                    timestamp=datetime.now(),
                    metadata={
                        'high_20': high_20,
                        'low_20': low_20,
                        'volume': volume,
                        'avg_volume': avg_volume
                    }
                )
                signals.append(signal)
        
        except Exception as e:
            self.logger.error(f"Error generating breakout signals for {symbol}: {e}")
        
        return signals
    
    async def _generate_arbitrage_signals(self, symbol: str, data: Dict[str, Any]) -> List[TradingSignal]:
        """Generate arbitrage signals"""
        signals = []
        
        try:
            # This would typically involve multiple exchanges or instruments
            # For now, implement a simple spread-based arbitrage
            
            # Calculate spread indicators
            bid = data.get('bid', 0)
            ask = data.get('ask', 0)
            spread = ask - bid if ask > 0 and bid > 0 else 0
            spread_pct = (spread / ask) * 100 if ask > 0 else 0
            
            # Arbitrage conditions (simplified)
            if spread_pct > 0.1:  # Spread > 0.1%
                # This is a simplified arbitrage signal
                # In practice, you'd compare prices across exchanges
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type=SignalType.BUY,  # Simplified
                    confidence=0.6,
                    strength=0.5,
                    entry_price=ask,
                    stop_loss=ask * 1.01,
                    take_profit=ask * 0.99,
                    position_size=self.config.max_position_size * 0.2,
                    strategy=StrategyType.ARBITRAGE,
                    timestamp=datetime.now(),
                    metadata={
                        'spread': spread,
                        'spread_pct': spread_pct,
                        'bid': bid,
                        'ask': ask
                    }
                )
                signals.append(signal)
        
        except Exception as e:
            self.logger.error(f"Error generating arbitrage signals for {symbol}: {e}")
        
        return signals
    
    async def _prepare_features(self, symbol: str, data: Dict[str, Any]) -> Optional[np.ndarray]:
        """Prepare features for ML models"""
        try:
            if not data.get('close') or len(data['close']) < self.config.lookback_period:
                return None
            
            # Get price data
            prices = np.array(data['close'][-self.config.lookback_period:])
            volumes = np.array(data.get('volume', [0])[-self.config.lookback_period:])
            
            # Calculate technical indicators
            features = []
            
            # Price features
            features.extend([
                prices[-1],  # Current price
                np.mean(prices),  # Mean price
                np.std(prices),  # Price volatility
                (prices[-1] - prices[0]) / prices[0],  # Total return
            ])
            
            # Moving averages
            for period in [5, 10, 20, 50]:
                if len(prices) >= period:
                    sma = np.mean(prices[-period:])
                    features.append(sma)
                    features.append((prices[-1] - sma) / sma)  # Price vs SMA
                else:
                    features.extend([0, 0])
            
            # Technical indicators
            rsi = self._calculate_rsi(prices)
            macd = self._calculate_macd(prices)
            bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(prices)
            
            features.extend([
                rsi,
                macd,
                (prices[-1] - bb_lower) / (bb_upper - bb_lower) if bb_upper != bb_lower else 0.5,
            ])
            
            # Volume features
            if len(volumes) > 0:
                features.extend([
                    volumes[-1],
                    np.mean(volumes),
                    np.std(volumes),
                ])
            else:
                features.extend([0, 0, 0])
            
            # Time features
            now = datetime.now()
            features.extend([
                now.hour / 24,  # Hour of day
                now.weekday() / 7,  # Day of week
            ])
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            self.logger.error(f"Error preparing features for {symbol}: {e}")
            return None
    
    async def _filter_signals(self, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Filter signals based on criteria"""
        filtered = []
        
        for signal in signals:
            # Check minimum confidence
            if signal.confidence < self.config.min_confidence:
                continue
            
            # Check position size limits
            if signal.position_size > self.config.max_position_size:
                signal.position_size = self.config.max_position_size
            
            # Check risk per trade
            if signal.position_size * self.config.risk_per_trade > self.config.risk_per_trade:
                signal.position_size = self.config.risk_per_trade / self.config.risk_per_trade
            
            filtered.append(signal)
        
        return filtered
    
    async def _rank_signals(self, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Rank signals by expected value"""
        for signal in signals:
            # Calculate expected value
            expected_value = self._calculate_expected_value(signal)
            signal.metadata['expected_value'] = expected_value
        
        # Sort by expected value (descending)
        return sorted(signals, key=lambda s: s.metadata.get('expected_value', 0), reverse=True)
    
    def _calculate_expected_value(self, signal: TradingSignal) -> float:
        """Calculate expected value of a signal"""
        # Simplified expected value calculation
        win_probability = signal.confidence
        win_amount = abs(signal.take_profit - signal.entry_price)
        loss_amount = abs(signal.entry_price - signal.stop_loss)
        
        expected_value = (win_probability * win_amount) - ((1 - win_probability) * loss_amount)
        return expected_value * signal.position_size
    
    def _calculate_stop_loss(self, data: Dict[str, Any], signal_type: SignalType) -> float:
        """Calculate stop loss price"""
        current_price = data.get('close', [0])[-1] if data.get('close') else 0
        
        if signal_type == SignalType.BUY:
            return current_price * 0.98  # 2% stop loss
        else:
            return current_price * 1.02  # 2% stop loss
    
    def _calculate_take_profit(self, data: Dict[str, Any], signal_type: SignalType) -> float:
        """Calculate take profit price"""
        current_price = data.get('close', [0])[-1] if data.get('close') else 0
        
        if signal_type == SignalType.BUY:
            return current_price * 1.05  # 5% take profit
        else:
            return current_price * 0.95  # 5% take profit
    
    def _calculate_position_size(self, confidence: float) -> float:
        """Calculate position size based on confidence"""
        base_size = self.config.max_position_size * 0.5
        confidence_multiplier = confidence
        return min(base_size * confidence_multiplier, self.config.max_position_size)
    
    # Technical indicator calculations
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI"""
        if len(prices) < period + 1:
            return 50
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> float:
        """Calculate MACD"""
        if len(prices) < slow:
            return 0
        
        ema_fast = self._calculate_ema(prices, fast)
        ema_slow = self._calculate_ema(prices, slow)
        return ema_fast - ema_slow
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """Calculate EMA"""
        if len(prices) < period:
            return prices[-1]
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def _calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate SMA"""
        if len(prices) < period:
            return prices[-1]
        return np.mean(prices[-period:])
    
    def _calculate_bollinger_bands(self, prices: List[float], period: int = 20, std_dev: float = 2) -> Tuple[float, float, float]:
        """Calculate Bollinger Bands"""
        if len(prices) < period:
            return prices[-1], prices[-1], prices[-1]
        
        sma = np.mean(prices[-period:])
        std = np.std(prices[-period:])
        
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        
        return upper, sma, lower
    
    async def _load_models(self) -> None:
        """Load trained models"""
        try:
            # Load ensemble models
            for i in range(self.config.model_ensemble_size):
                model_name = f"ensemble_{i}"
                
                # Try to load from registry
                model = await self.model_registry.load_model(model_name)
                if model:
                    self.models[model_name] = model
                    
                    # Load corresponding scaler
                    scaler = await self.model_registry.load_scaler(f"{model_name}_scaler")
                    if scaler:
                        self.scalers[f"{model_name}_scaler"] = scaler
            
            self.logger.info(f"Loaded {len(self.models)} models")
            
        except Exception as e:
            self.logger.error(f"Error loading models: {e}")
    
    async def _initialize_strategies(self) -> None:
        """Initialize trading strategies"""
        try:
            # Initialize strategy performance tracking
            for strategy in StrategyType:
                self.strategy_performance[strategy] = {
                    'total_signals': 0,
                    'successful_signals': 0,
                    'total_return': 0.0,
                    'last_updated': datetime.now()
                }
            
            self.logger.info("Strategies initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing strategies: {e}")
    
    async def _adaptive_learning_loop(self) -> None:
        """Adaptive learning loop"""
        while True:
            try:
                # Check if retraining is needed
                if datetime.now() - self.last_retrain > timedelta(hours=24):
                    await self._retrain_models()
                    self.last_retrain = datetime.now()
                
                # Update strategy weights based on performance
                await self._update_strategy_weights()
                
                await asyncio.sleep(3600)  # Check every hour
                
            except Exception as e:
                self.logger.error(f"Error in adaptive learning loop: {e}")
                await asyncio.sleep(3600)
    
    async def _retrain_models(self) -> None:
        """Retrain models with latest data"""
        try:
            self.is_learning = True
            self.logger.info("Starting model retraining...")
            
            # Get latest training data
            training_data = await self.market_data.get_training_data()
            
            # Prepare features and targets
            X, y = await self._prepare_training_data(training_data)
            
            if X is not None and y is not None:
                # Retrain ensemble models
                for i in range(self.config.model_ensemble_size):
                    model_name = f"ensemble_{i}"
                    
                    # Create and train model
                    model = self._create_model(i)
                    scaler = StandardScaler()
                    
                    X_scaled = scaler.fit_transform(X)
                    model.fit(X_scaled, y)
                    
                    # Save model and scaler
                    await self.model_registry.save_model(model_name, model)
                    await self.model_registry.save_scaler(f"{model_name}_scaler", scaler)
                    
                    self.models[model_name] = model
                    self.scalers[f"{model_name}_scaler"] = scaler
                
                self.logger.info("Model retraining completed")
            
        except Exception as e:
            self.logger.error(f"Error retraining models: {e}")
        finally:
            self.is_learning = False
    
    def _create_model(self, index: int):
        """Create a model for the ensemble"""
        if index % 3 == 0:
            return RandomForestRegressor(n_estimators=100, random_state=42)
        elif index % 3 == 1:
            return GradientBoostingRegressor(n_estimators=100, random_state=42)
        else:
            return MLPRegressor(hidden_layer_sizes=(100, 50), random_state=42)
    
    async def _prepare_training_data(self, data: Dict[str, Any]) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """Prepare training data for models"""
        try:
            # This is a simplified implementation
            # In practice, you'd have more sophisticated feature engineering
            features = []
            targets = []
            
            # Process each symbol's data
            for symbol, symbol_data in data.items():
                if 'close' in symbol_data and len(symbol_data['close']) > 50:
                    prices = symbol_data['close']
                    
                    # Create features and targets
                    for i in range(20, len(prices) - 5):
                        # Features (simplified)
                        feature_vector = [
                            prices[i],
                            np.mean(prices[i-20:i]),
                            np.std(prices[i-20:i]),
                            (prices[i] - prices[i-1]) / prices[i-1] if prices[i-1] != 0 else 0
                        ]
                        
                        # Target (future return)
                        future_return = (prices[i+5] - prices[i]) / prices[i] if prices[i] != 0 else 0
                        
                        features.append(feature_vector)
                        targets.append(1 if future_return > 0.01 else 0)  # Binary classification
            
            if features:
                return np.array(features), np.array(targets)
            else:
                return None, None
                
        except Exception as e:
            self.logger.error(f"Error preparing training data: {e}")
            return None, None
    
    async def _update_strategy_weights(self) -> None:
        """Update strategy weights based on performance"""
        try:
            # Calculate performance for each strategy
            for strategy, performance in self.strategy_performance.items():
                if performance['total_signals'] > 0:
                    success_rate = performance['successful_signals'] / performance['total_signals']
                    avg_return = performance['total_return'] / performance['total_signals']
                    
                    # Update weight based on performance
                    new_weight = success_rate * avg_return
                    self.config.strategy_weights[strategy] = max(0.1, min(0.8, new_weight))
            
            # Normalize weights
            total_weight = sum(self.config.strategy_weights.values())
            for strategy in self.config.strategy_weights:
                self.config.strategy_weights[strategy] /= total_weight
            
            self.logger.info(f"Updated strategy weights: {self.config.strategy_weights}")
            
        except Exception as e:
            self.logger.error(f"Error updating strategy weights: {e}")
    
    async def update_parameters(self, new_params: Dict[str, Any]) -> None:
        """Update decision engine parameters"""
        try:
            # Update configuration
            for key, value in new_params.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            
            self.logger.info(f"Updated parameters: {new_params}")
            
        except Exception as e:
            self.logger.error(f"Error updating parameters: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get decision engine status"""
        return {
            'models_loaded': len(self.models),
            'is_learning': self.is_learning,
            'last_retrain': self.last_retrain.isoformat(),
            'strategy_weights': self.config.strategy_weights,
            'strategy_performance': self.strategy_performance,
            'signals_generated': len(self.signal_history)
        }
