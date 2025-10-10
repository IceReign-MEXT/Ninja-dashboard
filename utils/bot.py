import os
from dotenv import load_dotenv
import telebot

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ETH_WALLET = os.getenv("ETH_WALLET")
SOL_WALLET = os.getenv("SOL_WALLET")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN not loaded. Check your .env file.")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

# Command: /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome to ICEGODS 24/7 Tracker!\n\nCommands:\n"
        "/start - Main menu\n"
        "/profile - Your profile\n"
        "/bots - Manage your bots\n"
        "/buy - Buy subscription\n"
        "/free - Free trial\n"
        "/help - Help info"
    )

# Command: /profile
@bot.message_handler(commands=['profile'])
def profile(message):
    # In production, fetch user subscription from DB
    bot.send_message(
        message.chat.id,
        f"👤 Profile Info:\n"
        f"Name: {os.getenv('MAIN_ADMIN_NAME')}\n"
        f"Username: {os.getenv('MAIN_ADMIN_USERNAME')}\n"
        f"Subscription: Active\n"
        f"Registered: 2025-10-10"
    )

# Command: /buy
@bot.message_handler(commands=['buy'])
def buy(message):
    bot.send_message(
        message.chat.id,
        f"🛒 Subscription Options:\n"
        f"1️⃣ Monthly: $10\n"
        f"2️⃣ Yearly: $80\n\n"
        f"💰 Send payment to these wallets:\n"
        f"ETH: {ETH_WALLET}\n"
        f"SOL: {SOL_WALLET}\n\n"
        f"After payment, send /confirm to activate your subscription."
    )

# Command: /free
@bot.message_handler(commands=['free'])
def free(message):
    bot.send_message(
        message.chat.id,
        "🎁 Free Trial Activated for 3 Days! Enjoy limited access."
    )

# Command: /confirm
@bot.message_handler(commands=['confirm'])
def confirm(message):
    bot.send_message(
        message.chat.id,
        "✅ Subscription activated for 30 days!"
    )

# Command: /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ Help & Info:\n"
        "/start - Main menu\n"
        "/profile - Show profile info\n"
        "/bots - Manage your bots\n"
        "/buy - Buy subscription\n"
        "/free - Free trial\n"
        "/help - Help info"
    )

print("✅ ICEGODS Bot Running!")
bot.infinity_polling()
