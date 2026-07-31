"""File management operations"""
import os
import shutil
import zipfile
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

class FileManager:
    @staticmethod
    def create_file(path: str, content: str = "") -> str:
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return f"File created: {path}"
        except Exception as e:
            return f"Error creating file: {e}"

    @staticmethod
    def read_file(path: str) -> str:
        try:
            return Path(path).read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file: {e}"

    @staticmethod
    def delete_file(path: str) -> str:
        try:
            p = Path(path)
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            return f"Deleted: {path}"
        except Exception as e:
            return f"Error deleting: {e}"

    @staticmethod
    def copy_file(src: str, dst: str) -> str:
        try:
            shutil.copy2(src, dst)
            return f"Copied to: {dst}"
        except Exception as e:
            return f"Error copying: {e}"

    @staticmethod
    def move_file(src: str, dst: str) -> str:
        try:
            shutil.move(src, dst)
            return f"Moved to: {dst}"
        except Exception as e:
            return f"Error moving: {e}"

    @staticmethod
    def search_files(query: str, directory: str = None) -> List[str]:
        if not directory:
            directory = str(Path.home())
        results = []
        try:
            for root, _, files in os.walk(directory):
                for f in files:
                    if query.lower() in f.lower():
                        results.append(os.path.join(root, f))
                if len(results) >= 20:
                    break
        except Exception as e:
            logger.error(f"Search error: {e}")
        return results

    @staticmethod
    def compress_zip(files: List[str], output: str) -> str:
        try:
            with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
                for f in files:
                    zf.write(f, arcname=Path(f).name)
            return f"ZIP created: {output}"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def extract_zip(zip_path: str, output_dir: str) -> str:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(output_dir)
            return f"Extracted to: {output_dir}"
        except Exception as e:
            return f"Error: {e}"
