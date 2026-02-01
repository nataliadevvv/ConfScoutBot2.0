# 🚀 Complete Deployment Guide

## Table of Contents
1. [Quick Start (5 minutes)](#quick-start)
2. [Detailed Setup Instructions](#detailed-setup)
3. [Running 24/7](#running-247)
4. [Troubleshooting](#troubleshooting)
5. [Updating Your Bot](#updating-your-bot)

---

## Quick Start

### For Linux/Mac Users:

```bash
# 1. Get your bot token from @BotFather on Telegram
# 2. Clone/download this repository
# 3. Run setup script
./setup.sh

# 4. Edit .env and add your token (will open automatically)

# 5. Run the bot
./run_bot.sh
```

### For Windows Users:

```batch
REM 1. Get your bot token from @BotFather on Telegram
REM 2. Clone/download this repository
REM 3. Run setup script
setup.bat

REM 4. Edit .env and add your token (will open automatically)

REM 5. Run the bot
run_bot.bat
```

---

## Detailed Setup

### Step 1: Get Your Bot Token

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow instructions to create your bot
5. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Download the Code

**Option A: Using Git**
```bash
git clone https://github.com/yourusername/conference-bot.git
cd conference-bot
```

**Option B: Download ZIP**
1. Download the repository as ZIP
2. Extract it
3. Open terminal/command prompt in that folder

### Step 3: Install Python (if needed)

**Check if Python is installed:**
```bash
python3 --version  # Linux/Mac
python --version   # Windows
```

You need Python 3.9 or higher.

**If not installed:**
- **Linux (Ubuntu/Debian):** `sudo apt-get install python3 python3-venv`
- **Mac:** Download from https://www.python.org or use `brew install python3`
- **Windows:** Download from https://www.python.org (check "Add to PATH" during installation)

### Step 4: Run Setup

**Linux/Mac:**
```bash
chmod +x setup.sh run_bot.sh
./setup.sh
```

**Windows:**
```batch
setup.bat
```

The setup will:
- Create a virtual environment
- Install all dependencies
- Create `.env` file
- Open editor for you to add your token

### Step 5: Add Your Bot Token

Edit the `.env` file and replace `your_bot_token_here` with your actual token:

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Save and close the file.**

### Step 6: Start the Bot

**Linux/Mac:**
```bash
./run_bot.sh
```

**Windows:**
```batch
run_bot.bat
```

You should see:
```
INFO - Starting Conference Bot...
INFO - Application started
```

### Step 7: Test Your Bot

1. Open Telegram
2. Search for your bot (the username you created)
3. Send `/start`
4. You should get a welcome message!

---

## Running 24/7

### Option 1: Linux Server with systemd (Recommended)

Create a service file:

```bash
sudo nano /etc/systemd/system/conference-bot.service
```

Paste this (update paths and username):

```ini
[Unit]
Description=Conference Telegram Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/full/path/to/conference-bot
Environment="PATH=/full/path/to/conference-bot/venv/bin"
ExecStart=/full/path/to/conference-bot/venv/bin/python conference_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Replace:**
- `YOUR_USERNAME` with your Linux username
- `/full/path/to/conference-bot` with actual path (use `pwd` to find it)

**Start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable conference-bot
sudo systemctl start conference-bot
```

**Useful commands:**
```bash
# Check status
sudo systemctl status conference-bot

# View logs
journalctl -u conference-bot -f

# Restart
sudo systemctl restart conference-bot

# Stop
sudo systemctl stop conference-bot
```

### Option 2: Using Screen (Linux/Mac)

```bash
# Install screen
sudo apt-get install screen  # Ubuntu/Debian
brew install screen          # Mac

# Start screen session
screen -S conference-bot

# Run the bot
source venv/bin/activate
python conference_bot.py

# Detach: Press Ctrl+A, then D

# Reattach later
screen -r conference-bot

# List sessions
screen -ls

# Kill session
screen -X -S conference-bot quit
```

### Option 3: Using nohup (Linux/Mac)

```bash
nohup ./run_bot.sh > bot.log 2>&1 &

# View logs
tail -f bot.log

# Find and stop process
ps aux | grep conference_bot.py
kill <PID>
```

### Option 4: Windows - Keep Running

**Method A: Keep Terminal Open**
Just run `run_bot.bat` and minimize the window.

**Method B: Run as Hidden Process**
Create `start_hidden.vbs`:
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "run_bot.bat" & Chr(34), 0
Set WshShell = Nothing
```

Double-click this file to start bot invisibly.

To stop: Open Task Manager → Find Python → End Task

**Method C: Windows Service**
Use NSSM (Non-Sucking Service Manager):
1. Download NSSM from https://nssm.cc/download
2. Run: `nssm install ConferenceBot`
3. Set path to `run_bot.bat`
4. Install and start service

### Option 5: Cloud Servers (DigitalOcean, AWS, etc.)

**1. Create a small VPS ($5-10/month)**
   - DigitalOcean Droplet
   - AWS EC2 t2.micro (free tier)
   - Google Cloud Compute Engine

**2. SSH into your server**
```bash
ssh root@your-server-ip
```

**3. Install dependencies**
```bash
apt-get update
apt-get install python3 python3-venv git
```

**4. Clone your repository**
```bash
git clone https://github.com/yourusername/conference-bot.git
cd conference-bot
```

**5. Follow setup steps above**

**6. Use systemd to keep it running** (see Option 1)

---

## Troubleshooting

### "Conflict: terminated by other getUpdates request"

**Problem:** Multiple bot instances running.

**Solution:**
```bash
# Linux/Mac
ps aux | grep conference_bot.py
kill -9 <PID>

# Windows
tasklist | findstr python
taskkill /F /PID <PID>

# Or just restart your computer
```

### Bot doesn't respond

**Checks:**
1. Is the bot running? Check terminal/task manager
2. Is the token correct in `.env`?
3. Do you have internet connection?
4. Check logs for errors

### "No module named 'telegram'"

**Problem:** Dependencies not installed or wrong Python environment.

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "Permission denied" on Linux

**Solution:**
```bash
chmod +x setup.sh run_bot.sh
```

### Virtual environment issues

**Start fresh:**
```bash
# Remove old venv
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Recreate
python3 -m venv venv  # Linux/Mac
python -m venv venv   # Windows

# Activate and install
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Still having issues?

1. Check bot logs carefully
2. Make sure firewall isn't blocking Python
3. Try running with `python -u conference_bot.py` for unbuffered output
4. Google the specific error message
5. Open an issue on GitHub with the error log

---

## Updating Your Bot

### Update Code

```bash
# Pull latest changes (if using git)
git pull origin main

# Or download and replace files manually
```

### Update Dependencies

```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt --upgrade
```

### Restart Bot

**If using systemd:**
```bash
sudo systemctl restart conference-bot
```

**If using screen:**
```bash
screen -r conference-bot
# Press Ctrl+C to stop
python conference_bot.py
# Press Ctrl+A, then D to detach
```

**If running manually:**
Just stop (Ctrl+C) and restart the bot.

---

## Performance Tips

### For Low-Memory Servers

Add to your service file:
```ini
[Service]
Environment="PYTHONOPTIMIZE=1"
```

### Reduce Log Size

```bash
# Rotate logs
sudo nano /etc/logrotate.d/conference-bot
```

Add:
```
/var/log/conference-bot.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### Monitor Resource Usage

```bash
# Check memory/CPU
htop

# Check specific process
ps aux | grep conference_bot
```

---

## Security Best Practices

1. **Never commit `.env` file** (already in .gitignore)
2. **Keep token secret** - regenerate if exposed
3. **Use environment variables** on servers
4. **Regular updates:** `pip install -r requirements.txt --upgrade`
5. **Set up firewall** on cloud servers
6. **Use HTTPS** for webhook mode (advanced)

---

## Next Steps

1. ✅ Deploy your bot locally
2. ✅ Test all commands
3. ✅ Set up 24/7 running
4. 🔧 Customize conference sources (see README.md)
5. 🔧 Add your own filters
6. 🔧 Integrate with conference APIs
7. 🚀 Deploy to cloud for better uptime

---

**Need help?** Open an issue or contact support!
