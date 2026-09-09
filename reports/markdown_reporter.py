"""
reports/markdown_reporter.py

Saves and exports Markdown reports for CodeInsight AI.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MarkdownReporter:
    """Manages creation and saving of Markdown report files."""

    def __init__(self, output_dir: str = "storage/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_report(self, report_markdown: str, project_id: str) -> Path:
        """Saves the markdown report to a file and returns its path."""
        file_path = self.output_dir / f"CodeInsight_Report_{project_id}.md"
        logger.info("Saving Markdown report to %s", file_path)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_markdown)
        return file_path
