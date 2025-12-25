"""
GenX-FX Demo Trading Application
Simple demo app to test the Python management system
"""

import time
import logging
import signal
import sys
from datetime import datetime
import random


class DemoTradingSystem:
    """Demo trading system for testing the management system"""
    
    def __init__(self):
        self.running = False
        self.trades_executed = 0
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('DemoTrading')
        
    def start_trading(self):
        """Start the demo trading system"""
        self.logger.info("🚀 GenX-FX Demo Trading System Starting...")
        self.running = True
        
        try:
            while self.running:
                # Simulate trading activity
                self.simulate_trading()
                time.sleep(5)  # Wait 5 seconds between activities
                
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
            self.stop_trading()
        except Exception as e:
            self.logger.error(f"Trading error: {e}")
            self.stop_trading()
    
    def simulate_trading(self):
        """Simulate trading activities"""
        activities = [
            "Analyzing market data...",
            "Checking risk parameters...",
            "Monitoring positions...",
            "Updating portfolio metrics...",
            "Scanning for opportunities..."
        ]
        
        activity = random.choice(activities)
        self.logger.info(f"📊 {activity}")
        
        # Occasionally simulate a trade
        if random.random() < 0.3:  # 30% chance
            self.trades_executed += 1
            profit = random.uniform(-100, 200)
            self.logger.info(f"💰 Trade #{self.trades_executed} executed - P&L: ${profit:.2f}")
    
    def stop_trading(self):
        """Stop the trading system"""
        self.logger.info("🛑 Stopping GenX-FX Demo Trading System...")
        self.running = False
        self.logger.info(f"📈 Session summary: {self.trades_executed} trades executed")


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"\\nReceived signal {signum}, shutting down gracefully...")
    sys.exit(0)


def main():
    """Main entry point"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("  GenX-FX Demo Trading System")
    print("  A6-9V Organization")
    print("=" * 60)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  Status: Demo Mode")
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    
    # Start the demo trading system
    trading_system = DemoTradingSystem()
    trading_system.start_trading()


if __name__ == "__main__":
    main()