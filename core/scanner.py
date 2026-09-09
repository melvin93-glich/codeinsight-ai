"""
core/scanner.py

Performs deep deterministic static code analysis, AST parsing,
and regex pattern extraction across project files.
"""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

logger = logging.getLogger(__name__)

# --- Patterns for Detection ---

SECRET_KEY_PATTERNS = {
    "OPENAI_API_KEY": (r"OPENAI_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "OpenAI API Authentication"),
    "GEMINI_API_KEY": (r"GEMINI_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "Google Gemini API Authentication"),
    "GOOGLE_API_KEY": (r"GOOGLE_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "Google API Key"),
    "ANTHROPIC_API_KEY": (r"ANTHROPIC_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "Anthropic Claude API Key"),
    "CLAUDE_API_KEY": (r"CLAUDE_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "Anthropic Claude API Key"),
    "GROQ_API_KEY": (r"GROQ_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "Groq AI Inference API Key"),
    "DEEPSEEK_API_KEY": (r"DEEPSEEK_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "DeepSeek AI API Key"),
    "HF_TOKEN": (r"(?:HF_TOKEN|HUGGINGFACE_HUB_TOKEN)\s*[:=]\s*['\"]?([^\s'\"#]+)", "Hugging Face Token"),
    "SERP_API_KEY": (r"SERP_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "SerpAPI Search Key"),
    "LANGCHAIN_API_KEY": (r"LANGCHAIN_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "LangChain API Key"),
    "LANGSMITH_API_KEY": (r"LANGSMITH_API_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "LangSmith Tracing Key"),
    "SUPABASE_KEY": (r"SUPABASE_(?:KEY|ANON_KEY|SERVICE_ROLE_KEY)\s*[:=]\s*['\"]?([^\s'\"#]+)", "Supabase Client/Admin Key"),
    "SUPABASE_URL": (r"SUPABASE_URL\s*[:=]\s*['\"]?([^\s'\"#]+)", "Supabase Project URL"),
    "MONGODB_URI": (r"(?:MONGODB_URI|MONGO_URI)\s*[:=]\s*['\"]?([^\s'\"#]+)", "MongoDB Connection String"),
    "DATABASE_URL": (r"DATABASE_URL\s*[:=]\s*['\"]?([^\s'\"#]+)", "Database Connection URI"),
    "FIREBASE_CONFIG": (r"FIREBASE_(?:CONFIG|API_KEY)\s*[:=]\s*['\"]?([^\s'\"#]+)", "Firebase App Credentials"),
    "AWS_SECRET_ACCESS_KEY": (r"AWS_SECRET_ACCESS_KEY\s*[:=]\s*['\"]?([^\s'\"#]+)", "AWS IAM Secret Key"),
    "AZURE_OPENAI_KEY": (r"AZURE_OPENAI_(?:KEY|API_KEY)\s*[:=]\s*['\"]?([^\s'\"#]+)", "Azure OpenAI Credentials"),
    "TELEGRAM_BOT_TOKEN": (r"TELEGRAM_BOT_TOKEN\s*[:=]\s*['\"]?([^\s'\"#]+)", "Telegram Bot API Token"),
    "JWT_SECRET": (r"(?:JWT_SECRET|SECRET_KEY)\s*[:=]\s*['\"]?([^\s'\"#]+)", "JWT Signing Secret"),
}

AI_MODELS = [
    ("gpt-4.1-mini", "OpenAI"),
    ("gpt-4o", "OpenAI"),
    ("gpt-4o-mini", "OpenAI"),
    ("gpt-4", "OpenAI"),
    ("gpt-3.5-turbo", "OpenAI"),
    ("text-embedding-3-small", "OpenAI"),
    ("text-embedding-3-large", "OpenAI"),
    ("gemini-1.5-pro", "Google"),
    ("gemini-1.5-flash", "Google"),
    ("gemini-2.0", "Google"),
    ("claude-3-5-sonnet", "Anthropic"),
    ("claude-3-opus", "Anthropic"),
    ("claude-3-haiku", "Anthropic"),
    ("mixtral-8x7b", "Mistral"),
    ("llama-3", "Meta / Ollama"),
    ("llama-3.1", "Meta / Ollama"),
    ("deepseek-r1", "DeepSeek"),
    ("deepseek-coder", "DeepSeek"),
    ("all-MiniLM", "Hugging Face"),
    ("bge-small", "BAAI / Hugging Face"),
    ("e5-base", "Hugging Face"),
]

AI_FRAMEWORKS = [
    ("LangChain", [r"import\s+langchain", r"from\s+langchain", r"require\(['\"]langchain['\"]\)", r"\"langchain\""]),
    ("LangGraph", [r"import\s+langgraph", r"from\s+langgraph", r"\"langgraph\""]),
    ("LlamaIndex", [r"import\s+llama_index", r"from\s+llama_index", r"\"llama-index\""]),
    ("CrewAI", [r"import\s+crewai", r"from\s+crewai", r"\"crewai\""]),
    ("AutoGen", [r"import\s+autogen", r"from\s+autogen", r"\"pyautogen\""]),
    ("Haystack", [r"import\s+haystack", r"from\s+haystack", r"\"farm-haystack\""]),
    ("DSPy", [r"import\s+dspy", r"from\s+dspy", r"\"dspy-ai\""]),
    ("Semantic Kernel", [r"semantic_kernel", r"Microsoft\.SemanticKernel"]),
    ("Transformers", [r"import\s+transformers", r"from\s+transformers", r"\"transformers\""]),
    ("Sentence Transformers", [r"sentence_transformers", r"\"sentence-transformers\""]),
    ("Instructor", [r"import\s+instructor", r"from\s+instructor", r"\"instructor\""]),
    ("Ollama SDK", [r"import\s+ollama", r"from\s+ollama", r"\"ollama\""]),
    ("LiteLLM", [r"import\s+litellm", r"from\s+litellm", r"\"litellm\""]),
    ("OpenAI SDK", [r"import\s+openai", r"from\s+openai", r"require\(['\"]openai['\"]\)", r"\"openai\""]),
    ("Google Generative AI", [r"google\.generativeai", r"@google/generative-ai", r"google-generativeai"]),
    ("Anthropic SDK", [r"import\s+anthropic", r"from\s+anthropic", r"@anthropic-ai/sdk"]),
]

VECTOR_DATABASES = [
    ("FAISS", [r"import\s+faiss", r"faiss\.Index", r"\"faiss-cpu\"", r"\"faiss-gpu\""]),
    ("Chroma", [r"import\s+chromadb", r"chromadb\.Client", r"\"chromadb\""]),
    ("Pinecone", [r"import\s+pinecone", r"Pinecone\(", r"\"@pinecone-database/pinecone\"", r"\"pinecone-client\""]),
    ("Qdrant", [r"import\s+qdrant_client", r"QdrantClient", r"\"@qdrant/js-client-rest\""]),
    ("Milvus", [r"pymilvus", r"MilvusClient", r"\"@zilliz/milvus2-sdk-node\""]),
    ("Weaviate", [r"import\s+weaviate", r"weaviate\.Client", r"\"weaviate-ts-client\""]),
    ("Redis Vector", [r"redis\.commands\.search", r"VectorField"]),
    ("ElasticSearch", [r"elasticsearch", r"ElasticsearchStore"]),
    ("OpenSearch", [r"opensearchpy", r"OpenSearchVectorSearch"]),
]

DATABASES = [
    ("MongoDB", [r"pymongo", r"mongoose", r"mongodb\+srv:", r"\"mongodb\""]),
    ("PostgreSQL", [r"psycopg2", r"asyncpg", r"pg", r"postgres://", r"postgresql://"]),
    ("MySQL", [r"mysqlconnector", r"pymysql", r"mysql2", r"mysql://"]),
    ("SQLite", [r"sqlite3", r"sqlite:", r"better-sqlite3"]),
    ("Firebase", [r"firebase_admin", r"firebase/app", r"firestore"]),
    ("Supabase", [r"supabase", r"@supabase/supabase-js"]),
    ("Redis", [r"import\s+redis", r"ioredis", r"redis://"]),
]

FRAMEWORKS_APIS = [
    ("FastAPI", [r"from\s+fastapi", r"import\s+FastAPI", r"\"fastapi\""]),
    ("Express", [r"require\(['\"]express['\"]\)", r"import\s+express", r"\"express\""]),
    ("Flask", [r"from\s+flask", r"import\s+Flask", r"\"flask\""]),
    ("Django", [r"django\.core", r"import\s+django", r"\"django\""]),
    ("Spring Boot", [r"org\.springframework\.boot", r"@SpringBootApplication"]),
    ("NestJS", [r"@nestjs/core", r"@nestjs/common"]),
    ("Next.js", [r"next/router", r"next/navigation", r"\"next\""]),
    ("React", [r"import\s+React", r"\"react\""]),
    ("Vue", [r"import\s+\{.*\}\s+from\s+['\"]vue['\"]", r"\"vue\""]),
    ("Svelte", [r"\"svelte\""]),
]

AUTH_PATTERNS = [
    ("JWT", [r"jsonwebtoken", r"PyJWT", r"jwt\.sign", r"jwt\.decode", r"Bearer\s+"]),
    ("OAuth", [r"passport-google", r"oauth2", r"GoogleAuthConfig", r"authorize_redirect"]),
    ("Firebase Auth", [r"firebase/auth", r"getAuth\(", r"verifyIdToken"]),
    ("Supabase Auth", [r"supabase\.auth", r"auth\.signUp"]),
    ("Clerk", [r"@clerk/clerk-sdk-node", r"@clerk/nextjs"]),
    ("NextAuth", [r"next-auth", r"NextAuth\("]),
    ("Passport", [r"passport\.use", r"require\(['\"]passport['\"]\)"]),
    ("Sessions", [r"express-session", r"Flask-Session", r"session\["]),
]


class CodeScanner:
    """Scans extracted project files and generates technical metadata."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def scan(self) -> Dict[str, Any]:
        """Executes full scan and returns structured metrics."""
        from core.extractor import ZipExtractor

        files = ZipExtractor.get_project_files(self.project_dir)
        folder_tree = ZipExtractor.build_folder_tree(self.project_dir)

        total_files = len(files)
        total_lines = 0
        file_list: List[str] = []
        file_contents: Dict[str, str] = {}
        file_extensions: Dict[str, int] = {}

        # Package manifests content
        manifests: Dict[str, str] = {}

        for f in files:
            rel_path = str(f.relative_to(self.project_dir)).replace("\\", "/")
            file_list.append(rel_path)
            ext = f.suffix.lower() or f.name
            file_extensions[ext] = file_extensions.get(ext, 0) + 1

            content = ZipExtractor.read_file_content(f)
            file_contents[rel_path] = content
            total_lines += len(content.splitlines())

            if f.name in {"package.json", "requirements.txt", "pyproject.toml", "Cargo.toml", "go.mod", "docker-compose.yml", "Dockerfile", "README.md"}:
                manifests[f.name] = content

        # Run scanners
        secrets_found = self._scan_secrets(file_contents)
        ai_models_found = self._scan_ai_models(file_contents)
        ai_frameworks_found = self._scan_patterns(file_contents, AI_FRAMEWORKS)
        vector_dbs_found = self._scan_patterns(file_contents, VECTOR_DATABASES)
        dbs_found = self._scan_patterns(file_contents, DATABASES)
        frameworks_found = self._scan_patterns(file_contents, FRAMEWORKS_APIS)
        auth_found = self._scan_patterns(file_contents, AUTH_PATTERNS)
        security_findings = self._scan_security(file_contents)
        design_patterns = self._scan_design_patterns(file_contents)
        external_services = self._scan_external_services(file_contents)
        deployment_found = self._scan_deployment(file_contents, file_list)

        # Detect Primary Language
        primary_lang = self._detect_primary_language(file_extensions)

        return {
            "project_name": self.project_dir.name,
            "total_files": total_files,
            "total_lines": total_lines,
            "file_list": file_list,
            "folder_tree": folder_tree,
            "file_extensions": file_extensions,
            "primary_language": primary_lang,
            "manifests": manifests,
            "secrets_found": secrets_found,
            "ai_models_found": ai_models_found,
            "ai_frameworks_found": ai_frameworks_found,
            "vector_dbs_found": vector_dbs_found,
            "dbs_found": dbs_found,
            "frameworks_found": frameworks_found,
            "auth_found": auth_found,
            "security_findings": security_findings,
            "design_patterns": design_patterns,
            "external_services": external_services,
            "deployment_found": deployment_found,
            "file_contents": file_contents,
        }

    def _detect_primary_language(self, extensions: Dict[str, int]) -> str:
        lang_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript (React)",
            ".jsx": "JavaScript (React)",
            ".java": "Java",
            ".go": "Go",
            ".rs": "Rust",
            ".cpp": "C++",
            ".c": "C",
            ".php": "PHP",
            ".cs": "C#",
            ".rb": "Ruby",
            ".html": "HTML/CSS",
        }
        counts: Dict[str, int] = {}
        for ext, count in extensions.items():
            lang = lang_map.get(ext)
            if lang:
                counts[lang] = counts.get(lang, 0) + count
        if not counts:
            return "Unknown / Mixed"
        return max(counts, key=counts.get)

    def _scan_secrets(self, file_contents: Dict[str, str]) -> List[Dict[str, str]]:
        found = []
        for file_path, content in file_contents.items():
            for key_name, (pattern, purpose) in SECRET_KEY_PATTERNS.items():
                if re.search(pattern, content, re.IGNORECASE) or key_name in content:
                    found.append({
                        "key_name": key_name,
                        "location": file_path,
                        "purpose": purpose,
                        "status": "✓ Key Reference Found"
                    })
        return found

    def _scan_ai_models(self, file_contents: Dict[str, str]) -> List[Dict[str, str]]:
        results = []
        seen = set()
        for file_path, content in file_contents.items():
            for model_name, provider in AI_MODELS:
                if model_name.lower() in content.lower():
                    key = (model_name, file_path)
                    if key not in seen:
                        seen.add(key)
                        # Extract containing function/class context roughly
                        func_match = re.search(r"(?:def|function|class)\s+([a-zA-Z0-9_]+)", content)
                        func_name = func_match.group(1) if func_match else "Global/Script"
                        results.append({
                            "model_name": model_name,
                            "provider": provider,
                            "file": file_path,
                            "function": func_name,
                            "purpose": f"Inference / AI processing with {model_name}"
                        })
        return results

    def _scan_patterns(self, file_contents: Dict[str, str], pattern_list: List[Tuple[str, List[str]]]) -> Dict[str, List[str]]:
        results: Dict[str, List[str]] = {}
        for name, regexes in pattern_list:
            matched_files = set()
            for file_path, content in file_contents.items():
                for reg in regexes:
                    if re.search(reg, content, re.IGNORECASE):
                        matched_files.add(file_path)
            if matched_files:
                results[name] = sorted(list(matched_files))
        return results

    def _scan_security(self, file_contents: Dict[str, str]) -> List[Dict[str, str]]:
        issues = []
        for file_path, content in file_contents.items():
            # Hardcoded API keys check (raw string like sk-...)
            if re.search(r"['\"]sk-[a-zA-Z0-9]{20,}['\"]", content):
                issues.append({"severity": "Critical", "issue": "Hardcoded OpenAI API Secret Key in source code", "location": file_path})
            # SQL Injection check
            if re.search(r"SELECT\s+.*\s+FROM\s+.*%s", content, re.IGNORECASE) or re.search(r"f['\"].*SELECT\s+.*\{.*\}", content, re.IGNORECASE):
                issues.append({"severity": "High", "issue": "Potential SQL Injection via unformatted string interpolation", "location": file_path})
            # Unsafe eval()
            if re.search(r"\beval\(", content):
                issues.append({"severity": "High", "issue": "Use of unsafe eval() execution", "location": file_path})
            # Debug mode enabled
            if re.search(r"DEBUG\s*=\s*True", content) or re.search(r"app\.run\(.*debug=True.*\)", content):
                issues.append({"severity": "Medium", "issue": "Debug mode enabled in code configuration", "location": file_path})
            # Open CORS
            if re.search(r"allow_origins=\['\*'\]", content) or re.search(r"cors\(\s*\{.*origin:\s*'\*'.*\}\)", content):
                issues.append({"severity": "Medium", "issue": "Open CORS policy (allows all origins '*')", "location": file_path})
        return issues

    def _scan_design_patterns(self, file_contents: Dict[str, str]) -> Dict[str, List[str]]:
        patterns = {
            "MVC": [r"controllers/", r"models/", r"views/"],
            "Repository": [r"Repository\b", r"repo/"],
            "Factory": [r"Factory\b", r"create_[a-z_]+"],
            "Singleton": [r"__instance", r"getInstance"],
            "Dependency Injection": [r"Depends\(", r"@Inject"],
            "Observer": [r"subscribe\(", r"EventEmitter"],
        }
        found: Dict[str, List[str]] = {}
        for pattern_name, regexes in patterns.items():
            files = set()
            for file_path, content in file_contents.items():
                for reg in regexes:
                    if re.search(reg, file_path, re.IGNORECASE) or re.search(reg, content):
                        files.add(file_path)
            if files:
                found[pattern_name] = sorted(list(files))
        return found

    def _scan_external_services(self, file_contents: Dict[str, str]) -> Dict[str, List[str]]:
        services = {
            "Stripe": [r"stripe"],
            "Razorpay": [r"razorpay"],
            "Twilio": [r"twilio"],
            "SendGrid": [r"sendgrid"],
            "Firebase": [r"firebase"],
            "AWS": [r"boto3", r"aws-sdk"],
            "Azure": [r"azure-storage", r"@azure/"],
            "Google Cloud": [r"google-cloud"],
            "Vercel": [r"vercel"],
            "Netlify": [r"netlify"],
            "Cloudinary": [r"cloudinary"],
            "GitHub": [r"github-api", r"octokit"],
        }
        found: Dict[str, List[str]] = {}
        for svc, regexes in services.items():
            files = set()
            for file_path, content in file_contents.items():
                for reg in regexes:
                    if re.search(reg, content, re.IGNORECASE):
                        files.add(file_path)
            if files:
                found[svc] = sorted(list(files))
        return found

    def _scan_deployment(self, file_contents: Dict[str, str], file_list: List[str]) -> Dict[str, List[str]]:
        deployments: Dict[str, List[str]] = {}
        if "Dockerfile" in file_list:
            deployments["Docker"] = ["Dockerfile"]
        if "docker-compose.yml" in file_list or "docker-compose.yaml" in file_list:
            deployments["Docker Compose"] = [f for f in file_list if "docker-compose" in f]
        
        for file_path in file_list:
            if ".github/workflows" in file_path:
                deployments.setdefault("GitHub Actions", []).append(file_path)
            if "nginx" in file_path.lower():
                deployments.setdefault("Nginx", []).append(file_path)
            if "render.yaml" in file_path:
                deployments.setdefault("Render", []).append(file_path)
            if "procfile" in file_path.lower():
                deployments.setdefault("Heroku / Procfile", []).append(file_path)
        return deployments
