#!/usr/bin/env python3
"""
QA & IT Conference Discovery Telegram Bot
With country and direction filtering for local deployment
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states for filter selection
SELECTING_COUNTRY, SELECTING_DIRECTION = range(2)

# Available filters
COUNTRIES = [
    "🇺🇸 USA", "🇬🇧 UK", "🇩🇪 Germany", "🇵🇱 Poland", 
    "🇳🇱 Netherlands", "🇪🇸 Spain", "🇫🇷 France", "🇮🇹 Italy",
    "🇨🇦 Canada", "🇦🇺 Australia", "🌍 Online", "🌎 All Countries"
]

DIRECTIONS = [
    "🔄 Agile", "🚀 DevOps", "🧪 Testing/QA", "☁️ Cloud",
    "🔒 Security", "📊 Data Science", "🤖 AI/ML", "📱 Mobile",
    "🌐 Web Development", "🏗️ Architecture", "💼 Management", "✨ All Directions"
]


class ConferenceBot:
    """Main bot class for conference discovery"""
    
    def __init__(self, token: str):
        """Initialize the bot with token"""
        self.token = token
        self.conferences_file = 'conferences.json'
        self.users_file = 'users.json'
        self.application = Application.builder().token(token).build()
        
        # Load or initialize data
        self.conferences = self._load_json(self.conferences_file, self._get_sample_conferences())
        self.users = self._load_json(self.users_file, {})
        
        # Register handlers
        self._register_handlers()
    
    def _get_sample_conferences(self) -> dict:
        """Get sample conferences - replace with your data source"""
        return {
            "1": {
                "id": "1",
                "name": "Agile Testing Days",
                "date": "2026-03-15",
                "location": "Berlin",
                "country": "Germany",
                "directions": ["agile", "testing"],
                "url": "https://agiletestingdays.com",
                "description": "Annual agile testing conference"
            },
            "2": {
                "id": "2",
                "name": "DevOps World",
                "date": "2026-04-20",
                "location": "San Francisco",
                "country": "USA",
                "directions": ["devops", "cloud"],
                "url": "https://devopsworld.com",
                "description": "Leading DevOps conference"
            },
            "3": {
                "id": "3",
                "name": "QA Global Summit",
                "date": "2026-05-10",
                "location": "Virtual",
                "country": "Online",
                "directions": ["testing", "qa"],
                "url": "https://qasummit.com",
                "description": "Virtual QA conference"
            },
            "4": {
                "id": "4",
                "name": "Cloud Native Conference",
                "date": "2026-06-12",
                "location": "London",
                "country": "UK",
                "directions": ["cloud", "devops", "architecture"],
                "url": "https://cloudnativecon.com",
                "description": "Cloud-native technologies"
            },
            "5": {
                "id": "5",
                "name": "Security & Testing Summit",
                "date": "2026-07-08",
                "location": "Warsaw",
                "country": "Poland",
                "directions": ["security", "testing"],
                "url": "https://sectesting.com",
                "description": "Security testing conference"
            }
        }
    
    def _load_json(self, filename: str, default: dict) -> dict:
        """Load JSON data from file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
        return default
    
    def _save_json(self, filename: str, data: dict):
        """Save JSON data to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving {filename}: {e}")
    
    def _register_handlers(self):
        """Register all command and callback handlers"""
        
        # Conversation handler for filter setup
        filter_conv = ConversationHandler(
            entry_points=[CommandHandler('filters', self.filters_command)],
            states={
                SELECTING_COUNTRY: [CallbackQueryHandler(self.select_country)],
                SELECTING_DIRECTION: [CallbackQueryHandler(self.select_direction)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel_command)],
        )
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("search", self.search_command))
        self.application.add_handler(CommandHandler("upcoming", self.upcoming_command))
        self.application.add_handler(CommandHandler("list", self.list_command))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe_command))
        self.application.add_handler(CommandHandler("unsubscribe", self.unsubscribe_command))
        self.application.add_handler(CommandHandler("myfilters", self.myfilters_command))
        self.application.add_handler(filter_conv)
        
        # Callback query handler for other buttons
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Add periodic job to check for new conferences (every 12 hours)
        if self.application.job_queue:
            self.application.job_queue.run_repeating(
                self.check_new_conferences_job,
                interval=timedelta(hours=12),
                first=timedelta(seconds=10)
            )
    
    def _matches_filters(self, conference: dict, user_filters: dict) -> bool:
        """Check if conference matches user filters"""
        countries = user_filters.get('countries', [])
        directions = user_filters.get('directions', [])
        
        # If "All" is selected, match everything
        if "🌎 All Countries" in countries and "✨ All Directions" in directions:
            return True
        
        # Check country match
        country_match = "🌎 All Countries" in countries or any(
            c.split()[-1].lower() in conference['country'].lower() 
            for c in countries
        )
        
        # Check direction match
        direction_match = "✨ All Directions" in directions or any(
            d.split()[1].lower() in [dir.lower() for dir in conference['directions']]
            for d in directions
        )
        
        return country_match and direction_match
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = str(update.effective_user.id)
        user = update.effective_user
        
        # Initialize user if new
        if user_id not in self.users:
            self.users[user_id] = {
                'subscribed': False,
                'filters': {
                    'countries': ["🌎 All Countries"],
                    'directions': ["✨ All Directions"]
                }
            }
            self._save_json(self.users_file, self.users)
        
        welcome_message = f"""
👋 Welcome to Conference Bot, {user.first_name}!

I'll help you discover QA & IT conferences matching your interests.

**Available Commands:**
/filters - Set your country and direction preferences
/list - View conferences matching your filters
/upcoming - View upcoming conferences (next 3 months)
/myfilters - View your current filter settings
/subscribe - Enable notifications about new conferences
/unsubscribe - Disable notifications
/help - Show this help message

🎯 Get started by setting your filters: /filters
        """
        
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 **How to Use Conference Bot**

1️⃣ **Set Your Filters** - /filters
   • Choose countries you're interested in
   • Select conference directions (Agile, DevOps, Testing, etc.)

2️⃣ **View Conferences** - /list
   • See all conferences matching your filters
   • Click on URLs for more details

3️⃣ **Manage Notifications**
   • /subscribe - Get notified about new conferences
   • /unsubscribe - Stop notifications

4️⃣ **Check Settings** - /myfilters
   • View your current filter preferences

**Available Filters:**
🌍 Countries: USA, UK, Germany, Poland, Netherlands, Spain, France, Italy, Canada, Australia, Online, All
🎯 Directions: Agile, DevOps, Testing/QA, Cloud, Security, Data Science, AI/ML, Mobile, Web, Architecture, Management, All

**Tips:**
• Select "All Countries" or "All Directions" to see everything
• You can select multiple options
• Update filters anytime with /filters
        """
        await update.message.reply_text(help_text)
    
    async def filters_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start filter selection process"""
        keyboard = []
        for i in range(0, len(COUNTRIES), 2):
            row = [
                InlineKeyboardButton(COUNTRIES[i], callback_data=f"country_{COUNTRIES[i]}")
            ]
            if i + 1 < len(COUNTRIES):
                row.append(
                    InlineKeyboardButton(COUNTRIES[i+1], callback_data=f"country_{COUNTRIES[i+1]}")
                )
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("✅ Done", callback_data="country_done")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Initialize context data
        context.user_data['selected_countries'] = []
        
        message = "🌍 **Select Countries** (choose one or more):"
        
        if update.message:
            await update.message.reply_text(message, reply_markup=reply_markup)
        else:
            await update.callback_query.message.reply_text(message, reply_markup=reply_markup)
        
        return SELECTING_COUNTRY
    
    async def select_country(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle country selection"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "country_done":
            selected = context.user_data.get('selected_countries', [])
            if not selected:
                selected = ["🌎 All Countries"]
                context.user_data['selected_countries'] = selected
            
            # Move to direction selection
            keyboard = []
            for i in range(0, len(DIRECTIONS), 2):
                row = [
                    InlineKeyboardButton(DIRECTIONS[i], callback_data=f"direction_{DIRECTIONS[i]}")
                ]
                if i + 1 < len(DIRECTIONS):
                    row.append(
                        InlineKeyboardButton(DIRECTIONS[i+1], callback_data=f"direction_{DIRECTIONS[i+1]}")
                    )
                keyboard.append(row)
            
            keyboard.append([InlineKeyboardButton("✅ Done", callback_data="direction_done")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            context.user_data['selected_directions'] = []
            
            await query.edit_message_text(
                "🎯 **Select Directions** (choose one or more):",
                reply_markup=reply_markup
            )
            return SELECTING_DIRECTION
        
        else:
            # Toggle country selection
            country = query.data.replace("country_", "")
            selected = context.user_data.get('selected_countries', [])
            
            # Handle "All Countries" logic
            if country == "🌎 All Countries":
                selected = ["🌎 All Countries"]
            else:
                if "🌎 All Countries" in selected:
                    selected.remove("🌎 All Countries")
                
                if country in selected:
                    selected.remove(country)
                else:
                    selected.append(country)
            
            context.user_data['selected_countries'] = selected
            
            selected_text = ", ".join(selected) if selected else "None"
            await query.answer(f"Selected: {selected_text}")
            
            return SELECTING_COUNTRY
    
    async def select_direction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle direction selection"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "direction_done":
            selected = context.user_data.get('selected_directions', [])
            if not selected:
                selected = ["✨ All Directions"]
                context.user_data['selected_directions'] = selected
            
            # Save preferences
            countries = context.user_data.get('selected_countries', ["🌎 All Countries"])
            directions = selected
            
            user_id = str(update.effective_user.id)
            
            if user_id not in self.users:
                self.users[user_id] = {'subscribed': False, 'filters': {}}
            
            self.users[user_id]['filters'] = {
                'countries': countries,
                'directions': directions
            }
            self._save_json(self.users_file, self.users)
            
            await query.edit_message_text(
                f"✅ **Filters Saved!**\n\n"
                f"🌍 Countries: {', '.join(countries)}\n"
                f"🎯 Directions: {', '.join(directions)}\n\n"
                f"Use /list to see matching conferences!"
            )
            
            return ConversationHandler.END
        
        else:
            # Toggle direction selection
            direction = query.data.replace("direction_", "")
            selected = context.user_data.get('selected_directions', [])
            
            # Handle "All Directions" logic
            if direction == "✨ All Directions":
                selected = ["✨ All Directions"]
            else:
                if "✨ All Directions" in selected:
                    selected.remove("✨ All Directions")
                
                if direction in selected:
                    selected.remove(direction)
                else:
                    selected.append(direction)
            
            context.user_data['selected_directions'] = selected
            
            selected_text = ", ".join(selected) if selected else "None"
            await query.answer(f"Selected: {selected_text}")
            
            return SELECTING_DIRECTION
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel filter selection"""
        await update.message.reply_text("❌ Filter selection cancelled.")
        return ConversationHandler.END
    
    async def myfilters_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user's current filters"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.users:
            self.users[user_id] = {
                'subscribed': False,
                'filters': {
                    'countries': ["🌎 All Countries"],
                    'directions': ["✨ All Directions"]
                }
            }
            self._save_json(self.users_file, self.users)
        
        user_data = self.users[user_id]
        countries = user_data['filters'].get('countries', ["🌎 All Countries"])
        directions = user_data['filters'].get('directions', ["✨ All Directions"])
        subscribed = user_data.get('subscribed', False)
        
        status = "✅ Active" if subscribed else "❌ Inactive"
        
        text = f"""
📋 **Your Current Filters**

🌍 **Countries:** {', '.join(countries)}
🎯 **Directions:** {', '.join(directions)}
🔔 **Notifications:** {status}

Use /filters to change your preferences.
        """
        await update.message.reply_text(text)
    
    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List conferences matching user filters"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.users:
            self.users[user_id] = {
                'subscribed': False,
                'filters': {
                    'countries': ["🌎 All Countries"],
                    'directions': ["✨ All Directions"]
                }
            }
        
        user_filters = self.users[user_id]['filters']
        
        # Filter conferences
        matching = [
            conf for conf in self.conferences.values()
            if self._matches_filters(conf, user_filters)
        ]
        
        if not matching:
            await update.message.reply_text(
                "😔 No conferences found matching your filters.\n\n"
                "Try adjusting your filters with /filters"
            )
            return
        
        # Sort by date
        matching.sort(key=lambda x: x['date'])
        
        response = f"📅 **Conferences Matching Your Filters** ({len(matching)} found)\n\n"
        
        for conf in matching[:10]:  # Show max 10
            response += f"**{conf['name']}**\n"
            response += f"📍 {conf['location']}, {conf['country']}\n"
            response += f"📆 {conf['date']}\n"
            response += f"🎯 {', '.join(conf['directions'])}\n"
            response += f"🔗 {conf['url']}\n\n"
        
        if len(matching) > 10:
            response += f"_...and {len(matching) - 10} more conferences_"
        
        await update.message.reply_text(response)
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search command - alias for /list"""
        await self.list_command(update, context)
    
    async def upcoming_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /upcoming command - show conferences in next 3 months"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.users:
            user_filters = {
                'countries': ["🌎 All Countries"],
                'directions': ["✨ All Directions"]
            }
        else:
            user_filters = self.users[user_id]['filters']
        
        upcoming = []
        now = datetime.now()
        three_months = now + timedelta(days=90)
        
        for conf in self.conferences.values():
            try:
                conf_date = datetime.strptime(conf['date'], '%Y-%m-%d')
                if now <= conf_date <= three_months and self._matches_filters(conf, user_filters):
                    upcoming.append(conf)
            except:
                pass
        
        if not upcoming:
            await update.message.reply_text(
                "📅 No conferences scheduled in the next 3 months matching your filters.\n"
                "Use /subscribe to get notified when new ones are added!"
            )
            return
        
        response = "📅 **Upcoming Conferences** (Next 3 Months)\n\n"
        for conf in upcoming[:10]:  # Show max 10
            response += f"**{conf['name']}**\n"
            response += f"📍 {conf['location']}\n"
            response += f"📆 {conf['date']}\n"
            response += f"🔗 {conf['url']}\n\n"
        
        await update.message.reply_text(response)
    
    async def subscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /subscribe command"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.users:
            self.users[user_id] = {
                'subscribed': False,
                'filters': {
                    'countries': ["🌎 All Countries"],
                    'directions': ["✨ All Directions"]
                }
            }
        
        self.users[user_id]['subscribed'] = True
        self._save_json(self.users_file, self.users)
        
        await update.message.reply_text(
            "✅ You're now subscribed to conference notifications!\n"
            "You'll receive updates about new conferences matching your filters.\n\n"
            "Use /filters to customize your preferences.\n"
            "Use /unsubscribe to stop notifications."
        )
    
    async def unsubscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /unsubscribe command"""
        user_id = str(update.effective_user.id)
        
        if user_id in self.users:
            self.users[user_id]['subscribed'] = False
            self._save_json(self.users_file, self.users)
        
        await update.message.reply_text(
            "❌ You've been unsubscribed from notifications.\n"
            "Use /subscribe anytime to enable them again."
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
    
    async def check_new_conferences_job(self, context: ContextTypes.DEFAULT_TYPE):
        """Background job to check for new conferences"""
        logger.info("Checking for new conferences...")
        
        # TODO: Implement your conference fetching logic here
        # This is where you'd scrape websites or call APIs
        
        # Example: Notify subscribed users about new conferences
        for user_id_str, user_data in self.users.items():
            if not user_data.get('subscribed', False):
                continue
            
            try:
                user_id = int(user_id_str)
                # TODO: Send notification if new conferences match user's filters
                # await context.bot.send_message(user_id, "New conference available!")
            except Exception as e:
                logger.error(f"Error notifying user {user_id_str}: {e}")
    
    def run_polling(self):
        """Run bot with polling (for local deployment)"""
        logger.info("Starting Conference Bot with polling...")
        self.application.run_polling(drop_pending_updates=True)


def main():
    """Main function to run the bot"""
    # Get token from environment variable
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set it using: export TELEGRAM_BOT_TOKEN='your-bot-token'")
        print("Or add it to your .env file")
        return
    
    try:
        # Initialize and run bot
        bot = ConferenceBot(TOKEN)
        bot.run_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
    finally:
        logger.info("Bot shutdown complete")


if __name__ == '__main__':
    main()
