# GenX-FX Setup Guide

## 🚀 Complete Setup Instructions

This guide will walk you through setting up the GenX-FX Autonomous Trading System from scratch.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.9 or higher
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: At least 10GB free space
- **Internet**: Stable internet connection for real-time data

### Required Software
- **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Code Editor**: VS Code, PyCharm, or your preferred editor

## 🔧 Installation Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/genx-fx.git
cd genx-fx
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv genx_env

# Activate virtual environment
# Windows:
genx_env\Scripts\activate
# macOS/Linux:
source genx_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Set Up Configuration
```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Edit configuration file
nano config/config.yaml  # or use your preferred editor
```

## ⚙️ Configuration

### Basic Configuration
Edit `config/config.yaml`:

```yaml
# System Configuration
system:
  name: "GenX-FX Trading System"
  version: "1.0.0"
  environment: "development"  # development, staging, production
  debug: true

# Trading Configuration
trading:
  symbols: ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
  strategies:
    - momentum
    - mean_reversion
    - breakout
    - arbitrage
    - ml_prediction
  min_confidence: 0.6
  max_signals_per_cycle: 10
  trading_hours:
    start: "09:30"
    end: "16:00"
    timezone: "US/Eastern"

# Risk Management
risk_management:
  max_position_size: 0.1  # 10% of portfolio
  max_daily_loss: 0.05   # 5% daily loss limit
  max_drawdown: 0.15     # 15% max drawdown
  max_correlation: 0.7   # Max correlation between positions
  max_volatility: 0.3    # Max portfolio volatility
  max_leverage: 2.0      # Max leverage
  max_positions: 10      # Max number of positions
  emergency_stop_loss: 0.2  # Emergency stop at 20% loss

# Broker Configuration
broker:
  type: "alpaca"  # alpaca, binance, coinbase, interactive_brokers
  api_key: "your_api_key_here"
  secret_key: "your_secret_key_here"
  base_url: "https://paper-api.alpaca.markets"
  sandbox: true
  timeout: 30
  retry_attempts: 3

# Data Sources
data_sources:
  primary: "yahoo_finance"
  backup: "alpha_vantage"
  real_time: true
  update_frequency: 1  # seconds
  history_days: 365

# Machine Learning
ml:
  model_types: ["classification", "regression", "ensemble"]
  ensemble_size: 5
  retrain_frequency: 24  # hours
  validation_threshold: 0.7
  deployment_threshold: 0.8

# Monitoring
monitoring:
  metrics_enabled: true
  alerts_enabled: true
  dashboard_enabled: true
  log_level: "INFO"
  retention_days: 30
```

### Environment Variables
Create a `.env` file in the root directory:

```bash
# Broker API Keys
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Database
DATABASE_URL=sqlite:///genx_trading.db

# Monitoring
PROMETHEUS_ENDPOINT=http://localhost:9090
GRAFANA_ENDPOINT=http://localhost:3000

# Email Alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ALERT_RECIPIENTS=alerts@yourdomain.com

# Security
SECRET_KEY=your_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here
```

## 🏦 Broker Setup

### Alpaca (Recommended for US Markets)
1. **Create Account**: [Alpaca Trading](https://alpaca.markets/)
2. **Get API Keys**: Go to Account → API Keys
3. **Paper Trading**: Use paper trading for testing
4. **Configure**: Update broker settings in config

### Binance (Crypto Trading)
1. **Create Account**: [Binance](https://www.binance.com/)
2. **Enable API**: Go to API Management
3. **Create API Key**: Generate new API key
4. **Set Permissions**: Enable trading permissions

### Interactive Brokers
1. **Create Account**: [Interactive Brokers](https://www.interactivebrokers.com/)
2. **Download TWS**: Install Trader Workstation
3. **Enable API**: Configure API settings
4. **Connect**: Use IB Gateway for API access

## 📊 Data Sources Setup

### Yahoo Finance (Free)
- No setup required
- Limited to basic market data
- Good for testing and development

### Alpha Vantage (Free Tier Available)
1. **Sign Up**: [Alpha Vantage](https://www.alphavantage.co/)
2. **Get API Key**: Free tier available
3. **Configure**: Add API key to config

### IEX Cloud (Free Tier Available)
1. **Sign Up**: [IEX Cloud](https://iexcloud.io/)
2. **Get API Key**: Free tier available
3. **Configure**: Add API key to config

## 🧠 Machine Learning Setup

### Model Training
```bash
# Train initial models
python -m ml.train_models --config config/ml_config.yaml

# Validate models
python -m ml.validate_models --config config/ml_config.yaml

# Deploy models
python -m ml.deploy_models --config config/ml_config.yaml
```

### Feature Engineering
```bash
# Generate features
python -m data.generate_features --symbols AAPL,GOOGL,MSFT

# Validate features
python -m data.validate_features --config config/data_config.yaml
```

## 🔍 Monitoring Setup

### Prometheus (Optional)
```bash
# Install Prometheus
docker run -d -p 9090:9090 prom/prometheus

# Configure scraping
# Edit prometheus.yml to include GenX-FX metrics
```

### Grafana (Optional)
```bash
# Install Grafana
docker run -d -p 3000:3000 grafana/grafana

# Import dashboard
# Use provided Grafana dashboard configuration
```

## 🚀 Running the System

### Development Mode
```bash
# Run with debug logging
python main.py --debug --config config/config.yaml
```

### Production Mode
```bash
# Run with production settings
python main.py --config config/production.yaml
```

### Docker (Optional)
```bash
# Build Docker image
docker build -t genx-fx .

# Run with Docker
docker run -d --name genx-fx genx-fx
```

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_decision_engine.py

# Run with coverage
pytest --cov=genx_fx tests/
```

### Integration Tests
```bash
# Run integration tests
pytest tests/integration/

# Test with paper trading
pytest tests/integration/test_paper_trading.py
```

### Backtesting
```bash
# Run backtest
python -m backtesting.run_backtest --config config/backtest_config.yaml

# Analyze results
python -m backtesting.analyze_results --results results/backtest_20231201/
```

## 📈 Performance Optimization

### Database Optimization
```bash
# Optimize SQLite database
python -m tools.optimize_database --db market_data.db

# Clean old data
python -m tools.cleanup_data --days 30
```

### Memory Optimization
```bash
# Monitor memory usage
python -m tools.monitor_memory

# Optimize memory usage
python -m tools.optimize_memory
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

#### 2. Database Connection Issues
```bash
# Solution: Check database file permissions
chmod 644 market_data.db
```

#### 3. Broker Connection Issues
```bash
# Solution: Verify API keys and network connectivity
python -m tools.test_broker_connection
```

#### 4. Memory Issues
```bash
# Solution: Reduce data retention period
# Edit config.yaml: data.retention_days: 7
```

### Log Analysis
```bash
# View system logs
tail -f logs/genx_trading.log

# Analyze error logs
grep "ERROR" logs/genx_trading.log

# Monitor performance
grep "PERFORMANCE" logs/genx_trading.log
```

## 📚 Next Steps

1. **Paper Trading**: Start with paper trading to test the system
2. **Backtesting**: Run historical backtests to validate strategies
3. **Monitoring**: Set up monitoring and alerting
4. **Optimization**: Fine-tune parameters based on performance
5. **Production**: Deploy to production with real money

## 🆘 Support

If you encounter issues:

1. **Check Logs**: Review system logs for error messages
2. **Documentation**: Consult the full documentation
3. **Community**: Ask questions in the GitHub discussions
4. **Issues**: Report bugs in the GitHub issues

## 🔒 Security Best Practices

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use environment variables for sensitive data
3. **Network Security**: Use secure connections (HTTPS)
4. **Access Control**: Limit system access to authorized users
5. **Regular Updates**: Keep dependencies updated

---

**Happy Trading! 🚀**
