# QA & IT Conference Discovery Telegram Bot 🤖

A Telegram bot that helps you discover QA and IT conferences across Europe and notifies you about new events with early bird ticket availability.

## Features ✨

- 🔍 **Search Conferences**: Find upcoming QA and IT conferences across Europe
- 🔔 **Smart Notifications**: Get notified when new conferences are added
- 🎟️ **Early Bird Alerts**: Never miss early bird ticket opportunities
- 📍 **Custom Filters**: Filter by country, topic, and date
- 💾 **Conference Database**: Stores conference information locally

## Setup Instructions 🚀

### 1. Create Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "Conference Finder")
4. Choose a username (must end in 'bot', e.g., "qa_conference_finder_bot")
5. BotFather will give you an API token - save this!

### 2. Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the Bot

Set your Telegram bot token as an environment variable:

```bash
# Linux/Mac
export TELEGRAM_BOT_TOKEN='your-token-from-botfather'

# Windows (Command Prompt)
set TELEGRAM_BOT_TOKEN=your-token-from-botfather

# Windows (PowerShell)
$env:TELEGRAM_BOT_TOKEN='your-token-from-botfather'
```

Or create a `.env` file:

```
TELEGRAM_BOT_TOKEN=your-token-from-botfather
```

### 4. Run the Bot

```bash
python conference_bot.py
```

The bot will start and you should see "Starting bot..." in the console.

## Usage 📱

### Available Commands

- `/start` - Start the bot and see welcome message
- `/search` - Search for QA/IT conferences
- `/subscribe` - Enable notifications for new conferences
- `/unsubscribe` - Disable notifications
- `/upcoming` - View upcoming conferences (next 3 months)
- `/filters` - Set your notification preferences
- `/help` - Show help message

### Example Workflow

1. Start a chat with your bot on Telegram
2. Send `/start` to initialize
3. Send `/subscribe` to enable notifications
4. Send `/search` to find conferences
5. Use `/filters` to customize what you see
6. Receive automatic notifications about new conferences!

## How It Works 🔧

### Architecture

```
conference_bot.py          # Main bot logic
├── ConferenceBot         # Core bot class
├── Command Handlers      # /start, /search, /subscribe, etc.
├── Callback Handlers     # Button interactions
└── Background Jobs       # Periodic conference checks

conferences.json          # Conference database
users.json               # User subscriptions and preferences
```

### Data Storage

The bot uses JSON files to store:
- **conferences.json**: All discovered conferences with details
- **users.json**: User subscriptions and filter preferences

### Notification System

The bot runs a background job every 12 hours to:
1. Search for new conferences online
2. Compare with existing database
3. Notify subscribed users about new findings
4. Alert about upcoming early bird deadlines

## Enhancing the Bot 🛠️

### Adding Web Search Capability

To enable real-time conference discovery, integrate web scraping:

```python
import requests
from bs4 import BeautifulSoup

def scrape_conferences():
    """Scrape conferences from popular sites"""
    sources = [
        'https://confs.tech',
        'https://conferenceindex.org',
        # Add more sources
    ]
    # Implement scraping logic
```

### Adding More Data Sources

Popular conference aggregators:
- Confs.tech (has an API!)
- Conferenceindex.org
- 10times.com
- Eventbrite API
- Meetup API

### Database Upgrade

For production use, consider replacing JSON files with:
- SQLite (built-in Python)
- PostgreSQL (scalable)
- MongoDB (flexible schema)

## Deployment Options 🌐

### Option 1: Run on Your Computer

Simple for testing, but bot stops when computer is off.

### Option 2: Deploy to a Server

**Free Options:**
- **Heroku** (with worker dyno)
- **Railway.app**
- **Render.com**
- **PythonAnywhere**

**Paid Options:**
- AWS EC2
- Google Cloud
- DigitalOcean

### Option 3: Serverless

- AWS Lambda with scheduled triggers
- Google Cloud Functions

## Example Deployment (Heroku)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create your-conference-bot

# Set environment variable
heroku config:set TELEGRAM_BOT_TOKEN='your-token'

# Create Procfile
echo "worker: python conference_bot.py" > Procfile

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Start the worker
heroku ps:scale worker=1
```

## Troubleshooting 🔍

### Bot doesn't respond
- Check if the bot is running (`python conference_bot.py`)
- Verify your token is correct
- Check console for error messages

### No notifications
- Ensure you've subscribed with `/subscribe`
- Check that the background job is running
- Verify conferences exist in the database

### Dependencies issues
- Make sure Python 3.8+ is installed
- Try reinstalling: `pip install -r requirements.txt --upgrade`

## Future Enhancements 🚀

- [ ] Integration with conference APIs (Confs.tech, Eventbrite)
- [ ] Calendar export (iCal format)
- [ ] Price tracking for tickets
- [ ] Conference reviews and ratings
- [ ] Multi-language support
- [ ] Speaking opportunity alerts
- [ ] Hotel and travel recommendations
- [ ] Early bird ticket countdown timer

## Contributing 🤝

Feel free to enhance the bot with:
- More data sources
- Better search algorithms
- UI improvements
- Additional notification options

## License 📄

This project is open source and available under the MIT License.

## Support 💬

If you encounter issues:
1. Check the console output for errors
2. Verify your bot token
3. Ensure all dependencies are installed
4. Check Telegram API status

## Acknowledgments 🙏

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Conference data from community sources

---

Happy conference hunting! 🎉
