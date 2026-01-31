"""
Telegram Bot for QA/IT Conference Discovery in Europe
Searches for conferences and notifies users about new events with early bird tickets
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import List, Dict
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Data storage files
CONFERENCES_FILE = 'conferences.json'
USERS_FILE = 'users.json'


class ConferenceBot:
    """Main bot class for conference discovery and notifications"""
    
    def __init__(self, token: str):
        self.token = token
        self.application = None
        
    def load_conferences(self) -> Dict:
        """Load conferences from storage"""
        try:
            with open(CONFERENCES_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_conferences(self, conferences: Dict):
        """Save conferences to storage"""
        with open(CONFERENCES_FILE, 'w') as f:
            json.dump(conferences, f, indent=2)
    
    def load_users(self) -> Dict:
        """Load user subscriptions from storage"""
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_users(self, users: Dict):
        """Save user subscriptions to storage"""
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        user = update.effective_user
        welcome_text = (
            f"👋 Hi {user.mention_html()}!\n\n"
            "I'm your QA & IT Conference Discovery Bot for Europe! 🚀\n\n"
            "Here's what I can do:\n"
            "• 🔍 Search for upcoming conferences\n"
            "• 🔔 Notify you about new conferences\n"
            "• 🎟️ Alert you about early bird tickets\n"
            "• 📍 Filter by country, topic, or date\n\n"
            "Commands:\n"
            "/search - Search for conferences\n"
            "/subscribe - Get notifications for new conferences\n"
            "/unsubscribe - Stop notifications\n"
            "/upcoming - Show upcoming conferences\n"
            "/help - Show help message\n"
        )
        await update.message.reply_html(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        help_text = (
            "📚 <b>Available Commands:</b>\n\n"
            "/start - Start the bot\n"
            "/search - Search for QA/IT conferences\n"
            "/subscribe - Enable notifications for new conferences\n"
            "/unsubscribe - Disable notifications\n"
            "/upcoming - View upcoming conferences (next 3 months)\n"
            "/filters - Set your preferences (countries, topics)\n"
            "/help - Show this help message\n\n"
            "<b>How to use:</b>\n"
            "1. Use /search to find conferences\n"
            "2. Use /subscribe to get notified about new ones\n"
            "3. Set your /filters to customize results\n"
        )
        await update.message.reply_html(help_text)
    
    async def search_conferences(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search for conferences using web search"""
        await update.message.reply_text("🔍 Searching for QA and IT conferences in Europe...\n\nThis may take a moment.")
        
        # Search queries for different types of conferences
        search_queries = [
            "QA testing conferences Europe 2025",
            "software testing conference Europe 2025",
            "IT conferences Europe 2025",
            "DevOps conferences Europe 2025",
            "tech conferences Europe 2025 early bird"
        ]
        
        all_results = []
        
        # Note: In a real implementation, you would use web_search here
        # For now, I'll create a structure showing how to process results
        
        message = (
            "📊 <b>Conference Search Results</b>\n\n"
            "To get real-time conference data, I need web search capabilities.\n\n"
            "In the meantime, here are some popular conference sources:\n\n"
            "🌐 <b>Conference Aggregators:</b>\n"
            "• <a href='https://confs.tech'>Confs.tech</a> - Tech conference calendar\n"
            "• <a href='https://conferenceindex.org'>Conference Index</a>\n"
            "• <a href='https://10times.com/technology'>10times</a> - Tech events\n\n"
            "🎯 <b>QA/Testing Specific:</b>\n"
            "• TestBash conferences\n"
            "• EuroSTAR Conference\n"
            "• Selenium Conference Europe\n\n"
            "💡 <b>Tip:</b> Use /upcoming to see manually added conferences, "
            "or use /subscribe to get notified when new ones are added!"
        )
        
        await update.message.reply_html(message, disable_web_page_preview=True)
    
    async def subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Subscribe to conference notifications"""
        user_id = str(update.effective_user.id)
        users = self.load_users()
        
        if user_id not in users:
            users[user_id] = {
                'subscribed': True,
                'filters': {
                    'countries': [],
                    'topics': ['QA', 'testing', 'IT', 'DevOps', 'software'],
                    'notify_early_bird': True
                },
                'subscribed_date': datetime.now().isoformat()
            }
        else:
            users[user_id]['subscribed'] = True
        
        self.save_users(users)
        
        await update.message.reply_text(
            "✅ You're now subscribed to conference notifications!\n\n"
            "You'll receive updates when:\n"
            "• New conferences are discovered\n"
            "• Early bird tickets become available\n"
            "• Important deadlines are approaching\n\n"
            "Use /filters to customize what you receive."
        )
    
    async def unsubscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unsubscribe from notifications"""
        user_id = str(update.effective_user.id)
        users = self.load_users()
        
        if user_id in users:
            users[user_id]['subscribed'] = False
            self.save_users(users)
            await update.message.reply_text("❌ You've been unsubscribed from notifications.")
        else:
            await update.message.reply_text("You weren't subscribed to notifications.")
    
    async def upcoming_conferences(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show upcoming conferences"""
        conferences = self.load_conferences()
        
        if not conferences:
            keyboard = [
                [InlineKeyboardButton("Add a Conference", callback_data='add_conference')],
                [InlineKeyboardButton("Search Online", callback_data='search_online')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "📭 No conferences in the database yet.\n\n"
                "You can help by adding conferences you know about!",
                reply_markup=reply_markup
            )
            return
        
        # Sort conferences by date
        sorted_conferences = sorted(
            conferences.items(),
            key=lambda x: x[1].get('start_date', '9999-12-31')
        )
        
        message = "📅 <b>Upcoming QA & IT Conferences in Europe</b>\n\n"
        
        for conf_id, conf in sorted_conferences[:10]:  # Show first 10
            name = conf.get('name', 'Unknown')
            country = conf.get('country', 'Unknown')
            city = conf.get('city', '')
            date = conf.get('start_date', 'TBA')
            early_bird = conf.get('early_bird_available', False)
            url = conf.get('url', '')
            
            location = f"{city}, {country}" if city else country
            
            message += f"🎯 <b>{name}</b>\n"
            message += f"📍 {location}\n"
            message += f"📆 {date}\n"
            
            if early_bird:
                message += "🎟️ <b>Early Bird Available!</b>\n"
            
            if url:
                message += f"🔗 <a href='{url}'>More Info</a>\n"
            
            message += "\n"
        
        await update.message.reply_html(message, disable_web_page_preview=True)
    
    async def set_filters(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Allow users to set notification filters"""
        keyboard = [
            [InlineKeyboardButton("🌍 Countries", callback_data='filter_countries')],
            [InlineKeyboardButton("🏷️ Topics", callback_data='filter_topics')],
            [InlineKeyboardButton("🎟️ Early Bird Only", callback_data='filter_earlybird')],
            [InlineKeyboardButton("✅ Done", callback_data='filter_done')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚙️ <b>Notification Filters</b>\n\n"
            "Customize what notifications you receive:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'add_conference':
            await query.edit_message_text(
                "To add a conference, send me the details in this format:\n\n"
                "Name: Conference Name\n"
                "Country: Country\n"
                "City: City (optional)\n"
                "Date: YYYY-MM-DD\n"
                "URL: https://... (optional)\n"
                "Early Bird: Yes/No"
            )
        
        elif query.data == 'search_online':
            await query.edit_message_text(
                "🔍 Searching online sources...\n\n"
                "Check these websites:\n"
                "• https://confs.tech\n"
                "• https://conferenceindex.org\n"
                "• https://10times.com/technology"
            )
        
        elif query.data.startswith('filter_'):
            await query.edit_message_text("Filter options coming soon!")
        
    async def check_new_conferences_job(self, context: ContextTypes.DEFAULT_TYPE):
        """Periodic job to check for new conferences and notify users"""
        logger.info("Checking for new conferences...")
        
        # This would use web search to find new conferences
        # For now, it's a placeholder for the periodic check
        
        users = self.load_users()
        subscribed_users = [
            user_id for user_id, data in users.items() 
            if data.get('subscribed', False)
        ]
        
        # If new conferences are found, notify subscribed users
        # Example notification:
        # for user_id in subscribed_users:
        #     await context.bot.send_message(
        #         chat_id=user_id,
        #         text="🆕 New conference found: ..."
        #     )
    
    def run(self):
        """Run the bot"""
        # Create application
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("search", self.search_conferences))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe))
        self.application.add_handler(CommandHandler("unsubscribe", self.unsubscribe))
        self.application.add_handler(CommandHandler("upcoming", self.upcoming_conferences))
        self.application.add_handler(CommandHandler("filters", self.set_filters))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Add periodic job to check for new conferences (every 12 hours)
        job_queue = self.application.job_queue
        job_queue.run_repeating(
            self.check_new_conferences_job,
            interval=timedelta(hours=12),
            first=timedelta(seconds=10)
        )
        
        # Start the bot
        logger.info("Starting bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main function to start the bot"""
    # Get token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("\nTo set it:")
        print("  export TELEGRAM_BOT_TOKEN='your-token-here'")
        return
    
    # Create and run bot
    bot = ConferenceBot(token)
    bot.run()


if __name__ == '__main__':
    main()

    from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "your-telegram-bot-token"

def my_callback(context):
    # Example callback code
    print("Job running!")

app = ApplicationBuilder().token(TOKEN).build()

# JobQueue is automatically available
job_queue = app.job_queue

# Run a repeating job every hour (3600 seconds)
job_queue.run_repeating(my_callback, interval=3600)

app.run_polling()

