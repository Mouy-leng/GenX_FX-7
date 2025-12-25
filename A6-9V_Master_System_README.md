# A6-9V Enhanced Master Trading System

## Organization: A6-9V
**Complete Trading Automation & Development Environment Launcher**

---

## 📋 System Overview

The A6-9V Enhanced Master Launcher is a comprehensive automation system that manages:
- **MetaTrader 4 & 5 Trading Platforms**
- **Python-based Trading Systems**
- **Development Environment Setup**
- **Automated Login & Trading Activation**

---

## 🗂️ Files Structure

```
C:\Users\lengk\Dropbox\OneDrive\Desktop\
├── A6-9V_Enhanced_Master_Launcher.bat      # Main system launcher
├── MT_AutoLogin_Fixed.ps1                  # MT4/5 automated login script
├── A6-9V_Master_Launcher.bat              # Original launcher (backup)
└── A6-9V_Master_System_README.md          # This documentation
```

---

## ⚙️ System Components

### 1. MetaTrader Integration
**Accounts Configured:**

**MT4 EXNESS:**
- Login: `70559995`
- Password: `Leng12345@#$01`
- Server: `Exness-Trail9`

**MT5 EXNESS:**
- Login: `279260115`
- Password: `Leng12345@#$01`
- Server: `Exness-MT5Trail8`

### 2. Python Trading Systems
- **GenX-FX Trading System**
- **Python Management System**
- **Automated Virtual Environment Activation**

### 3. Development Tools
- **Cursor IDE** - Code development environment
- **JetBrains Code With Me** - Collaborative coding session
- **Chrome** - Trading dashboards (TradingView, Yahoo Finance)

### 4. System Monitoring
- **Task Manager** - System resource monitoring
- **Process Verification** - MT4/5 status checking

---

## 🚀 Usage Instructions

### Quick Start
```batch
# Run the enhanced launcher
C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V_Enhanced_Master_Launcher.bat
```

### Manual PowerShell Execution
```powershell
# Run auto-login for both platforms
powershell -ExecutionPolicy Bypass -File "MT_AutoLogin_Fixed.ps1" -Platform both

# Run auto-login for MT4 only
powershell -ExecutionPolicy Bypass -File "MT_AutoLogin_Fixed.ps1" -Platform mt4

# Run auto-login for MT5 only
powershell -ExecutionPolicy Bypass -File "MT_AutoLogin_Fixed.ps1" -Platform mt5
```

---

## 🔧 System Flow

### Phase 1: MetaTrader Setup
1. ✅ Launch MT4 EXNESS terminal
2. ✅ Launch MT5 EXNESS terminal
3. ⏰ Wait 15 seconds for initialization
4. 🔐 Execute automated login script
5. 🤖 Enable Expert Advisors and auto-trading

### Phase 2: Core System Components
1. 📊 Start Python Management System
2. 💹 Launch GenX-FX Trading System
3. ✅ Activate virtual environments

### Phase 3: Development Environment
1. 🖥️ Open Cursor IDE
2. 🌐 Launch trading dashboards
3. 🔗 Open Code With Me session

### Phase 4: Verification & Monitoring
1. 🔍 Verify MT4/5 processes
2. 📈 Start system monitoring
3. 🔒 Lock desktop (optional)

---

## ⚠️ Important Notes

### Manual Steps Required
1. **MetaTrader Login**: The automated script attempts login but manual verification may be needed
2. **Expert Advisors**: Ensure EAs are enabled in both MT4 and MT5
3. **Trading Permissions**: Verify auto-trading is active
4. **Internet Connection**: Ensure stable connection for trading

### Security Considerations
- Credentials are stored in the PowerShell script
- Desktop auto-lock feature for security
- All processes run with user permissions

---

## 🛠️ Troubleshooting

### Common Issues

**MT4/5 Not Starting:**
```
Check installation paths:
- C:\Program Files (x86)\MetaTrader 4 EXNESS\terminal.exe
- C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe
```

**PowerShell Execution Policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**GenX-FX System Not Found:**
```
Verify paths:
- C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V\Trading\GenX_FX\main.py
- C:\Users\lengk\GenX_FX\src\main.py
```

**Login Automation Fails:**
- Verify MetaTrader windows are focused
- Check credentials in `MT_AutoLogin_Fixed.ps1`
- Ensure server names are correct

---

## 🔄 System Verification

### Check Running Processes
```batch
tasklist /FI "IMAGENAME eq terminal.exe"
tasklist /FI "IMAGENAME eq terminal64.exe"
```

### Verify Trading Status
1. Open MT4/MT5 platforms
2. Check connection status (should show server name)
3. Verify Expert Advisors tab shows "AutoTrading"
4. Confirm account balance and equity display

---

## 📊 System Status Indicators

| Component | Status Check |
|-----------|-------------|
| 🟢 MT4 Running | `terminal.exe` process active |
| 🟢 MT5 Running | `terminal64.exe` process active |
| 🟢 Python Systems | GenX-FX console window visible |
| 🟢 Development | Cursor IDE and Chrome running |
| 🟢 Auto-Trading | EA tab shows "Expert Advisors enabled" |

---

## 🚨 Trading Reminders

### Pre-Trading Checklist
- [ ] Verify account login successful
- [ ] Check internet connection stability
- [ ] Confirm sufficient account balance
- [ ] Enable Expert Advisors
- [ ] Verify trading hours
- [ ] Check economic calendar

### Risk Management
- Monitor account balance and margin levels
- Set appropriate stop-loss levels
- Never risk more than you can afford to lose
- Keep trading journal updated

---

## 📞 Support & Updates

### Organization: A6-9V
**System Version:** Enhanced v2.0
**Last Updated:** 2025-01-20

For issues or improvements, refer to the A6-9V development team.

### Code With Me Session
Join collaborative development session:
- URL: https://code-with-me.global.jetbrains.com/ZhaX8frcoZS0qveUMv8vAg
- Platform: JetBrains IntelliJ IDEA

---

**🎯 Status: OPERATIONAL | A6-9V Master System Ready for Trading**