import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ETH_WALLET = os.getenv("ETH_WALLET")
SOL_WALLET = os.getenv("SOL_WALLET")
FREE_TRIAL_DAYS = int(os.getenv("FREE_TRIAL_DAYS", 3))
MONTHLY_SUBSCRIPTION = int(os.getenv("MONTHLY_SUBSCRIPTION", 10))
YEARLY_SUBSCRIPTION = int(os.getenv("YEARLY_SUBSCRIPTION", 80))

if not BOT_TOKEN:
    print("❌ BOT_TOKEN not found in .env")
    exit()

# Handlers
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Buy Subscription", callback_data='buy')],
        [InlineKeyboardButton("Free Trial", callback_data='free')],
        [InlineKeyboardButton("Profile", callback_data='profile')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("👋 Welcome to ICEGODS 24/7 Tracker!", reply_markup=reply_markup)

def buy(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"🛒 Subscription Options:\n1️⃣ Monthly: ${MONTHLY_SUBSCRIPTION}\n2️⃣ Yearly: ${YEARLY_SUBSCRIPTION}\n\n"
        f"💰 Send payment to this wallet:\nETH: {ETH_WALLET}\nSOL: {SOL_WALLET}\nAfter payment, send /confirm to activate."
    )

def free(update: Update, context: CallbackContext):
    update.message.reply_text(f"🎁 Free Trial Activated for {FREE_TRIAL_DAYS} days!")

def profile(update: Update, context: CallbackContext):
    update.message.reply_text("👤 Profile Info:\nName: Mex Robert\nUsername: @RobertSmithETH\nSubscription: None\nRegistered: 2025-10-10")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/start - Main menu\n/profile - Show profile\n/buy - Subscribe\n/free - Trial\n/help - Help info"
    )

updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('buy', buy))
updater.dispatcher.add_handler(CommandHandler('free', free))
updater.dispatcher.add_handler(CommandHandler('profile', profile))
updater.dispatcher.add_handler(CommandHandler('help', help_command))

print("✅ ICEGODS Bot Running!")
updater.start_polling()
updater.idle()
