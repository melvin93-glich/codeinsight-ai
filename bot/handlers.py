"""
bot/handlers.py

Telegram command handlers for CodeInsight AI.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /start command."""
    user = update.effective_user
    logger.info("User %s (%s) started the bot", user.id, user.first_name)

    welcome_message = (
        f"👋 Hi {user.first_name}!\n\n"
        "I'm *CodeInsight AI* — send me a ZIP file of your project "
        "and I'll produce a comprehensive 24-section technical report (Markdown + PDF).\n\n"
        "**Features Analyzed:**\n"
        "• Executive Summary & Tech Stack\n"
        "• AI/LLM Models, Providers, RAG & Vector DBs\n"
        "• Secret Detection & Security Vulnerabilities\n"
        "• Architecture, DB, APIs & Deployment\n"
        "• Code Quality Scores & Generated README\n\n"
        "Use /help to see options, or simply upload a `.zip` archive to begin!"
    )

    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /help command."""
    help_message = (
        "*Available commands:*\n\n"
        "/start — Welcome message & overview\n"
        "/help — Show usage instructions\n"
        "/upload — How to upload a project\n\n"
        "*How to use:* \n"
        "1. Zip your project source folder\n"
        "2. Upload the `.zip` file directly into this chat\n"
        "3. Wait while CodeInsight AI extracts, scans, and analyzes your codebase\n"
        "4. Download your complete 24-section Markdown & PDF report!"
    )
    await update.message.reply_text(help_message, parse_mode="Markdown")


async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /upload command."""
    max_upload_mb = context.bot_data.get("max_upload_mb", 500)
    await update.message.reply_text(
        "📦 Just drag & drop or send your `.zip` file directly in this chat!\n"
        f"Maximum allowed size: {max_upload_mb} MB."
    )
