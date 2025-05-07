# notifier.py
import telebot
import os
import json

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_IDS_FILE = "chat_ids.json"

# Validate environment variables
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def load_chat_ids():
    """Load chat IDs from JSON file."""
    try:
        if os.path.exists(CHAT_IDS_FILE):
            with open(CHAT_IDS_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading chat IDs: {e}")
        return []

def save_chat_ids(chat_ids):
    """Save chat IDs to JSON file."""
    try:
        with open(CHAT_IDS_FILE, 'w') as f:
            json.dump(chat_ids, f)
    except Exception as e:
        print(f"Error saving chat IDs: {e}")

chat_ids = load_chat_ids()

def send_telegram_notification(message: str):
    """Send a notification message to all subscribed chats."""
    current_chat_ids = load_chat_ids()
    for chat_id in current_chat_ids:
        try:
            bot.send_message(chat_id, message)
        except Exception as e:
            print(f"Error sending to {chat_id}: {e}")

@bot.message_handler(commands=['chatid'])
def handle_chatid(message: telebot.types.Message) -> None:
    bot.reply_to(message, f"Your chat id is {message.chat.id}")

@bot.message_handler(commands=['start'])
def handle_start(message: telebot.types.Message):
    """Add user to notification list on /start command."""
    chat_id = message.chat.id
    current_chat_ids = load_chat_ids()
    
    if chat_id not in current_chat_ids:
        current_chat_ids.append(chat_id)
        save_chat_ids(current_chat_ids)
        reply = "✅ Вы подписаны на уведомления о новых устройствах!"
    else:
        reply = "ℹ️ Вы уже подписаны на обновления."
        
    bot.reply_to(message, reply)

def start_bot():
    """Runs the Telegram bot polling"""
    bot.infinity_polling()

if __name__ == "__main__":
    start_bot()