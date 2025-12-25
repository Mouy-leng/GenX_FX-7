"""
GenX-FX Data Validator
Data validation and quality checks for autonomous trading
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta


class DataValidator:
    """Data validator for market data quality checks"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.validation_rules = self._default_validation_rules()
    
    def _default_validation_rules(self) -> Dict[str, Any]:
        """Default validation rules for market data"""
        return {
            'required_columns': ['open', 'high', 'low', 'close', 'volume'],
            'price_range_check': True,
            'volume_check': True,
            'timestamp_check': True,
            'null_check': True,
            'ohlc_consistency': True
        }
    
    def validate_market_data(self, data: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate market data DataFrame"""
        errors = []
        
        # Check required columns
        if self.validation_rules.get('required_columns'):
            missing_cols = [col for col in self.validation_rules['required_columns'] 
                          if col not in data.columns]
            if missing_cols:
                errors.append(f"Missing required columns: {missing_cols}")
        
        # Check for null values
        if self.validation_rules.get('null_check', True):
            null_counts = data.isnull().sum()
            if null_counts.any():
                errors.append(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
        
        # Check OHLC consistency
        if self.validation_rules.get('ohlc_consistency', True):
            if all(col in data.columns for col in ['open', 'high', 'low', 'close']):
                # High should be >= Open, Low, Close
                high_violations = (data['high'] < data[['open', 'low', 'close']].max(axis=1)).sum()
                # Low should be <= Open, High, Close  
                low_violations = (data['low'] > data[['open', 'high', 'close']].min(axis=1)).sum()
                
                if high_violations > 0:
                    errors.append(f"High price violations: {high_violations} rows")
                if low_violations > 0:
                    errors.append(f"Low price violations: {low_violations} rows")
        
        # Check price ranges
        if self.validation_rules.get('price_range_check', True):
            price_cols = ['open', 'high', 'low', 'close']
            for col in price_cols:
                if col in data.columns:
                    if (data[col] <= 0).any():
                        errors.append(f"Non-positive prices found in {col}")
                    if (data[col] > 1000000).any():  # Arbitrary large value check
                        errors.append(f"Extremely high prices found in {col}")
        
        # Check volume
        if self.validation_rules.get('volume_check', True):
            if 'volume' in data.columns:
                if (data['volume'] < 0).any():
                    errors.append("Negative volume values found")
        
        return len(errors) == 0, errors
    
    def validate_features(self, features: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate feature data"""
        errors = []
        
        for name, feature_data in features.items():
            if feature_data is None:
                errors.append(f"Feature '{name}' is None")
                continue
            
            if isinstance(feature_data, pd.Series):
                if feature_data.empty:
                    errors.append(f"Feature '{name}' is empty")
                if feature_data.isnull().all():
                    errors.append(f"Feature '{name}' contains only null values")
        
        return len(errors) == 0, errors
    
    def check_data_freshness(self, data: pd.DataFrame, 
                           max_age_minutes: int = 60) -> Tuple[bool, str]:
        """Check if data is fresh enough"""
        if data.empty:
            return False, "Data is empty"
        
        if 'timestamp' not in data.columns:
            return True, "No timestamp column to check freshness"
        
        latest_timestamp = pd.to_datetime(data['timestamp']).max()
        current_time = datetime.now()
        
        if pd.isna(latest_timestamp):
            return False, "Latest timestamp is null"
        
        age_minutes = (current_time - latest_timestamp).total_seconds() / 60
        
        if age_minutes > max_age_minutes:
            return False, f"Data is {age_minutes:.1f} minutes old (max: {max_age_minutes})"
        
        return True, f"Data is fresh ({age_minutes:.1f} minutes old)"