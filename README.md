# Conference Bot 🤖

A Telegram bot for tracking IT conferences with filtering by country and direction (Agile, DevOps, Testing, QA, Cloud, Security, etc.).

## Features ✨

- 🌍 **Country Filtering**: Filter conferences by country (USA, UK, Germany, Poland, etc.)
- 🎯 **Direction Filtering**: Filter by conference topics (Agile, DevOps, Testing, Cloud, Security, AI/ML, etc.)
- 🔔 **Smart Notifications**: Get notified about new conferences matching your interests
- 📅 **Upcoming Conferences**: View all upcoming conferences matching your filters
- 💾 **Persistent Preferences**: Your filters are saved automatically

## Available Filters

### Countries 🌍
- USA, UK, Germany, Poland, Netherlands, Spain, France, Italy
- Canada, Australia
- Online conferences
- All Countries (no filter)

### Directions 🎯
- Agile
- DevOps
- Testing/QA
- Cloud
- Security
- Data Science
- AI/ML
- Mobile Development
- Web Development
- Architecture
- Management
- All Directions (no filter)

## Local Deployment 🚀

### Prerequisites

- Python 3.9 or higher
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/conference-bot.git
cd conference-bot
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your bot token
nano .env  # or use any text editor
```

Add your token:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Step 5: Run the Bot

```bash
python conference_bot.py
```

You should see:
```
INFO - Starting Conference Bot...
INFO - Application started
```

## Running as a Service (Linux) 🔄

To keep the bot running 24/7 on Linux:

### Create systemd service:

```bash
sudo nano /etc/systemd/system/conference-bot.service
```

Add this content:

```ini
[Unit]
Description=Conference Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/conference-bot
Environment="PATH=/path/to/conference-bot/venv/bin"
ExecStart=/path/to/conference-bot/venv/bin/python conference_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable conference-bot
sudo systemctl start conference-bot

# Check status
sudo systemctl status conference-bot

# View logs
journalctl -u conference-bot -f
```

## Running with Screen (Alternative) 📺

```bash
# Install screen
sudo apt-get install screen  # Ubuntu/Debian
# or
sudo yum install screen      # CentOS/RHEL

# Start a screen session
screen -S conference-bot

# Run the bot
python conference_bot.py

# Detach: Press Ctrl+A then D

# Reattach later
screen -r conference-bot

# List all screens
screen -ls
```

## Running on Windows 🪟

### Method 1: Keep Terminal Open
Simply run the bot and keep the terminal window open.

### Method 2: Use pythonw (Hidden Window)
```bash
pythonw conference_bot.py
```

### Method 3: Create a Batch File
Create `start_bot.bat`:
```batch
@echo off
cd /d %~dp0
call venv\Scripts\activate
python conference_bot.py
pause
```

## Bot Commands 📝

- `/start` - Welcome message and introduction
- `/filter` - Set your country and direction filters
- `/list` - View conferences matching your filters
- `/myfilters` - View your current filter settings
- `/subscribe` - Enable notifications for new conferences
- `/unsubscribe` - Disable notifications
- `/help` - Show help message

## Usage Example 💡

1. Start the bot: `/start`
2. Set filters: `/filter`
   - Select countries: USA, UK, Poland
   - Select directions: DevOps, Testing, Cloud
3. View conferences: `/list`
4. Enable notifications: `/subscribe`

## Troubleshooting 🔧

### "Conflict: terminated by other getUpdates request"

This means you have multiple bot instances running:

```bash
# Find and kill all instances
ps aux | grep conference_bot.py
kill -9 <PID>

# Or on Windows
tasklist | findstr python
taskkill /F /PID <PID>
```

### Bot not responding

1. Check if bot is running: `ps aux | grep conference_bot.py`
2. Check logs for errors
3. Verify your bot token is correct
4. Ensure you have internet connection

### Dependencies issues

```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Development 🛠️

### Adding New Conferences

Edit the `load_sample_conferences()` method in `conference_bot.py`:

```python
def load_sample_conferences(self):
    self.conferences = [
        Conference(
            id="1",
            name="Your Conference Name",
            date="2026-03-15",
            location="City Name",
            country="Country",
            directions=["agile", "testing"],  # lowercase
            url="https://conference-url.com",
            description="Description here"
        ),
        # Add more conferences...
    ]
```

### Integrating with Conference APIs

Replace `load_sample_conferences()` with your API/scraper:

```python
def fetch_conferences_from_api(self):
    """Fetch conferences from external API"""
    response = requests.get('https://api.example.com/conferences')
    data = response.json()
    
    self.conferences = [
        Conference(
            id=conf['id'],
            name=conf['name'],
            date=conf['date'],
            location=conf['location'],
            country=conf['country'],
            directions=conf['topics'],
            url=conf['url']
        )
        for conf in data['conferences']
    ]
```

## File Structure 📁

```
conference-bot/
├── conference_bot.py          # Main bot file
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .env                      # Your actual config (not in git)
├── .gitignore               # Git ignore rules
├── user_preferences.json    # User data (auto-generated)
├── venv/                    # Virtual environment
└── README.md               # This file
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License 📄

MIT License - feel free to use and modify!

## Support 💬

If you have issues:
1. Check the Troubleshooting section
2. Open an issue on GitHub
3. Contact [@YourTelegramHandle](https://t.me/yourhandle)

## TODO 📋

- [ ] Integrate with real conference APIs
- [ ] Add web scraping for conference sites
- [ ] Support more countries and directions
- [ ] Add calendar export (.ics files)
- [ ] Implement conference reminders
- [ ] Add search functionality
- [ ] Multi-language support

---

Made with ❤️ for the IT conference community
