"""Clipboard management with history"""
import pyperclip
import logging
from typing import List
from collections import deque

logger = logging.getLogger(__name__)

class ClipboardManager:
    def __init__(self, max_history: int = 20):
        self.history: deque = deque(maxlen=max_history)
        self._last = ""

    def copy(self, text: str) -> str:
        pyperclip.copy(text)
        self.history.append(text)
        return "Copied to clipboard"

    def paste(self) -> str:
        return pyperclip.paste()

    def get_history(self) -> str:
        if not self.history:
            return "Clipboard history is empty"
        lines = [f"{i+1}. {item[:50]}..." if len(item) > 50 else f"{i+1}. {item}" 
                 for i, item in enumerate(self.history)]
        return "Clipboard History:\n" + "\n".join(lines)

    def clear_history(self) -> str:
        self.history.clear()
        return "Clipboard history cleared"

clipboard = ClipboardManager()
