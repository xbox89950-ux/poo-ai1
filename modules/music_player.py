"""Local music player"""
import os
import logging
from pathlib import Path
from typing import List

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

logger = logging.getLogger(__name__)

class MusicPlayer:
    def __init__(self):
        self.playlist: List[str] = []
        self.current_index = 0
        if PYGAME_AVAILABLE:
            pygame.mixer.init()

    def play_file(self, path: str) -> str:
        if not PYGAME_AVAILABLE:
            return "pygame not installed. Run: pip install pygame"
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            return f"Playing: {Path(path).name}"
        except Exception as e:
            return f"Error: {e}"

    def pause(self) -> str:
        if PYGAME_AVAILABLE:
            pygame.mixer.music.pause()
        return "Paused"

    def resume(self) -> str:
        if PYGAME_AVAILABLE:
            pygame.mixer.music.unpause()
        return "Resumed"

    def stop(self) -> str:
        if PYGAME_AVAILABLE:
            pygame.mixer.music.stop()
        return "Stopped"

    def set_volume(self, level: float) -> str:
        if PYGAME_AVAILABLE:
            pygame.mixer.music.set_volume(max(0.0, min(1.0, level)))
        return f"Volume set to {int(level*100)}%"

    def play_folder(self, folder: str) -> str:
        path = Path(folder)
        if not path.exists():
            return "Folder not found"
        self.playlist = [str(f) for f in path.glob("*.mp3")] + [str(f) for f in path.glob("*.wav")]
        if not self.playlist:
            return "No music files found"
        self.current_index = 0
        return self.play_file(self.playlist[0])

music = MusicPlayer()
