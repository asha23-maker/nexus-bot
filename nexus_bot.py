# nexus_bot.py
import os
import logging
import feedparser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
from nexus_content import NEXUS_DATA

# --- Настройки ---
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN is not set! Please configure it in Railway.")

SUBSCRIBERS_FILE = "subscribers.txt"
LAST_TWEET_FILE = "last_tweet.txt"
NITTER_RSS = "https://nitter.net/NexusLabs/rss"

# --- Логирование ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("nexus-bot")

WELCOME_TEXT = (
    "🌐 *Welcome to Nexus Navigator Bot!*\n\n"
    "This bot helps newcomers learn the basics of Nexus.\n"
    "Vision & Mission, Architecture & Core Components, Community, Research & Leadership and useful links.\n\n"
    "*Choose a category:*"
)

# --- Кнопки ---
def back_menu_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to menu", callback_data="back_to_menu")]])

def main_menu_markup() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton("🧭 How to start", callback_data="howto")],
        [InlineKeyboardButton("💡 Vision & Mission", callback_data="vision")],
        [InlineKeyboardButton("🏗️ Architecture", callback_data="architecture")],
        [InlineKeyboardButton("✨ Testnet III", callback_data="testnet")],
        [InlineKeyboardButton("🤝 Community & Team", callback_data="community")],
        [InlineKeyboardButton("📅 Events & Blog", callback_data="events")],
        [InlineKeyboardButton("🔗 Official Links", callback_data="links")],
        [InlineKeyboardButton("📣 Subscribe to Post Alerts", callback_data="subscribe")],
        [InlineKeyboardButton("⚠️ Disclaimer", callback_data="disclaimer")],
    ]
    return InlineKeyboardMarkup(kb)

# --- Подписки ---
def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        return []

def save_subscriber(user_id):
    subs = set(load_subscribers())
    if user_id not in subs:
        with open(SUBSCRIBERS_FILE, "a", encoding="utf-8") as f:
            f.write(user_id + "\n")

def remove_subscriber(user_id):
    subs = set(load_subscribers())
    if user_id in subs:
        subs.remove(user_id)
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
            for s in subs:
                f.write(s + "\n")

# --- Храним последний твит ---
def get_last_tweet_link():
    try:
        with open(LAST_TWEET_FILE, "r", encoding="utf-8") as f:
            return f.read().strip() or None
    except FileNotFoundError:
        return None

def set_last_tweet_link(link):
    with open(LAST_TWEET_FILE, "w", encoding="utf-8") as f:
        f.write(link)

# --- Обработчики ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_menu":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="Markdown")
        return

    if data == "subscribe":
        sub_kb = [
            [InlineKeyboardButton("🔔 Yes", callback_data="subscribe_yes"),
             InlineKeyboardButton("🚫 No", callback_data="subscribe_no")],
            [InlineKeyboardButton("🔙 Back to menu", callback_data="back_to_menu")],
        ]
        await query.edit_message_text(NEXUS_DATA.get("subscribe", "Subscribe to updates."),
                                      parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(sub_kb))
        return

    if data == "subscribe_yes":
        save_subscriber(str(query.from_user.id))
        await query.edit_message_text("✅ You are now subscribed to Nexus Twitter post alerts!",
                                      reply_markup=back_menu_markup())
        return

    if data == "subscribe_no":
        remove_subscriber(str(query.from_user.id))
        await query.edit_message_text("🚫 You’ve unsubscribed from post alerts.",
                                      reply_markup=back_menu_markup())
        return

    content = NEXUS_DATA.get(data)
    if content:
        await query.edit_message_text(content, parse_mode="Markdown",
                                      disable_web_page_preview=True,
                                      reply_markup=back_menu_markup())
    else:
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="Markdown")

# --- Проверка твитов ---
async def check_twitter_updates(context: ContextTypes.DEFAULT_TYPE):
    try:
        feed = feedparser.parse(NITTER_RSS)
        if not feed.entries:
            return

        latest = feed.entries[0]
        new_link = latest.link.strip()
        last = get_last_tweet_link()

        if new_link and new_link != last:
            set_last_tweet_link(new_link)
            text = f"🆕 *New Nexus Twitter Post!*\n\n{latest.title}\n{new_link}"
            for uid in load_subscribers():
                try:
                    await context.bot.send_message(chat_id=uid, text=text, parse_mode="Markdown")
                except Exception as e:
                    logger.warning(f"Failed to send to {uid}: {e}")
    except Exception as e:
        logger.error(f"check_twitter_updates error: {e}")

# --- Запуск бота ---
def main():
    logger.info("Starting Nexus Bot...")

    # Проверка файла с подписчиками при старте
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            logger.info(f"Subscribers file content:\n{f.read()}")
    else:
        logger.info("Subscribers file not found.")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.job_queue.run_repeating(check_twitter_updates, interval=180, first=10)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
