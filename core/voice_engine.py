"""Voice engine: Speech Recognition + TTS + Wake Word"""
import asyncio
import logging
import tempfile
import os
from typing import Callable, Optional
import speech_recognition as sr
import edge_tts
import pyttsx3
from config.settings import SETTINGS

logger = logging.getLogger(__name__)

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.wake_word_detected = False
        self.on_command: Optional[Callable[[str], None]] = None
        self.on_wake: Optional[Callable[[], None]] = None

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.dynamic_energy_threshold = True

        self._offline_tts = pyttsx3.init()
        self._offline_tts.setProperty('rate', 175)
        voices = self._offline_tts.getProperty('voices')
        for v in voices:
            if 'female' in v.name.lower() or 'zira' in v.name.lower():
                self._offline_tts.setProperty('voice', v.id)
                break

    def detect_language(self, text: str) -> str:
        bengali_range = range(0x0980, 0x09FF)
        if any(ord(c) in bengali_range for c in text):
            return "bn"
        banglish = ['kholo', 'cholo', 'koro', 'dao', 'amar', 'ki', 'keno', 'khao', 'jao']
        if any(p in text.lower() for p in banglish):
            return "bn"
        return "en"

    async def speak(self, text: str, lang: Optional[str] = None):
        if not lang:
            lang = self.detect_language(text)
        voice = SETTINGS.TTS_VOICE_BN if lang == "bn" else SETTINGS.TTS_VOICE_EN
        try:
            communicate = edge_tts.Communicate(text, voice)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp_path = tmp.name
            await communicate.save(tmp_path)
            os.system(f'start /min "" "{tmp_path}"')
            await asyncio.sleep(len(text) * 0.08 + 1)
            try:
                os.remove(tmp_path)
            except:
                pass
        except Exception as e:
            logger.warning(f"Edge-TTS failed: {e}, falling back to offline TTS")
            self._offline_tts.say(text)
            self._offline_tts.runAndWait()

    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            try:
                text = self.recognizer.recognize_google(audio, language="bn-BD,en-US")
                logger.info(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                logger.error(f"Google SR error: {e}")
                return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return None

    def check_wake_word(self, text: str) -> bool:
        text_lower = text.lower().strip()
        return any(wake in text_lower for wake in SETTINGS.WAKE_WORDS)

    async def listen_loop(self):
        self.is_listening = True
        logger.info("Voice loop started")
        while self.is_listening:
            text = self.listen_once(timeout=3, phrase_time_limit=5)
            if text and self.check_wake_word(text):
                if self.on_wake:
                    self.on_wake()
                await self.speak("Yes boss?" if self.detect_language(text) == "en" else "হ্যাঁ বলুন")
                command = self.listen_once(timeout=5, phrase_time_limit=10)
                if command and self.on_command:
                    self.on_command(command)
            await asyncio.sleep(0.1)

    def stop(self):
        self.is_listening = False
