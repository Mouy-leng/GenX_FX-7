#!/usr/bin/env python3
"""
A6-9V Secure Credential Update Helper
Safely updates credential files without exposing secrets
"""

import os
import getpass
from pathlib import Path
import re

class SecureCredentialUpdater:
    """Helper for safely updating credentials"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.secrets_file = self.base_path / "config" / "secrets.env"
        self.main_env_file = Path(__file__).parent.parent.parent.parent / ".env"
        
    def update_cursor_api_key(self):
        """Update Cursor API key in main .env file"""
        print("🔑 Updating Cursor API Key")
        print("="*50)
        
        # Get current value
        current_key = self._get_current_value(self.main_env_file, "CURSOR_API_KEY")
        if current_key and current_key != "your_cursor_api_key_here":
            print(f"Current key: {current_key[:10]}...")
            update = input("Update existing key? (y/n): ").lower().strip()
            if update != 'y':
                return
        
        # Get new key securely
        new_key = getpass.getpass("Enter your Cursor API Key (hidden): ")
        if not new_key or new_key.strip() == "":
            print("❌ No key entered. Cancelled.")
            return
            
        # Update file
        self._update_env_value(self.main_env_file, "CURSOR_API_KEY", new_key.strip())
        print("✅ Cursor API Key updated successfully!")
        
    def update_openai_key(self):
        """Update OpenAI API key"""
        print("🤖 Updating OpenAI API Key")
        print("="*50)
        
        current_key = self._get_current_value(self.secrets_file, "OPENAI_API_KEY")
        if current_key and current_key != "your_openai_api_key_here":
            print(f"Current key: {current_key[:10]}...")
            update = input("Update existing key? (y/n): ").lower().strip()
            if update != 'y':
                return
        
        new_key = getpass.getpass("Enter your OpenAI API Key (hidden): ")
        if not new_key or new_key.strip() == "":
            print("❌ No key entered. Cancelled.")
            return
            
        self._update_env_value(self.secrets_file, "OPENAI_API_KEY", new_key.strip())
        print("✅ OpenAI API Key updated successfully!")
    
    def update_trading_keys(self):
        """Update trading platform keys"""
        print("🏦 Updating Trading Platform Keys")
        print("="*50)
        
        platforms = [
            ("ALPACA_API_KEY", "Alpaca API Key"),
            ("ALPACA_SECRET_KEY", "Alpaca Secret Key"),
            ("BINANCE_API_KEY", "Binance API Key"),  
            ("BINANCE_SECRET_KEY", "Binance Secret Key")
        ]
        
        for key_name, display_name in platforms:
            current = self._get_current_value(self.secrets_file, key_name)
            if current and not current.startswith("your_"):
                print(f"✅ {display_name}: {current[:10]}... (already set)")
                continue
                
            print(f"\n📍 {display_name}:")
            new_key = getpass.getpass(f"Enter {display_name} (hidden, or press Enter to skip): ")
            if new_key and new_key.strip():
                self._update_env_value(self.secrets_file, key_name, new_key.strip())
                print(f"✅ {display_name} updated!")
    
    def update_github_token(self):
        """Update GitHub token"""
        print("💻 Updating GitHub Token")
        print("="*50)
        
        current_token = self._get_current_value(self.secrets_file, "GITHUB_TOKEN")
        if current_token and current_token != "your_github_token_here":
            print(f"Current token: {current_token[:10]}...")
            update = input("Update existing token? (y/n): ").lower().strip()
            if update != 'y':
                return
        
        print("To get a GitHub token:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Generate new token (classic)")
        print("3. Select scopes: repo, workflow, admin:repo_hook")
        
        new_token = getpass.getpass("Enter your GitHub Token (hidden): ")
        if not new_token or new_token.strip() == "":
            print("❌ No token entered. Cancelled.")
            return
            
        self._update_env_value(self.secrets_file, "GITHUB_TOKEN", new_token.strip())
        print("✅ GitHub Token updated successfully!")
        
    def _get_current_value(self, file_path, key_name):
        """Get current value for a key"""
        try:
            if not file_path.exists():
                return None
                
            with open(file_path, 'r') as f:
                content = f.read()
                
            pattern = rf'^{re.escape(key_name)}=(.*)$'
            match = re.search(pattern, content, re.MULTILINE)
            return match.group(1) if match else None
            
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
            return None
    
    def _update_env_value(self, file_path, key_name, new_value):
        """Update or add a key=value pair in env file"""
        try:
            # Read current content
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
            else:
                content = ""
            
            # Update or add the key
            pattern = rf'^{re.escape(key_name)}=.*$'
            new_line = f"{key_name}={new_value}"
            
            if re.search(pattern, content, re.MULTILINE):
                # Replace existing
                content = re.sub(pattern, new_line, content, flags=re.MULTILINE)
            else:
                # Add new key
                content = content.rstrip() + f"\n{new_line}\n"
            
            # Write back
            file_path.parent.mkdir(exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
                
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
    
    def show_status(self):
        """Show current credential status"""
        print("\n📊 Current Credential Status")
        print("="*50)
        
        # Check main .env
        cursor_key = self._get_current_value(self.main_env_file, "CURSOR_API_KEY")
        status = "✅ SET" if cursor_key and not cursor_key.startswith("your_") else "❌ NOT SET"
        print(f"Cursor API Key: {status}")
        
        # Check trading system secrets
        keys_to_check = [
            ("OPENAI_API_KEY", "OpenAI API Key"),
            ("GITHUB_TOKEN", "GitHub Token"),
            ("ALPACA_API_KEY", "Alpaca API Key"),
            ("BINANCE_API_KEY", "Binance API Key"),
        ]
        
        for key_name, display_name in keys_to_check:
            value = self._get_current_value(self.secrets_file, key_name)
            status = "✅ SET" if value and not value.startswith("your_") else "❌ NOT SET"
            print(f"{display_name}: {status}")

def main():
    """Main interactive credential update"""
    updater = SecureCredentialUpdater()
    
    while True:
        print("\n🔐 A6-9V Secure Credential Updater")
        print("="*50)
        print("1. 📊 Show current status")
        print("2. 💻 Update Cursor API Key")
        print("3. 🤖 Update OpenAI API Key") 
        print("4. 🏦 Update Trading Platform Keys")
        print("5. 💻 Update GitHub Token")
        print("0. 🚪 Exit")
        
        choice = input("\nSelect option (0-5): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            updater.show_status()
        elif choice == "2":
            updater.update_cursor_api_key()
        elif choice == "3":
            updater.update_openai_key()
        elif choice == "4":
            updater.update_trading_keys()
        elif choice == "5":
            updater.update_github_token()
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()