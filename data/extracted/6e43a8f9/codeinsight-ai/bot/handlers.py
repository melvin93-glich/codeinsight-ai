"""
bot/handlers.py

Contains all Telegram command handlers for CodeInsight AI.
Each handler is an async function that receives an `update`
(the incoming message) and a `context` (bot-wide state/utilities).
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

# Logger for this module — Phase 16 will centralize logging config,
# for now this gives us visibility into what the bot is doing.
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /start command.

    Telegram sends this automatically when a user opens the bot
    for the first time, or when they type /start manually.
    """
    user = update.effective_user
    logger.info("User %s (%s) started the bot", user.id, user.first_name)

    welcome_message = (
        f"👋 Hi {user.first_name}!\n\n"
        "I'm *CodeInsight AI* — send me a ZIP file of your project "
        "and I'll analyze it: tech stack, AI/LLM usage, security issues, "
        "architecture, and generate a full report (Markdown + PDF).\n\n"
        "Use /help to see what I can do, or just send a .zip file to begin."
    )

    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /help command — lists available commands and usage.
    """
    help_message = (
        "*Available commands:*\n\n"
        "/start — Introduction and welcome message\n"
        "/help — Show this help message\n"
        "/upload — Instructions for uploading a project\n\n"
        "*How to use me:*\n"
        "1. Zip your project folder\n"
        "2. Send the .zip file directly in this chat\n"
        "3. Wait while I scan it\n"
        "4. Receive a full technical report (Markdown + PDF)"
    )
    await update.message.reply_text(help_message, parse_mode="Markdown")


async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /upload command — explains how to send a project.

    NOTE: This does not yet handle the actual file. Receiving and
    processing the ZIP itself is built in Phase 3 (ZIP Upload) using
    a MessageHandler for documents, not a CommandHandler.
    """
    await update.message.reply_text(
        "📦 Just send me a .zip file directly in this chat — "
        "no command needed. I'll detect it automatically.\n\n"
        f"Max size: {context.bot_data.get('max_upload_mb', 500)} MB."
    )
