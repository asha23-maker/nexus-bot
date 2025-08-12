# nexus_bot.py
import os
import json
import logging
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from nexus_content import NEXUS_DATA

# ----------------- ЛОГИ -----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("nexus-bot")

# ----------------- НАСТРОЙКИ -----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set! Add it in Railway → Variables.")

# Можно указать админа через переменную окружения ADMIN_ID, иначе берём дефолт.
ADMIN_ID = int(os.getenv("ADMIN_ID", "817635625"))

USERS_FILE = "users.json"   # здесь храним chat_id всех, кто писал боту

WELCOME_TEXT = (
    "🌐 *Welcome to Nexus Navigator Bot!*\n\n"
    "This bot helps newcomers learn the basics of Nexus.\n"
    "Vision & Mission, Architecture & Core Components, Community, Research & Leadership and useful links.\n\n"
    "*Choose a category:*"
)

# ----------------- ХРАНИЛКА ПОЛЬЗОВАТЕЛЕЙ -----------------
def load_users() -> List[int]:
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        logger.warning(f"Failed to load users.json: {e}")
        return []

def save_users(users: List[int]) -> None:
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f)
    except Exception as e:
        logger.error(f"Failed to save users.json: {e}")

def remember_user(chat_id: int) -> None:
    users = load_users()
    if chat_id not in users:
        users.append(chat_id)
        save_users(users)

# ----------------- КЛАВИАТУРЫ -----------------
def main_menu_markup() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton("🧭 How to start", callback_data="howto")],
        [InlineKeyboardButton("💡 Vision & Mission", callback_data="vision")],
        [InlineKeyboardButton("🏗️ Architecture", callback_data="architecture")],
        [InlineKeyboardButton("✨ Testnet III", callback_data="testnet")],
        [InlineKeyboardButton("🤝 Community & Team", callback_data="community")],
        [InlineKeyboardButton("📅 Events & Blog", callback_data="events")],
        [InlineKeyboardButton("🔗 Official Links", callback_data="links")],
        [InlineKeyboardButton("⚠️ Disclaimer", callback_data="disclaimer")],
    ]
    return InlineKeyboardMarkup(kb)

def back_menu_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back to menu", callback_data="back_to_menu")]]
    )

# ----------------- ХЕНДЛЕРЫ -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Регистрируем пользователя и показываем главное меню."""
    chat_id = update.effective_chat.id
    remember_user(chat_id)

    if update.message:  # обычный /start
        await update.message.reply_text(
            WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="Markdown"
        )
    elif update.callback_query:  # на всякий случай
        await update.callback_query.edit_message_text(
            WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="Markdown"
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем нажатия на инлайн-кнопки."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_menu":
        await query.edit_message_text(
            WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="Markdown"
        )
        return

    # Любая секция из NEXUS_DATA
    content = NEXUS_DATA.get(data)
    if content:
        await query.edit_message_text(
            text=content,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=back_menu_markup(),
        )
    else:
        await query.edit_message_text(
            WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="Markdown"
        )

async def register_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Любое сообщение от пользователя — запоминаем его chat_id (для рассылки)."""
    remember_user(update.effective_chat.id)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Рассылка всем пользователям (только для ADMIN_ID).
       Поддерживает многострочный текст: всё, что после '/broadcast' — идёт как сообщение.
    """
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not allowed to use this command.")
        return

    # Берём ВСЁ сообщение, убираем саму команду '/broadcast'
    full_text = update.message.text or ""
    msg = full_text[len("/broadcast"):].strip()

    if not msg:
        await update.message.reply_text(
            "Usage:\n/broadcast <your message>\n\n"
            "Можно с переносами строк. Пример:\n"
            "/broadcast Привет!\nСегодня апдейт:\n- Пункт 1\n- Пункт 2"
        )
        return

    users = load_users()
    sent = 0

    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg)
            sent += 1
        except Exception as e:
            logger.warning(f"Failed to send to {uid}: {e}")

    await update.message.reply_text(f"✅ Broadcast sent to {sent} users.")

# ----------------- MAIN -----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))

    # Инлайн-кнопки
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Любое НЕ-командное сообщение → регистрируем пользователя
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, register_any_message))

    logger.info("Nexus Bot started…")
    app.run_polling()

if __name__ == "__main__":
    main()
