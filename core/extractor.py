"""
core/extractor.py

Handles safe extraction of ZIP archives, file tree generation,
and safe content reading for CodeInsight AI analysis.
"""

import logging
import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Set, Tuple

logger = logging.getLogger(__name__)

# Standard directories and file patterns to ignore during analysis to keep context relevant
IGNORE_DIRS: Set[str] = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".next",
    ".nuxt",
    "dist",
    "build",
    "out",
    "target",
    ".idea",
    ".vscode",
    "coverage",
    ".DS_Store",
}

IGNORE_EXTENSIONS: Set[str] = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".so",
    ".dll",
    ".exe",
    ".bin",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".svg",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".mp3",
    ".mp4",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".pdf",
    ".db",
    ".sqlite3",
}

MAX_FILE_SIZE_BYTES = 500 * 1024  # 500 KB per file limit for text reading


class ZipExtractor:
    """Safely extracts ZIP files and inspects project structure."""

    def __init__(self, extract_base_dir: str = "data/extracted"):
        self.extract_base_dir = Path(extract_base_dir)
        self.extract_base_dir.mkdir(parents=True, exist_ok=True)

    def extract_zip(self, zip_path: str, project_id: str) -> Path:
        """
        Safely extracts a zip file into a dedicated project directory.
        Prevents ZipSlip vulnerabilities by checking canonical paths.
        """
        zip_path_obj = Path(zip_path)
        if not zip_path_obj.exists():
            raise FileNotFoundError(f"ZIP file not found at: {zip_path}")

        target_dir = self.extract_base_dir / project_id
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Extracting %s to %s", zip_path, target_dir)

        with zipfile.ZipFile(zip_path_obj, "r") as zip_ref:
            for member in zip_ref.infolist():
                # Prevent ZipSlip
                member_path = Path(member.filename)
                target_path = (target_dir / member_path).resolve()
                if not str(target_path).startswith(str(target_dir.resolve())):
                    raise ValueError(f"Security Alert: ZipSlip path traversal attempt detected in file {member.filename}")
                zip_ref.extract(member, target_dir)

        # Handle top-level single root folder wrapper if present
        children = [c for c in target_dir.iterdir() if c.is_dir() and c.name not in IGNORE_DIRS]
        files = [c for c in target_dir.iterdir() if c.is_file()]
        if len(children) == 1 and len(files) == 0:
            logger.info("Unwrapping single top-level folder: %s", children[0].name)
            target_dir = children[0]

        return target_dir

    @staticmethod
    def get_project_files(project_dir: Path) -> List[Path]:
        """Returns a list of all non-ignored relative file paths in the project."""
        project_files: List[Path] = []
        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file_name in files:
                ext = Path(file_name).suffix.lower()
                if ext in IGNORE_EXTENSIONS or (file_name.startswith(".") and file_name not in {".env", ".env.example", ".gitignore", ".dockerignore"}):
                    continue
                full_path = Path(root) / file_name
                project_files.append(full_path)
        return project_files

    @staticmethod
    def build_folder_tree(project_dir: Path, max_depth: int = 4) -> str:
        """Builds a readable ASCII folder tree for the project."""
        tree_lines: List[str] = [f"{project_dir.name}/"]

        def _add_dir(current_path: Path, prefix: str = "", depth: int = 1):
            if depth > max_depth:
                tree_lines.append(f"{prefix}└── ... (max depth reached)")
                return

            try:
                entries = sorted(list(current_path.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
            except PermissionError:
                return

            filtered_entries = [
                e for e in entries
                if e.name not in IGNORE_DIRS and e.suffix.lower() not in IGNORE_EXTENSIONS
            ]

            for idx, entry in enumerate(filtered_entries):
                is_last = (idx == len(filtered_entries) - 1)
                connector = "└── " if is_last else "├── "
                sub_prefix = "    " if is_last else "│   "

                if entry.is_dir():
                    tree_lines.append(f"{prefix}{connector}{entry.name}/")
                    _add_dir(entry, prefix + sub_prefix, depth + 1)
                else:
                    tree_lines.append(f"{prefix}{connector}{entry.name}")

        _add_dir(project_dir)
        return "\n".join(tree_lines[:150])

    @staticmethod
    def read_file_content(file_path: Path) -> str:
        """Safely reads text content of a file."""
        if not file_path.exists() or file_path.is_dir():
            return ""
        if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
            return f"[File content truncated because size > {MAX_FILE_SIZE_BYTES // 1024} KB]"

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as exc:
            logger.warning("Could not read file %s: %s", file_path, exc)
            return ""