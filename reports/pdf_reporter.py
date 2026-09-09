"""
reports/pdf_reporter.py

Converts CodeInsight AI Markdown reports into styled, publication-ready PDF documents using ReportLab.
"""

import logging
import re
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger(__name__)


class PDFReporter:
    """Renders Markdown report text into a PDF document."""

    def __init__(self, output_dir: str = "storage/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf(self, markdown_text: str, project_id: str) -> Path:
        """Parses Markdown text and compiles a PDF report."""
        pdf_path = self.output_dir / f"CodeInsight_Report_{project_id}.pdf"
        logger.info("Generating PDF report to %s", pdf_path)

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()

        # Custom Palette
        PRIMARY_COLOR = HexColor("#1E293B")    # Slate 800
        ACCENT_COLOR = HexColor("#2563EB")     # Blue 600
        BG_LIGHT = HexColor("#F8FAFC")         # Slate 50
        TEXT_COLOR = HexColor("#0F172A")       # Slate 900
        BORDER_COLOR = HexColor("#E2E8F0")     # Slate 200

        # Custom Typography
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=ACCENT_COLOR,
            spaceAfter=12,
        )
        h2_style = ParagraphStyle(
            "SectionH2",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=PRIMARY_COLOR,
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True,
        )
        h3_style = ParagraphStyle(
            "SectionH3",
            parent=styles["Heading3"],
            fontSize=11,
            leading=14,
            textColor=ACCENT_COLOR,
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True,
        )
        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=13.5,
            textColor=TEXT_COLOR,
            spaceAfter=5,
        )
        bullet_style = ParagraphStyle(
            "BulletCustom",
            parent=body_style,
            leftIndent=12,
            spaceAfter=3,
        )
        code_style = ParagraphStyle(
            "CodeBlock",
            parent=styles["Code"],
            fontSize=8,
            leading=10,
            textColor=HexColor("#0F172A"),
            backColor=BG_LIGHT,
            borderColor=BORDER_COLOR,
            borderWidth=0.5,
            borderPadding=6,
            spaceAfter=8,
        )

        story = []

        # Cover Banner
        story.append(Paragraph("CodeInsight AI Technical Analysis", title_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_COLOR, spaceAfter=15))

        lines = markdown_text.splitlines()
        in_code_block = False
        code_buffer = []

        for line in lines:
            line_str = line.strip()

            # Code Blocks
            if line_str.startswith("```"):
                if in_code_block:
                    in_code_block = False
                    story.append(Preformatted("\n".join(code_buffer), code_style))
                    code_buffer = []
                else:
                    in_code_block = True
                    code_buffer = []
                continue

            if in_code_block:
                code_buffer.append(line)
                continue

            if not line_str:
                story.append(Spacer(1, 4))
                continue

            # Headings
            if line_str.startswith("# "):
                continue  # Skip main title since we drew cover
            elif line_str.startswith("## "):
                text = line_str[3:].strip()
                story.append(Spacer(1, 8))
                story.append(Paragraph(text, h2_style))
                story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=6))
            elif line_str.startswith("### "):
                text = line_str[4:].strip()
                story.append(Paragraph(text, h3_style))
            elif line_str.startswith("* ") or line_str.startswith("- "):
                formatted_line = self._format_inline_markdown(line_str[2:].strip())
                story.append(Paragraph(f"• {formatted_line}", bullet_style))
            elif line_str.startswith("---"):
                story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=6, spaceAfter=6))
            else:
                formatted_line = self._format_inline_markdown(line_str)
                story.append(Paragraph(formatted_line, body_style))

        doc.build(story)
        return pdf_path

    @staticmethod
    def _format_inline_markdown(text: str) -> str:
        """Converts basic markdown bold/code tags into ReportLab HTML tags."""
        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"`(.*?)`", r"<font face='Courier' color='#2563EB'><b>\1</b></font>", text)
        return text
