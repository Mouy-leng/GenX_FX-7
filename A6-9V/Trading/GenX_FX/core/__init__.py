"""
GenX-FX Autonomous Trading System Core
Advanced self-managing trading system with AI/ML capabilities
"""

__version__ = "1.0.0"
__author__ = "A6-9V"

from .autonomous_agent import AutonomousAgent
from .self_manager import SelfManager
from .decision_engine import DecisionEngine
from .risk_manager import RiskManager

__all__ = [
    "AutonomousAgent",
    "SelfManager", 
    "DecisionEngine",
    "RiskManager"
]
