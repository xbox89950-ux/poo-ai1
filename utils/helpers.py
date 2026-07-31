"""Utility helpers"""
import re
from pathlib import Path

def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\|?*]', '_', name)

def get_desktop_path() -> Path:
    return Path.home() / "Desktop"

def truncate_text(text: str, max_len: int = 500) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."
