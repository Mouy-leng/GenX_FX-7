"""
Broker Adapter - Advanced broker integration
Handles multiple broker connections and order execution
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import aiohttp
import websockets

# Import statements moved to avoid circular imports


class BrokerType(Enum):
    """Broker types"""
    ALPACA = "alpaca"
    INTERACTIVE_BROKERS = "interactive_brokers"
    BINANCE = "binance"
    COINBASE = "coinbase"
    META_TRADER = "meta_trader"


class OrderType(Enum):
    """Order types"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderSide(Enum):
    """Order sides"""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    """Order status"""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    PARTIALLY_FILLED = "partially_filled"


@dataclass
class Order:
    """Trading order"""
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0.0
    average_price: float = 0.0
    created_at: datetime = None
    updated_at: datetime = None
    metadata: Dict[str, Any] = None


@dataclass
class Position:
    """Trading position"""
    symbol: str
    side: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    timestamp: datetime


@dataclass
class BrokerConfig:
    """Broker configuration"""
    broker_type: BrokerType
    api_key: str
    secret_key: str
    base_url: str
    sandbox: bool = True
    timeout: int = 30
    retry_attempts: int = 3


class BrokerAdapter:
    """
    Advanced broker adapter supporting multiple brokers
    """
    
    def __init__(self, config: BrokerConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.metrics = None
        
        # Connection management
        self.session = None
        self.websocket = None
        self.is_connected = False
        
        # Order management
        self.orders = {}
        self.positions = {}
        
        # Rate limiting
        self.rate_limits = {}
        self.last_request = {}
        
    async def initialize(self, metrics=None) -> bool:
        """Initialize broker connection"""
        try:
            self.logger.info(f"Initializing broker: {self.config.broker_type.value}")
            
            # Set components if provided
            if metrics:
                self.metrics = metrics
            
            # Create HTTP session
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
            
            # Initialize broker-specific connection
            if self.config.broker_type == BrokerType.ALPACA:
                await self._initialize_alpaca()
            elif self.config.broker_type == BrokerType.BINANCE:
                await self._initialize_binance()
            elif self.config.broker_type == BrokerType.COINBASE:
                await self._initialize_coinbase()
            else:
                self.logger.warning(f"Unsupported broker type: {self.config.broker_type.value}")
                return False
            
            self.is_connected = True
            self.logger.info("Broker connection established")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize broker: {e}")
            return False
    
    async def execute_trade(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a trading signal"""
        try:
            # Create order from signal
            order = await self._create_order_from_signal(signal)
            
            if not order:
                return {'success': False, 'error': 'Failed to create order'}
            
            # Execute order
            result = await self._execute_order(order)
            
            if result['success']:
                # Update order tracking
                self.orders[order.order_id] = order
                
                # Record metrics
                await self.metrics.record_trade_execution(order, result)
                
                self.logger.info(f"Trade executed: {order.order_id}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing trade: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_positions(self) -> Dict[str, Position]:
        """Get current positions"""
        try:
            if self.config.broker_type == BrokerType.ALPACA:
                return await self._get_alpaca_positions()
            elif self.config.broker_type == BrokerType.BINANCE:
                return await self._get_binance_positions()
            elif self.config.broker_type == BrokerType.COINBASE:
                return await self._get_coinbase_positions()
            else:
                return {}
                
        except Exception as e:
            self.logger.error(f"Error getting positions: {e}")
            return {}
    
    async def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol"""
        try:
            if self.config.broker_type == BrokerType.ALPACA:
                return await self._get_alpaca_price(symbol)
            elif self.config.broker_type == BrokerType.BINANCE:
                return await self._get_binance_price(symbol)
            elif self.config.broker_type == BrokerType.COINBASE:
                return await self._get_coinbase_price(symbol)
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting current price for {symbol}: {e}")
            return None
    
    async def close_all_positions(self) -> Dict[str, Any]:
        """Close all positions"""
        try:
            positions = await self.get_positions()
            results = {}
            
            for symbol, position in positions.items():
                # Create close order
                close_order = Order(
                    order_id=f"close_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    symbol=symbol,
                    side=OrderSide.SELL if position.side == 'long' else OrderSide.BUY,
                    order_type=OrderType.MARKET,
                    quantity=position.quantity
                )
                
                # Execute close order
                result = await self._execute_order(close_order)
                results[symbol] = result
                
                if result['success']:
                    self.logger.info(f"Position closed: {symbol}")
            
            return {'success': True, 'results': results}
            
        except Exception as e:
            self.logger.error(f"Error closing all positions: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _create_order_from_signal(self, signal: Dict[str, Any]) -> Optional[Order]:
        """Create order from trading signal"""
        try:
            order_id = f"order_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Determine order side
            side = OrderSide.BUY if signal.get('signal_type') == 'buy' else OrderSide.SELL
            
            # Determine order type
            order_type = OrderType.MARKET  # Default to market order
            
            # Create order
            order = Order(
                order_id=order_id,
                symbol=signal.get('symbol', ''),
                side=side,
                order_type=order_type,
                quantity=signal.get('position_size', 0),
                price=signal.get('entry_price'),
                stop_price=signal.get('stop_loss'),
                created_at=datetime.now(),
                metadata=signal
            )
            
            return order
            
        except Exception as e:
            self.logger.error(f"Error creating order from signal: {e}")
            return None
    
    async def _execute_order(self, order: Order) -> Dict[str, Any]:
        """Execute an order"""
        try:
            if self.config.broker_type == BrokerType.ALPACA:
                return await self._execute_alpaca_order(order)
            elif self.config.broker_type == BrokerType.BINANCE:
                return await self._execute_binance_order(order)
            elif self.config.broker_type == BrokerType.COINBASE:
                return await self._execute_coinbase_order(order)
            else:
                return {'success': False, 'error': 'Unsupported broker type'}
                
        except Exception as e:
            self.logger.error(f"Error executing order: {e}")
            return {'success': False, 'error': str(e)}
    
    # Alpaca-specific methods
    async def _initialize_alpaca(self) -> None:
        """Initialize Alpaca connection"""
        try:
            # Set up authentication headers
            self.headers = {
                'APCA-API-KEY-ID': self.config.api_key,
                'APCA-API-SECRET-KEY': self.config.secret_key
            }
            
            # Test connection
            url = f"{self.config.base_url}/v2/account"
            async with self.session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    self.logger.info("Alpaca connection verified")
                else:
                    raise Exception(f"Alpaca connection failed: {response.status}")
                    
        except Exception as e:
            self.logger.error(f"Error initializing Alpaca: {e}")
            raise
    
    async def _execute_alpaca_order(self, order: Order) -> Dict[str, Any]:
        """Execute order on Alpaca"""
        try:
            url = f"{self.config.base_url}/v2/orders"
            
            order_data = {
                'symbol': order.symbol,
                'qty': str(order.quantity),
                'side': order.side.value,
                'type': order.order_type.value,
                'time_in_force': 'day'
            }
            
            if order.price:
                order_data['limit_price'] = str(order.price)
            
            if order.stop_price:
                order_data['stop_price'] = str(order.stop_price)
            
            async with self.session.post(url, headers=self.headers, json=order_data) as response:
                if response.status == 201:
                    result = await response.json()
                    order.order_id = result['id']
                    order.status = OrderStatus.PENDING
                    return {'success': True, 'order_id': result['id']}
                else:
                    error_text = await response.text()
                    return {'success': False, 'error': f"Alpaca error: {error_text}"}
                    
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _get_alpaca_positions(self) -> Dict[str, Position]:
        """Get positions from Alpaca"""
        try:
            url = f"{self.config.base_url}/v2/positions"
            
            async with self.session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    positions_data = await response.json()
                    positions = {}
                    
                    for pos_data in positions_data:
                        symbol = pos_data['symbol']
                        position = Position(
                            symbol=symbol,
                            side='long' if float(pos_data['qty']) > 0 else 'short',
                            quantity=abs(float(pos_data['qty'])),
                            average_price=float(pos_data['avg_entry_price']),
                            current_price=float(pos_data['current_price']),
                            unrealized_pnl=float(pos_data['unrealized_pl']),
                            realized_pnl=float(pos_data['realized_pl']),
                            timestamp=datetime.now()
                        )
                        positions[symbol] = position
                    
                    return positions
                else:
                    return {}
                    
        except Exception as e:
            self.logger.error(f"Error getting Alpaca positions: {e}")
            return {}
    
    async def _get_alpaca_price(self, symbol: str) -> Optional[float]:
        """Get current price from Alpaca"""
        try:
            url = f"{self.config.base_url}/v2/latest/trades"
            params = {'symbols': symbol}
            
            async with self.session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and symbol in data:
                        return float(data[symbol]['p'])
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting Alpaca price for {symbol}: {e}")
            return None
    
    # Binance-specific methods
    async def _initialize_binance(self) -> None:
        """Initialize Binance connection"""
        try:
            # Set up authentication
            self.api_key = self.config.api_key
            self.secret_key = self.config.secret_key
            
            # Test connection
            url = f"{self.config.base_url}/api/v3/ping"
            async with self.session.get(url) as response:
                if response.status == 200:
                    self.logger.info("Binance connection verified")
                else:
                    raise Exception(f"Binance connection failed: {response.status}")
                    
        except Exception as e:
            self.logger.error(f"Error initializing Binance: {e}")
            raise
    
    async def _execute_binance_order(self, order: Order) -> Dict[str, Any]:
        """Execute order on Binance"""
        try:
            # This is a simplified implementation
            # In practice, you'd implement proper Binance API integration
            self.logger.info(f"Binance order execution not implemented: {order.symbol}")
            return {'success': False, 'error': 'Binance integration not implemented'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _get_binance_positions(self) -> Dict[str, Position]:
        """Get positions from Binance"""
        try:
            # This is a simplified implementation
            # In practice, you'd implement proper Binance API integration
            return {}
            
        except Exception as e:
            self.logger.error(f"Error getting Binance positions: {e}")
            return {}
    
    async def _get_binance_price(self, symbol: str) -> Optional[float]:
        """Get current price from Binance"""
        try:
            url = f"{self.config.base_url}/api/v3/ticker/price"
            params = {'symbol': symbol}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data['price'])
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting Binance price for {symbol}: {e}")
            return None
    
    # Coinbase-specific methods
    async def _initialize_coinbase(self) -> None:
        """Initialize Coinbase connection"""
        try:
            # Set up authentication
            self.api_key = self.config.api_key
            self.secret_key = self.config.secret_key
            
            # Test connection
            url = f"{self.config.base_url}/v2/time"
            async with self.session.get(url) as response:
                if response.status == 200:
                    self.logger.info("Coinbase connection verified")
                else:
                    raise Exception(f"Coinbase connection failed: {response.status}")
                    
        except Exception as e:
            self.logger.error(f"Error initializing Coinbase: {e}")
            raise
    
    async def _execute_coinbase_order(self, order: Order) -> Dict[str, Any]:
        """Execute order on Coinbase"""
        try:
            # This is a simplified implementation
            # In practice, you'd implement proper Coinbase API integration
            self.logger.info(f"Coinbase order execution not implemented: {order.symbol}")
            return {'success': False, 'error': 'Coinbase integration not implemented'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _get_coinbase_positions(self) -> Dict[str, Position]:
        """Get positions from Coinbase"""
        try:
            # This is a simplified implementation
            # In practice, you'd implement proper Coinbase API integration
            return {}
            
        except Exception as e:
            self.logger.error(f"Error getting Coinbase positions: {e}")
            return {}
    
    async def _get_coinbase_price(self, symbol: str) -> Optional[float]:
        """Get current price from Coinbase"""
        try:
            url = f"{self.config.base_url}/v2/prices/{symbol}/spot"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data['data']['amount'])
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting Coinbase price for {symbol}: {e}")
            return None
    
    async def shutdown(self) -> None:
        """Shutdown broker connection"""
        try:
            if self.session:
                await self.session.close()
            
            if self.websocket:
                await self.websocket.close()
            
            self.is_connected = False
            self.logger.info("Broker connection closed")
            
        except Exception as e:
            self.logger.error(f"Error during broker shutdown: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get broker adapter status"""
        return {
            'is_connected': self.is_connected,
            'broker_type': self.config.broker_type.value,
            'orders_count': len(self.orders),
            'positions_count': len(self.positions),
            'config': {
                'broker_type': self.config.broker_type.value,
                'sandbox': self.config.sandbox,
                'timeout': self.config.timeout
            }
        }
