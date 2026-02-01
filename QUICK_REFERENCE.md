# 🎯 Quick Reference - Conference Bot

## What I've Created For You

### ✅ Complete Bot with Filtering Features
- **Country Filters**: USA, UK, Germany, Poland, Netherlands, Spain, France, Italy, Canada, Australia, Online, All
- **Direction Filters**: Agile, DevOps, Testing/QA, Cloud, Security, Data Science, AI/ML, Mobile, Web, Architecture, Management, All

### 📁 Files Included

1. **conference_bot.py** - Main bot application with all features
2. **requirements.txt** - Python dependencies
3. **.env.example** - Template for your bot token
4. **.gitignore** - Git ignore rules
5. **README.md** - Complete documentation
6. **DEPLOYMENT_GUIDE.md** - Step-by-step deployment instructions
7. **setup.sh** / **setup.bat** - Automatic setup scripts (Linux/Mac & Windows)
8. **run_bot.sh** / **run_bot.bat** - Easy start scripts (Linux/Mac & Windows)

## 🚀 Super Quick Start

### Linux/Mac (3 steps):
```bash
./setup.sh
# Edit .env with your token
./run_bot.sh
```

### Windows (3 steps):
```batch
setup.bat
REM Edit .env with your token
run_bot.bat
```

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome & introduction |
| `/filter` | Set country & direction filters |
| `/list` | View matching conferences |
| `/myfilters` | View your current filters |
| `/subscribe` | Enable notifications |
| `/unsubscribe` | Disable notifications |
| `/help` | Show help message |

## 🎨 How Filtering Works

Users can:
1. Select **multiple countries** (or "All Countries")
2. Select **multiple directions** (or "All Directions")
3. Preferences are **saved automatically**
4. Only conferences matching **both** filters are shown

### Example Use Case:
```
User selects:
- Countries: USA, Poland, Online
- Directions: DevOps, Testing

Result: Only DevOps/Testing conferences in USA, Poland, or Online
```

## 🔧 Next Steps to Customize

### 1. Add Real Conference Data
Replace `load_sample_conferences()` in `conference_bot.py`:

```python
def load_conferences_from_api(self):
    # Your API call here
    response = requests.get('https://api.conferences.com/events')
    data = response.json()
    
    self.conferences = [
        Conference(
            id=conf['id'],
            name=conf['name'],
            date=conf['date'],
            location=conf['location'],
            country=conf['country'],
            directions=[d.lower() for d in conf['topics']],
            url=conf['url']
        )
        for conf in data
    ]
```

### 2. Add More Countries
Edit `COUNTRIES` list in `conference_bot.py`:
```python
COUNTRIES = [
    "🇺🇸 USA", "🇬🇧 UK", "🇩🇪 Germany", 
    "🇯🇵 Japan",  # Add this
    "🇸🇬 Singapore",  # And this
    # ... etc
]
```

### 3. Add More Directions
Edit `DIRECTIONS` list:
```python
DIRECTIONS = [
    "🔄 Agile", "🚀 DevOps", 
    "🎮 Gaming",  # Add this
    "🔗 Blockchain",  # And this
    # ... etc
]
```

## 🐛 Common Issues & Fixes

### "Conflict" Error
```bash
# Kill existing instances
ps aux | grep conference_bot.py
kill -9 <PID>
```

### Bot Not Responding
1. Check token in `.env`
2. Verify bot is running
3. Check internet connection
4. Look at terminal for errors

### "Module not found"
```bash
source venv/bin/activate  # Activate venv first!
pip install -r requirements.txt
```

## 📊 Data Persistence

- **User preferences** saved to `user_preferences.json`
- **Survives restarts** - users don't lose their filters
- **JSON format** - easy to backup/inspect

## 🌐 Running 24/7

### Linux Server (Best):
```bash
sudo systemctl enable conference-bot
sudo systemctl start conference-bot
```

### Screen (Simple):
```bash
screen -S bot
./run_bot.sh
# Ctrl+A, then D to detach
```

### Windows (Keep Terminal Open):
```batch
run_bot.bat
REM Minimize window
```

## 📈 Monitoring

### Check if running:
```bash
ps aux | grep conference_bot.py
```

### View logs (if using systemd):
```bash
journalctl -u conference-bot -f
```

## 🎓 Understanding the Code

### Main Components:

1. **Conference** - Data model for conferences
2. **UserPreferences** - Manages user filter settings
3. **ConferenceBot** - Main bot logic
4. **Handlers** - Process commands and callbacks

### Flow:
```
User sends /filter
  → Bot shows country buttons
  → User selects countries
  → Bot shows direction buttons  
  → User selects directions
  → Preferences saved
  → User uses /list
  → Bot filters conferences
  → Shows matching results
```

## 🔐 Security Notes

- ✅ Token stored in `.env` (not committed to git)
- ✅ `.env` in `.gitignore`
- ✅ No hardcoded credentials
- ✅ User data in local JSON file

## 📞 Getting Help

1. Read **DEPLOYMENT_GUIDE.md** for detailed setup
2. Check **README.md** for features & usage
3. Look at error messages in terminal
4. Google specific errors
5. Open GitHub issue with logs

## ✨ Features Implemented

- ✅ Multi-country filtering
- ✅ Multi-direction filtering  
- ✅ Persistent user preferences
- ✅ Subscribe/Unsubscribe
- ✅ Conference listing
- ✅ Interactive button UI
- ✅ Conversation flow for filter setup
- ✅ Ready for 24/7 deployment

## 🚫 Why Render.com Might Not Work

Render.com issues:
- Free tier sleeps after inactivity
- Polling mode needs constant connection
- Better for webhook mode (requires HTTPS)

**Local deployment is simpler and more reliable for polling mode!**

## 💡 Future Enhancements

Ideas to add:
- [ ] Web scraping for conferences
- [ ] Calendar export (.ics files)
- [ ] Conference reminders (1 week before)
- [ ] Search by keyword
- [ ] Price range filters
- [ ] Date range filters
- [ ] Email notifications
- [ ] Admin panel
- [ ] Analytics/stats

---

**Ready to deploy?** Start with DEPLOYMENT_GUIDE.md! 🚀
