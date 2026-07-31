"""Central configuration for Poo AI Assistant"""
import os
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass
class Config:
    APP_NAME: str = "Poo AI"
    VERSION: str = "2.0.0"
    DEBUG: bool = True

    BASE_DIR: Path = BASE_DIR
    LOG_DIR: Path = BASE_DIR / "logs"
    DB_PATH: Path = BASE_DIR / "database" / "poo.db"
    ASSETS_DIR: Path = BASE_DIR / "gui" / "assets"
    PLUGINS_DIR: Path = BASE_DIR / "plugins"

    OPENAI_API_KEY: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    OPENAI_MODEL: str = "gpt-4o-mini"
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    DEFAULT_AI_PROVIDER: str = "openai"

    WAKE_WORDS: List[str] = field(default_factory=lambda: [
        "hey poo", "poo", "hello poo", "hi poo",
        "হে পু", "পু", "হ্যালো পু", "হাই পু"
    ])
    TTS_VOICE_BN: str = "bn-BD-PradeepNeural"
    TTS_VOICE_EN: str = "en-US-GuyNeural"
    TTS_VOICE_EN_F: str = "en-US-JennyNeural"
    LISTEN_TIMEOUT: int = 5
    PHRASE_THRESHOLD: float = 0.5

    THEME: str = "dark"
    ENABLE_ANIMATIONS: bool = True
    WINDOW_OPACITY: float = 0.95

    CONFIRM_DESTRUCTIVE: bool = True
    ENCRYPT_DATA: bool = False

    AUTO_START: bool = False
    START_MINIMIZED: bool = False

    def __post_init__(self):
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(self.LOG_DIR / "poo.log", encoding="utf-8")
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))
        logging.getLogger().addHandler(fh)

SETTINGS = Config()
