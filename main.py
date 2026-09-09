"""
main.py

Main entry point for CodeInsight AI.
Starts Telegram Bot polling and optional Web Dashboard server.
"""

import sys
import logging
import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.handlers import start_command, help_command, upload_command
from bot.upload_handler import handle_document

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def run_telegram_bot() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        logger.warning(
            "TELEGRAM_BOT_TOKEN is missing or set to placeholder. "
            "Bot mode will not run until token is configured in .env."
        )
        return

    # Ensure an active asyncio event loop exists (required for Python 3.10+)
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    max_upload_mb = int(os.getenv("MAX_UPLOAD_SIZE_MB", "500"))
    upload_dir = os.getenv("UPLOAD_DIR", "data/uploads")

    application = Application.builder().token(token).build()
    application.bot_data["max_upload_mb"] = max_upload_mb
    application.bot_data["upload_dir"] = upload_dir

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("upload", upload_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    logger.info("CodeInsight AI Telegram Bot starting...")
    application.run_polling(allowed_updates=["message"])


def run_web_server():
    import uvicorn
    from web.server import app
    host = os.getenv("WEB_HOST", "0.0.0.0")
    port = int(os.getenv("WEB_PORT", "8000"))
    logger.info("CodeInsight AI Web Server starting on %s:%s ...", host, port)
    uvicorn.run(app, host=host, port=port)


def main() -> None:
    load_dotenv()
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        run_web_server()
    else:
        run_telegram_bot()


if __name__ == "__main__":
    main()
