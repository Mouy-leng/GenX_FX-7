"""
Market Data Manager - Advanced market data handling
Handles real-time data ingestion, storage, and feature engineering
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import sqlite3
from pathlib import Path
import websockets
import aiohttp
import yfinance as yf

# Import statements moved to avoid circular imports


class DataSource(Enum):
    """Data sources"""
    YAHOO_FINANCE = "yahoo_finance"
    ALPHA_VANTAGE = "alpha_vantage"
    IEX_CLOUD = "iex_cloud"
    BINANCE = "binance"
    COINBASE = "coinbase"


class DataType(Enum):
    """Data types"""
    OHLCV = "ohlcv"
    TICK = "tick"
    ORDER_BOOK = "order_book"
    TRADES = "trades"
    NEWS = "news"
    SENTIMENT = "sentiment"


@dataclass
class MarketDataConfig:
    """Market data configuration"""
    symbols: List[str]
    data_sources: List[DataSource]
    update_frequency: int = 1  # seconds
    history_days: int = 365
    storage_path: str = "market_data"
    real_time_enabled: bool = True
    backup_enabled: bool = True


class MarketDataManager:
    """
    Advanced market data management system
    Handles real-time data ingestion, storage, and processing
    """
    
    def __init__(self, config: MarketDataConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.metrics = None
        
        # Data storage
        self.storage_path = Path(config.storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Database connection
        self.db_path = self.storage_path / "market_data.db"
        self.db_connection = None
        
        # Real-time data
        self.current_data = {}
        self.data_streams = {}
        self.is_streaming = False
        
        # Data processing
        self.feature_cache = {}
        self.last_update = {}
        
        # Background tasks
        self.is_running = False
        
    async def initialize(self, metrics=None) -> bool:
        """Initialize market data manager"""
        try:
            self.logger.info("Initializing market data manager...")
            
            # Set components if provided
            if metrics:
                self.metrics = metrics
            
            # Initialize database
            await self._initialize_database()
            
            # Load historical data
            await self._load_historical_data()
            
            # Start real-time data streams
            if self.config.real_time_enabled:
                await self._start_data_streams()
            
            # Start background tasks
            self.is_running = True
            asyncio.create_task(self._data_processing_loop())
            asyncio.create_task(self._backup_loop())
            
            self.logger.info("Market data manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize market data manager: {e}")
            return False
    
    async def get_latest_data(self) -> Dict[str, Any]:
        """Get latest market data for all symbols"""
        try:
            latest_data = {}
            
            for symbol in self.config.symbols:
                symbol_data = await self._get_symbol_data(symbol)
                if symbol_data:
                    latest_data[symbol] = symbol_data
            
            return latest_data
            
        except Exception as e:
            self.logger.error(f"Error getting latest data: {e}")
            return {}
    
    async def get_training_data(self) -> Dict[str, Any]:
        """Get training data for ML models"""
        try:
            training_data = {}
            
            for symbol in self.config.symbols:
                # Get historical data
                historical_data = await self._get_historical_data(symbol, days=365)
                
                if historical_data:
                    # Process data for training
                    processed_data = await self._process_training_data(historical_data)
                    training_data[symbol] = processed_data
            
            return training_data
            
        except Exception as e:
            self.logger.error(f"Error getting training data: {e}")
            return {}
    
    async def get_market_conditions(self) -> Dict[str, Any]:
        """Get current market conditions"""
        try:
            conditions = {}
            
            for symbol in self.config.symbols:
                symbol_data = await self._get_symbol_data(symbol)
                if symbol_data:
                    # Calculate market conditions
                    volatility = await self._calculate_volatility(symbol_data)
                    trend = await self._calculate_trend(symbol_data)
                    volume_profile = await self._calculate_volume_profile(symbol_data)
                    
                    conditions[symbol] = {
                        'volatility': volatility,
                        'trend': trend,
                        'volume_profile': volume_profile,
                        'timestamp': datetime.now()
                    }
            
            return conditions
            
        except Exception as e:
            self.logger.error(f"Error getting market conditions: {e}")
            return {}
    
    async def _initialize_database(self) -> None:
        """Initialize SQLite database"""
        try:
            self.db_connection = sqlite3.connect(self.db_path)
            cursor = self.db_connection.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ohlcv_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_conditions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    volatility REAL,
                    trend REAL,
                    volume_profile REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_symbol_timestamp ON ohlcv_data(symbol, timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_symbol_conditions ON market_conditions(symbol, timestamp)')
            
            self.db_connection.commit()
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    async def _load_historical_data(self) -> None:
        """Load historical data for all symbols"""
        try:
            for symbol in self.config.symbols:
                # Check if data exists
                existing_data = await self._get_historical_data(symbol, days=1)
                
                if not existing_data:
                    # Download historical data
                    await self._download_historical_data(symbol)
                
                self.logger.info(f"Historical data loaded for {symbol}")
            
        except Exception as e:
            self.logger.error(f"Error loading historical data: {e}")
    
    async def _download_historical_data(self, symbol: str) -> None:
        """Download historical data for a symbol"""
        try:
            # Use yfinance for historical data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f"{self.config.history_days}d")
            
            if data.empty:
                self.logger.warning(f"No historical data found for {symbol}")
                return
            
            # Store in database
            await self._store_historical_data(symbol, data)
            
            self.logger.info(f"Historical data downloaded for {symbol}")
            
        except Exception as e:
            self.logger.error(f"Error downloading historical data for {symbol}: {e}")
    
    async def _store_historical_data(self, symbol: str, data: pd.DataFrame) -> None:
        """Store historical data in database"""
        try:
            cursor = self.db_connection.cursor()
            
            for timestamp, row in data.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO ohlcv_data 
                    (symbol, timestamp, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    symbol,
                    timestamp.isoformat(),
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    row['Volume']
                ))
            
            self.db_connection.commit()
            
        except Exception as e:
            self.logger.error(f"Error storing historical data for {symbol}: {e}")
    
    async def _get_historical_data(self, symbol: str, days: int = 30) -> Optional[pd.DataFrame]:
        """Get historical data for a symbol"""
        try:
            cursor = self.db_connection.cursor()
            
            # Calculate start date
            start_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                SELECT timestamp, open, high, low, close, volume
                FROM ohlcv_data
                WHERE symbol = ? AND timestamp >= ?
                ORDER BY timestamp
            ''', (symbol, start_date.isoformat()))
            
            rows = cursor.fetchall()
            
            if not rows:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error getting historical data for {symbol}: {e}")
            return None
    
    async def _get_symbol_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get latest data for a symbol"""
        try:
            # Get from real-time data if available
            if symbol in self.current_data:
                return self.current_data[symbol]
            
            # Get from database
            historical_data = await self._get_historical_data(symbol, days=1)
            if historical_data is not None and not historical_data.empty:
                latest_row = historical_data.iloc[-1]
                return {
                    'symbol': symbol,
                    'open': latest_row['open'],
                    'high': latest_row['high'],
                    'low': latest_row['low'],
                    'close': latest_row['close'],
                    'volume': latest_row['volume'],
                    'timestamp': latest_row.name
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting symbol data for {symbol}: {e}")
            return None
    
    async def _start_data_streams(self) -> None:
        """Start real-time data streams"""
        try:
            self.is_streaming = True
            
            # Start WebSocket connections for each symbol
            for symbol in self.config.symbols:
                asyncio.create_task(self._start_symbol_stream(symbol))
            
            self.logger.info("Real-time data streams started")
            
        except Exception as e:
            self.logger.error(f"Error starting data streams: {e}")
    
    async def _start_symbol_stream(self, symbol: str) -> None:
        """Start real-time data stream for a symbol"""
        try:
            # This is a simplified implementation
            # In practice, you'd connect to real WebSocket feeds
            
            while self.is_streaming:
                # Simulate real-time data updates
                await self._update_real_time_data(symbol)
                await asyncio.sleep(self.config.update_frequency)
                
        except Exception as e:
            self.logger.error(f"Error in symbol stream for {symbol}: {e}")
    
    async def _update_real_time_data(self, symbol: str) -> None:
        """Update real-time data for a symbol"""
        try:
            # Get latest data from API
            latest_data = await self._fetch_latest_data(symbol)
            
            if latest_data:
                # Update current data
                self.current_data[symbol] = latest_data
                
                # Store in database
                await self._store_real_time_data(symbol, latest_data)
                
                # Update last update time
                self.last_update[symbol] = datetime.now()
                
        except Exception as e:
            self.logger.error(f"Error updating real-time data for {symbol}: {e}")
    
    async def _fetch_latest_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch latest data from API"""
        try:
            # Use yfinance for real-time data
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if 'regularMarketPrice' in info:
                return {
                    'symbol': symbol,
                    'open': info.get('open', 0),
                    'high': info.get('dayHigh', 0),
                    'low': info.get('dayLow', 0),
                    'close': info.get('regularMarketPrice', 0),
                    'volume': info.get('volume', 0),
                    'timestamp': datetime.now()
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error fetching latest data for {symbol}: {e}")
            return None
    
    async def _store_real_time_data(self, symbol: str, data: Dict[str, Any]) -> None:
        """Store real-time data in database"""
        try:
            cursor = self.db_connection.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO ohlcv_data 
                (symbol, timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                data['timestamp'].isoformat(),
                data['open'],
                data['high'],
                data['low'],
                data['close'],
                data['volume']
            ))
            
            self.db_connection.commit()
            
        except Exception as e:
            self.logger.error(f"Error storing real-time data for {symbol}: {e}")
    
    async def _process_training_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Process data for ML training"""
        try:
            processed_data = {
                'close': data['close'].tolist(),
                'high': data['high'].tolist(),
                'low': data['low'].tolist(),
                'open': data['open'].tolist(),
                'volume': data['volume'].tolist(),
                'timestamp': data.index.tolist()
            }
            
            # Add technical indicators
            processed_data['sma_20'] = data['close'].rolling(window=20).mean().tolist()
            processed_data['sma_50'] = data['close'].rolling(window=50).mean().tolist()
            processed_data['rsi'] = self._calculate_rsi_series(data['close']).tolist()
            processed_data['macd'] = self._calculate_macd_series(data['close']).tolist()
            
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error processing training data: {e}")
            return {}
    
    def _calculate_rsi_series(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI series"""
        try:
            deltas = prices.diff()
            gains = deltas.where(deltas > 0, 0)
            losses = -deltas.where(deltas < 0, 0)
            
            avg_gains = gains.rolling(window=period).mean()
            avg_losses = losses.rolling(window=period).mean()
            
            rs = avg_gains / avg_losses
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.fillna(50)
            
        except Exception as e:
            self.logger.error(f"Error calculating RSI: {e}")
            return pd.Series([50] * len(prices), index=prices.index)
    
    def _calculate_macd_series(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
        """Calculate MACD series"""
        try:
            ema_fast = prices.ewm(span=fast).mean()
            ema_slow = prices.ewm(span=slow).mean()
            macd = ema_fast - ema_slow
            
            return macd
            
        except Exception as e:
            self.logger.error(f"Error calculating MACD: {e}")
            return pd.Series([0] * len(prices), index=prices.index)
    
    async def _calculate_volatility(self, data: Dict[str, Any]) -> float:
        """Calculate volatility for market conditions"""
        try:
            # Simplified volatility calculation
            close_prices = data.get('close', [])
            if len(close_prices) < 2:
                return 0.0
            
            returns = np.diff(close_prices) / close_prices[:-1]
            volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
            
            return float(volatility)
            
        except Exception as e:
            self.logger.error(f"Error calculating volatility: {e}")
            return 0.0
    
    async def _calculate_trend(self, data: Dict[str, Any]) -> float:
        """Calculate trend for market conditions"""
        try:
            close_prices = data.get('close', [])
            if len(close_prices) < 2:
                return 0.0
            
            # Simple trend calculation
            trend = (close_prices[-1] - close_prices[0]) / close_prices[0]
            return float(trend)
            
        except Exception as e:
            self.logger.error(f"Error calculating trend: {e}")
            return 0.0
    
    async def _calculate_volume_profile(self, data: Dict[str, Any]) -> float:
        """Calculate volume profile for market conditions"""
        try:
            volumes = data.get('volume', [])
            if not volumes:
                return 0.0
            
            # Calculate volume profile
            avg_volume = np.mean(volumes)
            current_volume = volumes[-1] if volumes else 0
            
            volume_profile = current_volume / avg_volume if avg_volume > 0 else 1.0
            return float(volume_profile)
            
        except Exception as e:
            self.logger.error(f"Error calculating volume profile: {e}")
            return 1.0
    
    async def _data_processing_loop(self) -> None:
        """Background data processing loop"""
        while self.is_running:
            try:
                # Process market conditions
                await self._update_market_conditions()
                
                # Clean up old data
                await self._cleanup_old_data()
                
                await asyncio.sleep(300)  # Run every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in data processing loop: {e}")
                await asyncio.sleep(300)
    
    async def _update_market_conditions(self) -> None:
        """Update market conditions for all symbols"""
        try:
            for symbol in self.config.symbols:
                symbol_data = await self._get_symbol_data(symbol)
                if symbol_data:
                    # Calculate conditions
                    volatility = await self._calculate_volatility(symbol_data)
                    trend = await self._calculate_trend(symbol_data)
                    volume_profile = await self._calculate_volume_profile(symbol_data)
                    
                    # Store conditions
                    await self._store_market_conditions(symbol, volatility, trend, volume_profile)
                    
        except Exception as e:
            self.logger.error(f"Error updating market conditions: {e}")
    
    async def _store_market_conditions(self, symbol: str, volatility: float, trend: float, volume_profile: float) -> None:
        """Store market conditions in database"""
        try:
            cursor = self.db_connection.cursor()
            
            cursor.execute('''
                INSERT INTO market_conditions 
                (symbol, timestamp, volatility, trend, volume_profile)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                symbol,
                datetime.now().isoformat(),
                volatility,
                trend,
                volume_profile
            ))
            
            self.db_connection.commit()
            
        except Exception as e:
            self.logger.error(f"Error storing market conditions for {symbol}: {e}")
    
    async def _cleanup_old_data(self) -> None:
        """Clean up old data to manage storage"""
        try:
            cursor = self.db_connection.cursor()
            
            # Keep only last 365 days of data
            cutoff_date = datetime.now() - timedelta(days=365)
            
            cursor.execute('''
                DELETE FROM ohlcv_data 
                WHERE timestamp < ?
            ''', (cutoff_date.isoformat(),))
            
            cursor.execute('''
                DELETE FROM market_conditions 
                WHERE timestamp < ?
            ''', (cutoff_date.isoformat(),))
            
            self.db_connection.commit()
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old data: {e}")
    
    async def _backup_loop(self) -> None:
        """Periodic backup of data"""
        while self.is_running:
            try:
                if self.config.backup_enabled:
                    await self._backup_data()
                
                await asyncio.sleep(3600)  # Backup every hour
                
            except Exception as e:
                self.logger.error(f"Error in backup loop: {e}")
                await asyncio.sleep(3600)
    
    async def _backup_data(self) -> None:
        """Backup market data"""
        try:
            backup_path = self.storage_path / "backups"
            backup_path.mkdir(exist_ok=True)
            
            # Create backup file
            backup_file = backup_path / f"market_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            # Copy database
            import shutil
            shutil.copy2(self.db_path, backup_file)
            
            self.logger.info(f"Data backup created: {backup_file}")
            
        except Exception as e:
            self.logger.error(f"Error backing up data: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown market data manager"""
        try:
            self.is_running = False
            self.is_streaming = False
            
            # Close database connection
            if self.db_connection:
                self.db_connection.close()
            
            self.logger.info("Market data manager shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get market data manager status"""
        return {
            'is_streaming': self.is_streaming,
            'symbols_count': len(self.config.symbols),
            'current_data_count': len(self.current_data),
            'last_updates': {
                symbol: last_update.isoformat() 
                for symbol, last_update in self.last_update.items()
            },
            'config': self.config.__dict__
        }
