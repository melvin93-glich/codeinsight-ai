"""
analyzers/static_analyzer.py

Transforms raw scanner results into structured section data
adhering strictly to the 24-section requirement.
"""

from typing import Any, Dict, List


class StaticAnalyzer:
    """Pre-processes scanned project metrics into report section building blocks."""

    @staticmethod
    def analyze(scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts raw scan data into 24-section structured context."""

        # 1. Executive Summary
        exec_summary = {
            "project_name": scan_data.get("project_name", "Unknown"),
            "purpose": StaticAnalyzer._infer_purpose(scan_data),
            "description": f"Analyzed project containing {scan_data.get('total_files', 0)} files and ~{scan_data.get('total_lines', 0)} lines of code.",
            "project_type": StaticAnalyzer._infer_project_type(scan_data),
            "primary_language": scan_data.get("primary_language", "Unknown"),
            "complexity": StaticAnalyzer._estimate_complexity(scan_data),
            "architecture_style": StaticAnalyzer._infer_architecture(scan_data),
        }

        # 2. Tech Stack
        tech_stack = {
            "languages": [scan_data.get("primary_language")],
            "frameworks": list(scan_data.get("frameworks_found", {}).keys()) or ["Not detected"],
            "ai_frameworks": list(scan_data.get("ai_frameworks_found", {}).keys()) or ["Not detected"],
            "databases": list(scan_data.get("dbs_found", {}).keys()) or ["Not detected"],
            "vector_databases": list(scan_data.get("vector_dbs_found", {}).keys()) or ["Not detected"],
            "auth": list(scan_data.get("auth_found", {}).keys()) or ["Not detected"],
            "deployment": list(scan_data.get("deployment_found", {}).keys()) or ["Not detected"],
            "external_services": list(scan_data.get("external_services", {}).keys()) or ["Not detected"],
        }

        # 3. AI & LLM Analysis
        ai_models = scan_data.get("ai_models_found", [])

        # 4. AI Frameworks
        ai_frameworks = scan_data.get("ai_frameworks_found", {})

        # 5. RAG Detection
        rag_detected = len(scan_data.get("vector_dbs_found", {})) > 0 or "LangChain" in ai_frameworks or "LlamaIndex" in ai_frameworks

        # 6. Embedding Models
        embedding_models = [m for m in ai_models if "embedding" in m.get("model_name", "").lower() or "minilm" in m.get("model_name", "").lower()]

        # 7. Vector Database
        vector_dbs = scan_data.get("vector_dbs_found", {})

        # 8. Database Analysis
        databases = scan_data.get("dbs_found", {})

        # 9. API Analysis
        apis = scan_data.get("frameworks_found", {})

        # 10. Secrets
        secrets = scan_data.get("secrets_found", [])

        # 11. Auth
        auth = scan_data.get("auth_found", {})

        # 12 & 13. Folders & Files
        folder_tree = scan_data.get("folder_tree", "")
        file_list = scan_data.get("file_list", [])

        # 14. Dependencies
        manifests = scan_data.get("manifests", {})

        # 16. Security Audit
        security = scan_data.get("security_findings", [])

        # 17. Code Quality Scores
        quality_scores = StaticAnalyzer._calculate_quality_scores(scan_data)

        # 18. Design Patterns
        patterns = scan_data.get("design_patterns", {})

        # 20. Deployment
        deployment = scan_data.get("deployment_found", {})

        return {
            "exec_summary": exec_summary,
            "tech_stack": tech_stack,
            "ai_models": ai_models,
            "ai_frameworks": ai_frameworks,
            "rag_detected": rag_detected,
            "embedding_models": embedding_models,
            "vector_dbs": vector_dbs,
            "databases": databases,
            "apis": apis,
            "secrets": secrets,
            "auth": auth,
            "folder_tree": folder_tree,
            "file_list": file_list,
            "manifests": manifests,
            "security": security,
            "quality_scores": quality_scores,
            "patterns": patterns,
            "deployment": deployment,
            "raw_scan": scan_data,
        }

    @staticmethod
    def _infer_purpose(scan_data: Dict[str, Any]) -> str:
        readme = scan_data.get("manifests", {}).get("README.md", "")
        if readme:
            lines = [line.strip() for line in readme.splitlines() if line.strip() and not line.startswith("#")]
            if lines:
                return lines[0][:200]
        if scan_data.get("ai_frameworks_found"):
            return "AI-assisted application / LLM workflow project."
        if "FastAPI" in scan_data.get("frameworks_found", {}) or "Express" in scan_data.get("frameworks_found", {}):
            return "Web API service application."
        return "Software application project."

    @staticmethod
    def _infer_project_type(scan_data: Dict[str, Any]) -> str:
        fw = scan_data.get("frameworks_found", {})
        if "Next.js" in fw or "React" in fw or "Vue" in fw:
            return "Full-Stack Web Application"
        if "FastAPI" in fw or "Express" in fw or "Flask" in fw or "Django" in fw:
            return "Backend Web API / Microservice"
        return "Command Line / Standalone Module"

    @staticmethod
    def _estimate_complexity(scan_data: Dict[str, Any]) -> str:
        files = scan_data.get("total_files", 0)
        lines = scan_data.get("total_lines", 0)
        if files > 50 or lines > 5000:
            return "High"
        if files > 15 or lines > 1500:
            return "Medium"
        return "Low"

    @staticmethod
    def _infer_architecture(scan_data: Dict[str, Any]) -> str:
        fw = scan_data.get("frameworks_found", {})
        patterns = scan_data.get("design_patterns", {})
        if "MVC" in patterns:
            return "Model-View-Controller (MVC)"
        if "FastAPI" in fw or "Express" in fw:
            return "Modular REST API / Client-Server"
        return "Monolithic / Script-Based"

    @staticmethod
    def _calculate_quality_scores(scan_data: Dict[str, Any]) -> Dict[str, int]:
        total_files = scan_data.get("total_files", 1)
        security_issues = len(scan_data.get("security_findings", []))
        has_readme = "README.md" in scan_data.get("manifests", {})
        has_docker = "Docker" in scan_data.get("deployment_found", {})

        org_score = 8 if total_files > 3 else 6
        naming_score = 8
        docs_score = 9 if has_readme else 5
        sec_score = max(3, 10 - (security_issues * 2))
        handling_score = 7

        return {
            "Folder Organization": org_score,
            "Naming Conventions": naming_score,
            "Comments & Documentation": docs_score,
            "Scalability": 7 if has_docker else 6,
            "Maintainability": 7,
            "Reusability": 7,
            "Error Handling": handling_score,
            "Logging & Observability": 6,
            "Security Posture": sec_score,
        }
