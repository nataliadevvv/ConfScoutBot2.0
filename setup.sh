#!/bin/bash

echo "🤖 Conference Bot - Quick Start Setup"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Telegram bot token!"
    echo "   Get your token from: https://t.me/botfather"
    echo ""
    read -p "Press Enter to open .env file in nano editor..." 
    nano .env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the bot:"
echo "  1. source venv/bin/activate"
echo "  2. python conference_bot.py"
echo ""
echo "Or run: ./run_bot.sh"
echo ""
