"""Code generation and project management"""
import os
import subprocess
import logging
import re
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class CodeGenerator:
    LANGUAGE_MAP = {
        "python": ".py", "html": ".html", "css": ".css", "javascript": ".js",
        "typescript": ".ts", "react": ".jsx", "next.js": ".tsx", "vue": ".vue",
        "angular": ".ts", "node.js": ".js", "php": ".php", "laravel": ".php",
        "c": ".c", "c++": ".cpp", "c#": ".cs", "java": ".java", "kotlin": ".kt",
        "swift": ".swift", "dart": ".dart", "flutter": ".dart", "sql": ".sql",
        "mongodb": ".js", "mysql": ".sql", "sqlite": ".sql", "markdown": ".md",
        "txt": ".txt", "json": ".json", "yaml": ".yml", "xml": ".xml"
    }

    @staticmethod
    def extract_code_blocks(text: str) -> list:
        pattern = r"```(\w+)?
(.*?)```"
        return re.findall(pattern, text, re.DOTALL)

    @staticmethod
    def create_project(description: str, ai_response: str, base_dir: Optional[str] = None) -> str:
        if not base_dir:
            base_dir = str(Path.home() / "Desktop" / "PooProjects")
        blocks = CodeGenerator.extract_code_blocks(ai_response)
        if not blocks:
            return "No code blocks found in response."
        project_path = Path(base_dir) / re.sub(r'[^\w]', '_', description[:30])
        project_path.mkdir(parents=True, exist_ok=True)
        created = []
        for lang, code in blocks:
            ext = CodeGenerator.LANGUAGE_MAP.get(lang.lower(), f".{lang}")
            filename = f"main{ext}" if len(blocks) == 1 else f"file_{len(created)}{ext}"
            file_path = project_path / filename
            file_path.write_text(code.strip(), encoding="utf-8")
            created.append(str(file_path))
        try:
            subprocess.Popen(f'code "{project_path}"', shell=True)
        except Exception:
            pass
        return f"Created project at {project_path} with {len(created)} files."

    @staticmethod
    def run_python(file_path: str) -> str:
        try:
            result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=30)
            return result.stdout or result.stderr
        except Exception as e:
            return f"Error running file: {e}"

    @staticmethod
    def open_vscode(path: str = "."):
        try:
            subprocess.Popen(f'code "{path}"', shell=True)
            return "Opened VS Code"
        except Exception as e:
            return f"Error: {e}"
