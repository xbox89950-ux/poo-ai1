"""Safe Python code execution"""
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class CodeExecutor:
    @staticmethod
    def run_python(code: str, timeout: int = 10) -> str:
        """Execute Python code safely in a subprocess"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code)
                tmp_path = f.name

            result = subprocess.run(
                ["python", tmp_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            Path(tmp_path).unlink(missing_ok=True)

            output = result.stdout
            error = result.stderr

            if error and not output:
                return f"Error:\n{error[:500]}"
            if error:
                return f"Output:\n{output[:500]}\n\nError:\n{error[:300]}"
            return f"Output:\n{output[:1000]}"
        except subprocess.TimeoutExpired:
            return "Code execution timed out (max 10 seconds)"
        except Exception as e:
            return f"Execution error: {e}"

    @staticmethod
    def run_javascript(code: str) -> str:
        try:
            result = subprocess.run(
                ["node", "-e", code],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout or result.stderr
        except FileNotFoundError:
            return "Node.js not found. Install Node.js to run JavaScript."
        except Exception as e:
            return f"JS error: {e}"
