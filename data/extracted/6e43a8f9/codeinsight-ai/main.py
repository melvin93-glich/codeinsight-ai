"""
main.py

Entry point for CodeInsight AI.

Responsibilities:
1. Load environment variables (.env)
2. Build the Telegram Application
3. Register command handlers
4. Start polling for updates

Run with:
    python main.py
"""

import logging
import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

from bot.handlers import start_command, help_command, upload_command

# --- Logging setup -----------------------------------------------------
# INFO level shows normal operation; switch to DEBUG while troubleshooting.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    # --- Load secrets from .env into os.environ ---
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is missing or still set to the placeholder. "
            "Get a token from @BotFather and put it in your .env file."
        )

    max_upload_mb = int(os.getenv("MAX_UPLOAD_SIZE_MB", "500"))

    # --- Build the bot application ---
    # Application is the core object: it owns the event loop, the
    # dispatcher (which routes updates to handlers), and the bot client.
    application = Application.builder().token(token).build()

    # Shared data available to every handler via context.bot_data
    application.bot_data["max_upload_mb"] = max_upload_mb

    # --- Register handlers ---
    # CommandHandler matches messages that start with a specific "/command".
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("upload", upload_command))

    # --- Start polling ---
    # run_polling() repeatedly asks Telegram's servers for new updates,
    # blocking here until you stop the process (Ctrl+C).
    logger.info("CodeInsight AI is starting (polling mode)...")
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
