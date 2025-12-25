"""
GenX-FX Feature Store
Feature engineering and storage for autonomous trading
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class FeatureStore:
    """Feature store for managing trading features and indicators"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.features = {}
        self.metadata = {}
    
    def add_feature(self, name: str, data: Any, metadata: Optional[Dict] = None):
        """Add a feature to the store"""
        self.features[name] = data
        if metadata:
            self.metadata[name] = metadata
    
    def get_feature(self, name: str) -> Any:
        """Retrieve a feature by name"""
        return self.features.get(name)
    
    def list_features(self) -> List[str]:
        """List all available features"""
        return list(self.features.keys())
    
    def compute_technical_indicators(self, price_data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Compute basic technical indicators"""
        indicators = {}
        
        if 'close' in price_data.columns:
            # Simple moving averages
            indicators['sma_20'] = price_data['close'].rolling(window=20).mean()
            indicators['sma_50'] = price_data['close'].rolling(window=50).mean()
            
            # RSI (simplified)
            delta = price_data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            indicators['rsi'] = 100 - (100 / (1 + rs))
        
        return indicators
    
    def update_features(self, market_data: Dict[str, Any]):
        """Update features with new market data"""
        if isinstance(market_data, dict) and 'price_data' in market_data:
            indicators = self.compute_technical_indicators(market_data['price_data'])
            self.features.update(indicators)