# GenX-FX Secrets Management & Environment Setup Guide

## 🔐 Comprehensive Secrets Collection and Management

This guide will help you collect all secrets from your Google Drive (G:), (H:), Dropbox, OneDrive, and local drives, then set them up properly for the GenX-FX Autonomous Trading System.

## 📋 Overview

The GenX-FX system includes comprehensive scripts to:

1. **Collect Secrets** - Scan all drives and cloud storage for API keys, credentials, and configuration files
2. **Organize Secrets** - Categorize and consolidate all found secrets
3. **Setup Environments** - Configure all development environments (Cursor, PyCharm, VS Code)
4. **Create Notebooks** - Generate agent-specific configuration notebooks
5. **Secure Storage** - Create encrypted backups of all secrets

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the complete setup script
python scripts/complete_setup.py

# Or use the batch file on Windows
run_setup.bat
```

### Option 2: Manual Setup
```bash
# Step 1: Collect all secrets
python scripts/collect_all_secrets.py

# Step 2: Setup development environments
python scripts/setup_dev_env.py

# Step 3: Create agent notebooks
python scripts/collect_secrets.py
```

## 📁 What Gets Collected

### Secret Locations Scanned:
- **Google Drive (G:)** - `G:/`
- **Google Drive (H:)** - `H:/`
- **Dropbox** - `C:/Users/lengk/Dropbox/`
- **OneDrive** - `C:/Users/lengk/OneDrive/`
- **Desktop** - `C:/Users/lengk/Desktop/`
- **Documents** - `C:/Users/lengk/Documents/`
- **Downloads** - `C:/Users/lengk/Downloads/`
- **A6-9V Tools** - `C:/Users/lengk/Dropbox/OneDrive/Desktop/A6-9V Tools/`
- **A6-9V Trading** - `C:/Users/lengk/Dropbox/OneDrive/Desktop/A6-9V Trading/`
- **Additional Drives** - D:, E:, J: drives

### File Types Collected:
- **Environment Files** - `.env`, `.ini`, `.cfg`, `.conf`
- **API Keys** - `.key`, `.pem`, `.p12`, `.pfx`
- **Configurations** - `.json`, `.yaml`, `.yml`, `.xml`
- **Credentials** - `secrets*`, `credentials*`, `config*`
- **Certificates** - `.pem`, `.key`, `.p12`, `.pfx`, `.jks`
- **Logs** - `.log`, `.txt`, `.csv`

## 🔍 Generated Files

After running the setup, you'll find:

### 📊 Reports Directory (`reports/`)
- `comprehensive_secrets_report.json` - Complete secrets inventory
- `comprehensive_secrets_report.yaml` - YAML format report
- `comprehensive_secrets_inventory.md` - Detailed markdown report
- `api_keys_security_report.md` - Security alert for found API keys
- `development_setup_report.md` - Development environment setup report
- `complete_setup_report.md` - Final setup summary

### 🔐 Configuration Directory (`config/`)
- `consolidated_secrets.env` - All collected secrets in one file
- `secrets.env.example` - Template for environment variables

### 📓 Notebooks Directory (`notebooks/`)
- `GenX_FX_Agent_Notebook.ipynb` - Main agent configuration
- `GenX_FX_Main_Notebook.ipynb` - Complete system notebook
- Individual agent notebooks for each component

### 💾 Backups Directory (`backups/`)
- Encrypted backups of all found secret files
- Organized by location and timestamp
- Secure storage for critical credentials

## 🛠️ Development Environment Setup

### Cursor IDE Configuration
- **Workspace File** - `GenX-FX.code-workspace`
- **Settings** - `.vscode/settings.json`
- **Extensions** - Python, Jupyter, GitLens, Pylance
- **Launch Config** - `.vscode/launch.json`

### PyCharm Professional Configuration
- **Project Settings** - `.idea/project_config.json`
- **Interpreter** - Python 3.9
- **Plugins** - Python, Jupyter, Git integration
- **Code Style** - Black formatter, Pylint

### Visual Studio Code Configuration
- **Workspace** - `GenX-FX.code-workspace`
- **Settings** - Python, Jupyter, GitLens
- **Extensions** - Python, Jupyter, Pylance, Flake8, MyPy
- **Debugging** - Launch configurations for main and test

## 🔒 Security Features

### Automatic Security Scanning
- **API Key Detection** - Regex patterns to find exposed keys
- **Secret Classification** - Categorize by type and sensitivity
- **Security Alerts** - Immediate notification of found credentials
- **Rotation Recommendations** - Suggest key rotation for exposed secrets

### Secure Storage
- **Encrypted Backups** - All secrets backed up securely
- **Access Control** - Proper file permissions
- **Audit Trail** - Complete log of all collected secrets
- **Version Control** - Track changes to secret files

## 📋 Agent-Specific Configuration

### Autonomous Agent
- **Configuration** - Risk limits, learning parameters
- **Secrets** - API keys, authentication tokens
- **Environment** - Trading hours, market data sources

### Decision Engine
- **ML Models** - Model registry, training data
- **Strategies** - Trading strategy configurations
- **Features** - Technical indicator parameters

### Risk Manager
- **Limits** - Position sizing, drawdown limits
- **Monitoring** - Real-time risk metrics
- **Alerts** - Risk threshold notifications

### Self Manager
- **Updates** - Autonomous code updates
- **Backups** - System state backups
- **Rollbacks** - Emergency recovery procedures

## 🚨 Security Recommendations

### Immediate Actions Required:
1. **Review Found Secrets** - Check `config/consolidated_secrets.env`
2. **Rotate Exposed Keys** - Change any compromised credentials
3. **Remove from Files** - Delete secrets from source files
4. **Update Systems** - Update any systems using exposed keys
5. **Monitor Usage** - Watch for unauthorized access

### Long-term Security:
1. **Secret Management** - Implement proper secret management system
2. **Access Control** - Limit access to sensitive files
3. **Regular Audits** - Schedule periodic security reviews
4. **Encryption** - Encrypt sensitive data at rest
5. **Monitoring** - Continuous security monitoring

## 🔧 Troubleshooting

### Common Issues:

#### 1. Permission Denied
```bash
# Solution: Run as administrator
# Or check file permissions
chmod 755 scripts/
```

#### 2. Missing Dependencies
```bash
# Solution: Install required packages
pip install -r requirements.txt
```

#### 3. Drive Not Found
```bash
# Solution: Check drive letters
# Update secret_locations in scripts if needed
```

#### 4. Large Files
```bash
# Solution: Files > 50MB are automatically skipped
# Check logs for skipped files
```

## 📊 Monitoring and Alerts

### System Health Monitoring
- **File System** - Monitor secret file changes
- **Access Logs** - Track who accesses secrets
- **Backup Status** - Verify backup integrity
- **Security Events** - Alert on suspicious activity

### Performance Metrics
- **Collection Time** - How long secrets collection takes
- **File Count** - Number of files processed
- **Success Rate** - Percentage of successful operations
- **Error Rate** - Failed operations tracking

## 📚 Additional Resources

### Documentation
- **Setup Guide** - `docs/SETUP_GUIDE.md`
- **Architecture** - `docs/TRADING_SYSTEM/ARCHITECTURE.md`
- **Security** - `docs/TRADING_SYSTEM/SECURITY_COMPLIANCE.md`

### Scripts
- **Complete Setup** - `scripts/complete_setup.py`
- **Secrets Collection** - `scripts/collect_all_secrets.py`
- **Dev Environment** - `scripts/setup_dev_env.py`

### Configuration
- **Environment Template** - `config/secrets.env.example`
- **Consolidated Secrets** - `config/consolidated_secrets.env`
- **IDE Settings** - `.vscode/`, `.idea/`

## 🆘 Support

If you encounter issues:

1. **Check Logs** - Review system logs for error messages
2. **Read Reports** - Check generated reports for details
3. **Verify Permissions** - Ensure proper file access
4. **Update Dependencies** - Install missing packages
5. **Contact Support** - Reach out for assistance

## 🎯 Next Steps

After completing the setup:

1. **Review Secrets** - Check `config/consolidated_secrets.env`
2. **Update Credentials** - Fill in missing API keys
3. **Test Connections** - Verify all external services
4. **Run System** - Execute `python main.py`
5. **Monitor Performance** - Watch the system dashboard
6. **Review Reports** - Check all generated documentation

---

**🔐 Remember: Security is paramount. Always review and secure your credentials!**
