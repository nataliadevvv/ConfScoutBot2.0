#!/usr/bin/env python3
"""
Setup script for Conference Discovery Bot
Helps users configure the bot easily
"""

import os
import sys

def print_header():
    print("=" * 60)
    print("  QA & IT Conference Discovery Bot - Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   You have Python {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print("✅ Python version OK")
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Error installing dependencies:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_bot_token():
    """Get bot token from user"""
    print("\n🤖 Telegram Bot Setup")
    print("-" * 60)
    print("To create a bot:")
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot and follow the instructions")
    print("3. Copy the API token you receive")
    print("-" * 60)
    
    token = input("\nEnter your bot token (or press Enter to skip): ").strip()
    
    if token:
        # Create .env file
        with open('.env', 'w') as f:
            f.write(f"TELEGRAM_BOT_TOKEN={token}\n")
        
        # Also set environment variable for current session
        os.environ['TELEGRAM_BOT_TOKEN'] = token
        
        print("✅ Token saved to .env file")
        return True
    else:
        print("⏭️  Skipped. You can set the token later in .env file")
        return False

def create_data_files():
    """Create initial data files"""
    print("\n📁 Creating data files...")
    
    # Create empty conferences.json
    if not os.path.exists('conferences.json'):
        with open('conferences.json', 'w') as f:
            f.write('{}')
        print("✅ Created conferences.json")
    
    # Create empty users.json
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            f.write('{}')
        print("✅ Created users.json")

def test_bot():
    """Test if bot can start"""
    print("\n🧪 Testing bot configuration...")
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("⚠️  No bot token found. Please set TELEGRAM_BOT_TOKEN")
        return False
    
    try:
        import telegram
        bot = telegram.Bot(token=token)
        me = bot.get_me()
        print(f"✅ Bot connected successfully!")
        print(f"   Bot name: @{me.username}")
        return True
    except Exception as e:
        print(f"❌ Error connecting to bot: {e}")
        return False

def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "=" * 60)
    print("  Setup Complete! 🎉")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run the bot:")
    print("   python conference_bot.py")
    print()
    print("2. Open Telegram and search for your bot")
    print()
    print("3. Send /start to begin using the bot")
    print()
    print("Useful commands:")
    print("  /search     - Search for conferences")
    print("  /subscribe  - Get notifications")
    print("  /upcoming   - View upcoming events")
    print()
    print("For more info, check README.md")
    print("=" * 60)

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Warning: Failed to install dependencies")
        print("   Try running: pip install -r requirements.txt")
    
    # Get bot token
    token_set = get_bot_token()
    
    # Create data files
    create_data_files()
    
    # Test bot if token was provided
    if token_set:
        test_bot()
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    main()
