#!/bin/bash

echo "🚀 Starting Conference Bot..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the bot
python conference_bot.py
