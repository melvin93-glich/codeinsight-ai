"""
web/server.py

FastAPI server providing a Web Dashboard for live drag & drop ZIP analysis,
report visualizer, and document downloads.
"""

import os
import uuid
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from core.extractor import ZipExtractor
from core.scanner import CodeScanner
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.ai_analyzer import AIAnalyzer
from reports.markdown_reporter import MarkdownReporter
from reports.pdf_reporter import PDFReporter

app = FastAPI(title="CodeInsight AI - Web Dashboard")

UPLOAD_DIR = Path("data/uploads")
REPORT_DIR = Path("data/reports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = Path(__file__).parent / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>CodeInsight AI Web Server Running</h1>")


@app.post("/api/analyze")
async def analyze_upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are supported.")

    project_id = uuid.uuid4().hex[:8]
    zip_dest = UPLOAD_DIR / f"{project_id}_{file.filename}"

    with open(zip_dest, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        extractor = ZipExtractor(extract_base_dir="data/extracted")
        extracted_dir = extractor.extract_zip(str(zip_dest), project_id)

        scanner = CodeScanner(extracted_dir)
        raw_scan = scanner.scan()

        analysis_context = StaticAnalyzer.analyze(raw_scan)

        ai_analyzer = AIAnalyzer()
        markdown_report = ai_analyzer.generate_report(analysis_context)

        md_reporter = MarkdownReporter(output_dir=str(REPORT_DIR))
        pdf_reporter = PDFReporter(output_dir=str(REPORT_DIR))

        md_file = md_reporter.save_report(markdown_report, project_id)
        pdf_file = pdf_reporter.generate_pdf(markdown_report, project_id)

        return JSONResponse({
            "status": "success",
            "project_id": project_id,
            "project_name": raw_scan["project_name"],
            "primary_language": raw_scan["primary_language"],
            "total_files": raw_scan["total_files"],
            "total_lines": raw_scan["total_lines"],
            "markdown_report": markdown_report,
            "md_download_url": f"/api/download/{md_file.name}",
            "pdf_download_url": f"/api/download/{pdf_file.name}",
        })
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = REPORT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
