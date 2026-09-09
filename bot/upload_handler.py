"""
bot/upload_handler.py

Telegram upload handler for processing project ZIP files,
executing extraction, scanning, AI deep analysis, and delivering
both Markdown and PDF technical reports back to the user.
"""

import logging
import os
import uuid
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from core.extractor import ZipExtractor
from core.scanner import CodeScanner
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.ai_analyzer import AIAnalyzer
from reports.markdown_reporter import MarkdownReporter
from reports.pdf_reporter import PDFReporter

logger = logging.getLogger(__name__)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Triggered when a document/file is uploaded to the Telegram bot.
    """
    document = update.message.document
    if document is None:
        await update.message.reply_text("⚠️ Unable to read file. Please upload a valid .zip archive.")
        return

    file_name = document.file_name or "project.zip"
    max_upload_mb = context.bot_data.get("max_upload_mb", 500)
    upload_dir = Path(context.bot_data.get("upload_dir", "data/uploads"))

    # Validation 1: Check extension
    if not file_name.lower().endswith(".zip"):
        await update.message.reply_text(
            "❌ Only .zip files are supported.\n"
            "Please compress your project directory into a ZIP archive and send it again."
        )
        return

    # Validation 2: Check file size
    file_size_mb = (document.file_size or 0) / (1024 * 1024)
    if file_size_mb > max_upload_mb:
        await update.message.reply_text(
            f"❌ File size ({file_size_mb:.1f} MB) exceeds maximum allowed size of {max_upload_mb} MB."
        )
        return

    status_msg = await update.message.reply_text("📥 Received your ZIP archive. Downloading...")

    # Unique project execution ID
    project_id = uuid.uuid4().hex[:8]
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination_zip = upload_dir / f"{project_id}_{file_name}"

    try:
        telegram_file = await context.bot.get_file(document.file_id)
        await telegram_file.download_to_drive(custom_path=str(destination_zip))
    except Exception as exc:
        logger.exception("Failed to download file from Telegram")
        await status_msg.edit_text("⚠️ Network error while downloading file from Telegram. Please try again.")
        return

    try:
        # Step 1: Extraction
        await status_msg.edit_text("📦 Extracting ZIP archive safely...")
        extractor = ZipExtractor(extract_base_dir="data/extracted")
        extracted_dir = extractor.extract_zip(str(destination_zip), project_id)

        # Step 2: Static Code Scanning
        await status_msg.edit_text("🔍 Scanning file structure, dependencies, and code patterns...")
        scanner = CodeScanner(extracted_dir)
        raw_scan = scanner.scan()

        # Step 3: Pre-process Context
        analysis_context = StaticAnalyzer.analyze(raw_scan)

        # Step 4: AI Deep Analysis (24 Sections)
        await status_msg.edit_text("🤖 Generating 24-section AI technical report...")
        ai_analyzer = AIAnalyzer()
        markdown_report = ai_analyzer.generate_report(analysis_context)

        # Step 5: Report Compilation (Markdown & PDF)
        await status_msg.edit_text("📄 Compiling Markdown & PDF report files...")
        md_reporter = MarkdownReporter(output_dir="data/reports")
        pdf_reporter = PDFReporter(output_dir="data/reports")

        md_file = md_reporter.save_report(markdown_report, project_id)
        pdf_file = pdf_reporter.generate_pdf(markdown_report, project_id)

        # Send completion message & report files
        await status_msg.edit_text(
            "✅ **Analysis Complete!**\n\n"
            f"• **Project**: `{raw_scan['project_name']}`\n"
            f"• **Primary Language**: `{raw_scan['primary_language']}`\n"
            f"• **Files Scanned**: `{raw_scan['total_files']}`\n"
            f"• **Lines of Code**: `~{raw_scan['total_lines']}`\n\n"
            "Sending full report documents below..."
        )

        # Send PDF file
        with open(pdf_file, "rb") as pf:
            await update.message.reply_document(
                document=pf,
                filename=f"CodeInsight_Report_{raw_scan['project_name']}.pdf",
                caption="📄 Complete PDF Analysis Report (24 Sections)"
            )

        # Send Markdown file
        with open(md_file, "rb") as mf:
            await update.message.reply_document(
                document=mf,
                filename=f"CodeInsight_Report_{raw_scan['project_name']}.md",
                caption="📝 Raw Markdown Report"
            )

    except Exception as exc:
        logger.exception("Error processing project upload")
        await status_msg.edit_text(f"⚠️ Analysis error occurred: {exc}")