"""
cli.py

Command-line interface for CodeInsight AI.
Allows running local project analysis on a ZIP archive or directory.

Usage:
    python cli.py analyze path/to/project.zip
    python cli.py analyze path/to/project_dir
"""

import sys
import uuid
import logging
from pathlib import Path

# Force UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from core.extractor import ZipExtractor
from core.scanner import CodeScanner
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.ai_analyzer import AIAnalyzer
from reports.markdown_reporter import MarkdownReporter
from reports.pdf_reporter import PDFReporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("cli")


def analyze_project(target_path_str: str) -> None:
    target_path = Path(target_path_str).resolve()
    if not target_path.exists():
        print(f"Error: Path '{target_path_str}' does not exist.")
        sys.exit(1)

    project_id = uuid.uuid4().hex[:8]

    if target_path.is_file() and target_path.suffix.lower() == ".zip":
        print(f"[+] Extracting ZIP archive: {target_path.name}...")
        extractor = ZipExtractor(extract_base_dir="data/extracted")
        extracted_dir = extractor.extract_zip(str(target_path), project_id)
    elif target_path.is_dir():
        extracted_dir = target_path
    else:
        print(f"Error: Path '{target_path_str}' must be a .zip file or a directory.")
        sys.exit(1)

    print("[+] Scanning project files, AST patterns, dependencies, and secrets...")
    scanner = CodeScanner(extracted_dir)
    raw_scan = scanner.scan()

    print("[+] Aggregating static analysis metrics...")
    analysis_context = StaticAnalyzer.analyze(raw_scan)

    print("[+] Executing AI Deep Analysis (generating 24-section technical report)...")
    ai_analyzer = AIAnalyzer()
    markdown_report = ai_analyzer.generate_report(analysis_context)

    print("[+] Compiling Markdown and PDF report files...")
    md_reporter = MarkdownReporter(output_dir="data/reports")
    pdf_reporter = PDFReporter(output_dir="data/reports")

    md_file = md_reporter.save_report(markdown_report, project_id)
    pdf_file = pdf_reporter.generate_pdf(markdown_report, project_id)

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print(f"• Project Name:     {raw_scan['project_name']}")
    print(f"• Primary Language: {raw_scan['primary_language']}")
    print(f"• Files Scanned:    {raw_scan['total_files']}")
    print(f"• Lines of Code:    ~{raw_scan['total_lines']}")
    print("-" * 60)
    print(f"Markdown Report: {md_file.resolve()}")
    print(f"PDF Report:      {pdf_file.resolve()}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "analyze":
        print("Usage: python cli.py analyze <path_to_zip_or_directory>")
        sys.exit(1)

    analyze_project(sys.argv[2])
