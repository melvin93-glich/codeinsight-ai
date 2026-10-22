# CodeInsight AI 🔍⚡

> **Automated AI Project Analyzer & 24-Section Technical Auditor**  
> Analyze full codebases (ZIP or folder) across tech stack, AI/LLM models, RAG pipelines, secrets, security vulnerabilities, and code quality. Exports publication-ready **Markdown** and **PDF** reports.

---

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot%20API-2CA5E0.svg?style=flat&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ✨ Features

- **24-Section Deep Audit**: Generates an exhaustive technical report covering architecture, dependencies, security, LLM usage, RAG components, and quality scores.
- **Multi-Channel Access**:
  - 🌐 **Modern Web UI**: Drag-and-drop dashboard with live progress and inline markdown viewer.
  - 🤖 **Telegram Bot**: Send any project `.zip` directly to your bot for instant reports on mobile or desktop.
  - 💻 **CLI Tool**: Instant terminal auditing for local developer workflows.
- **Dual Export Formats**: Automatically outputs clean **GitHub-Flavored Markdown (`.md`)** and styled **ReportLab PDF (`.pdf`)**.
- **Deterministic Static + AI Deep Engine**: Combines AST/regex scanning for zero hallucinations with LLM intelligence (OpenAI / fallback rule engine).
- **Security-First**: Detects secret keys without ever exposing sensitive values, and prevents path traversal (ZipSlip protection).

---

## 🏗️ Architecture

```
Project (.zip / directory)
       │
       ▼
 [ Safe Extractor ] ── (ZipSlip Prevention & Ignore Filter)
       │
       ▼
 [ Code Scanner ]   ── (AST / Pattern Detection / Secrets / Security)
       │
       ▼
 [ AI Analyzer ]    ── (24-Section Technical Synthesis)
       │
   ┌───┴───────────────┐
   ▼                   ▼
Markdown (.md)      PDF Report (.pdf)
```

---

## 🚀 Quickstart

### 1. Prerequisites & Installation

```bash
# Clone the repository
git clone https://github.com/your-username/codeinsight-ai.git
cd codeinsight-ai

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
MAX_UPLOAD_SIZE_MB=500
UPLOAD_DIR=data/uploads
```
*(Note: If `OPENAI_API_KEY` is omitted, CodeInsight AI automatically falls back to its deterministic rule engine).*

---

## 💻 Usage

### 🌐 Web Dashboard (Browser)
Run the web server:
```bash
python main.py web
```
Open **`http://127.0.0.1:8000`** in your browser. Drag and drop your project `.zip` to inspect and download reports.

### 🤖 Telegram Bot
Start polling:
```bash
python main.py
```
Open your bot in Telegram, type `/start`, and upload your `.zip` archive. The bot will deliver status messages along with your `.pdf` and `.md` reports.

### ⚡ CLI (Terminal)
Analyze any local ZIP or repository directory:
```bash
# Analyze a ZIP archive
python cli.py analyze path/to/project.zip

# Analyze a local folder
python cli.py analyze path/to/project_folder
```

---

## 📊 24-Section Report Breakdown

| # | Section | Focus |
|---|---|---|
| **1–2** | **Executive Summary & Tech Stack** | Core purpose, languages, frameworks, DBs, cloud, complexity |
| **3–7** | **AI, RAG & Vector Intelligence** | Detected LLMs (OpenAI, Claude, Gemini, etc.), frameworks, chunking, vector stores |
| **8–11** | **Backend, APIs & Auth** | Databases, REST/GraphQL endpoints, secret references (safe audit), auth schemes |
| **12–15** | **Structure, Files & Architecture** | ASCII directory tree, manifests, dependencies, data flow diagrams |
| **16–18** | **Security & Code Quality** | Vulnerability scan (SQLi, eval, CORS), 1–10 quality metrics, design patterns |
| **19–22** | **Ops & Performance** | External SaaS integrations, deployment configs, bottlenecks, missing features |
| **23–24** | **README & Final Summary** | Auto-generated professional README, score cards, and production readiness |

---

## 📁 Repository Structure

```
codeinsight-ai/
├── analyzers/         # Static heuristics & AI analysis engine
├── bot/               # Telegram bot handlers & upload workflows
├── core/              # ZipSlip extraction, AST & regex scanner
├── data/              # Temp uploads, extracted files, and reports
├── reports/           # Markdown and ReportLab PDF generators
├── web/               # FastAPI backend & HTML5 dashboard
├── cli.py             # Command-line interface entry point
├── main.py            # Primary runner (Bot & Web modes)
└── requirements.txt   # Project dependencies
```

---

## 🛡️ License

Distributed under the **MIT License**. See `LICENSE` for more information.
