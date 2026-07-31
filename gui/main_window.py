"""Main GUI window with glassmorphism design"""
import sys
import asyncio
import logging
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, Signal, QObject, QThread
from PySide6.QtGui import QFont

from config.settings import SETTINGS
from core.voice_engine import VoiceEngine
from core.ai_brain import AIBrain
from core.command_parser import CommandParser
from gui.animations import AIOrb, VoiceWave, TypingIndicator
from modules.web_search import WebSearch
from modules.code_generator import CodeGenerator
from modules.weather import Weather
from modules.news import News
from modules.system_info import SystemInfo
from modules.display_control import DisplayControl
from modules.music_player import music
from modules.calculator import Calculator
from modules.translator import Translator
from modules.pdf_reader import PDFReader
from modules.doc_reader import DocReader
from modules.clipboard import clipboard
from modules.network_control import NetworkControl
from modules.voice_recorder import VoiceRecorder
from modules.jokes import Jokes
from modules.datetime_util import DateTimeUtil
from modules.code_executor import CodeExecutor
from modules.ocr import OCR
from modules.calendar_reminder import CalendarReminder
from modules.alarm_timer import alarm_timer

logger = logging.getLogger(__name__)

class WorkerSignals(QObject):
    response_ready = Signal(str)

class AIWorker(QThread):
    def __init__(self, brain: AIBrain, text: str):
        super().__init__()
        self.brain = brain
        self.text = text
        self.signals = WorkerSignals()

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.brain.think(self.text))
            self.signals.response_ready.emit(response)
        except Exception as e:
            logger.error(f"AI Worker error: {e}")
            self.signals.response_ready.emit("Error processing request")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{SETTINGS.APP_NAME} v{SETTINGS.VERSION}")
        self.setMinimumSize(1000, 800)
        self.voice = VoiceEngine()
        self.brain = AIBrain()
        self.parser = CommandParser()
        self._last_code = ""
        self._setup_ui()
        self._apply_glass_theme()
        self.voice.on_command = self.handle_text_input
        self.voice.on_wake = self.on_wake_word

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        header = QHBoxLayout()
        self.orb = AIOrb(size=100)
        header.addWidget(self.orb)
        header_right = QVBoxLayout()
        self.status_label = QLabel("● Ready")
        self.status_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header_right.addWidget(self.status_label)
        self.wave = VoiceWave()
        self.wave.set_active(False)
        header_right.addWidget(self.wave)
        header.addLayout(header_right)
        header.addStretch()
        layout.addLayout(header)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 11))
        self.chat_display.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(self.chat_display)

        self.typing = TypingIndicator()
        self.typing.hide()
        layout.addWidget(self.typing)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type command or speak (e.g., 'ক্রোম খোলো', 'Hey Poo')...")
        self.input_field.setFont(QFont("Segoe UI", 12))
        self.input_field.returnPressed.connect(self.on_send)
        self.input_field.setMinimumHeight(45)

        self.mic_btn = QPushButton("🎤")
        self.mic_btn.setFixedSize(50, 45)
        self.mic_btn.setToolTip("Hold to speak")
        self.mic_btn.pressed.connect(self.start_listening)
        self.mic_btn.released.connect(self.stop_listening)

        self.send_btn = QPushButton("➤")
        self.send_btn.setFixedSize(50, 45)
        self.send_btn.clicked.connect(self.on_send)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.mic_btn)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)

        quick = QHBoxLayout()
        quick_actions = [
            ("Chrome", "open chrome"), ("VS Code", "open vs code"),
            ("Screenshot", "take screenshot"), ("Weather", "weather Dhaka"),
            ("Time", "what time"), ("Joke", "tell me a joke"),
        ]
        for label, cmd in quick_actions:
            btn = QPushButton(label)
            btn.setFixedHeight(35)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            quick.addWidget(btn)
        layout.addLayout(quick)

    def _apply_glass_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0f23, stop:0.5 #1a1a2e, stop:1 #16213e);
            }
            QTextEdit {
                background-color: rgba(30, 30, 46, 180);
                color: #cdd6f4;
                border: 1px solid rgba(137, 180, 250, 60);
                border-radius: 12px;
                padding: 15px;
            }
            QLineEdit {
                background-color: rgba(30, 30, 46, 200);
                color: #cdd6f4;
                border: 1px solid rgba(137, 180, 250, 80);
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton {
                background-color: rgba(137, 180, 250, 200);
                color: #1e1e2e;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(180, 190, 254, 240);
            }
            QPushButton:pressed {
                background-color: rgba(137, 180, 250, 150);
            }
            QLabel {
                color: #a6e3a1;
            }
        """)

    def on_wake_word(self):
        self.status_label.setText("● Wake word detected!")
        self.orb.set_active(True)
        self.wave.set_active(True)

    def start_listening(self):
        self.status_label.setText("● Listening...")
        self.status_label.setStyleSheet("color: #f9e2af;")
        self.orb.set_active(True)
        self.wave.set_active(True)
        text = self.voice.listen_once(timeout=5)
        if text:
            self.input_field.setText(text)
            self.handle_text_input(text)
        self.stop_listening()

    def stop_listening(self):
        self.status_label.setText("● Ready")
        self.status_label.setStyleSheet("color: #a6e3a1;")
        self.orb.set_active(False)
        self.wave.set_active(False)

    def on_send(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self.input_field.clear()
        self.handle_text_input(text)

    def quick_command(self, cmd: str):
        self.input_field.setText(cmd)
        self.on_send()

    def handle_text_input(self, text: str):
        self.chat_display.append(f"<b style='color:#89b4fa'>You:</b> {text}")
        action_type, action, target = self.parser.parse(text)

        response = ""

        if action_type == "automation":
            if action == "system_action":
                response = self.parser.execute_automation(action, target)
            else:
                response = self.parser.execute_automation(action, target)

        elif action_type == "system":
            if "CONFIRM_REQUIRED" in str(target):
                action_name = str(target).split(":")[1]
                reply = QMessageBox.question(self, "Confirm Action",
                    f"Are you sure you want to {action_name}?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    response = self.parser.execute_automation("system_action", action_name)
                else:
                    response = "Action cancelled"
            else:
                response = "System action handled."

        elif action_type == "web":
            if action == "search_google":
                response = WebSearch.search_google(target)
            elif action == "search_youtube":
                response = WebSearch.search_youtube(target)
            elif action == "open_website":
                response = WebSearch.open_website(target)

        elif action_type == "code":
            if action == "generate":
                self._ask_ai(text, is_code=True)
                return
            elif action == "run":
                if self._last_code:
                    response = CodeExecutor.run_python(self._last_code)
                else:
                    response = "No code to run. Generate code first."

        elif action_type == "info":
            if action == "weather":
                response = Weather.get_weather(target or "Dhaka")
            elif action == "news":
                response = News.get_headlines()
            elif action == "system_info":
                response = SystemInfo.get_all()
            elif action == "time":
                response = DateTimeUtil.get_time()
            elif action == "date":
                response = DateTimeUtil.get_date()

        elif action_type == "control":
            if action == "brightness":
                response = DisplayControl.set_brightness(int(target or 50))
            elif action == "wallpaper":
                response = DisplayControl.set_wallpaper(target)

        elif action_type == "media":
            if action == "play_music":
                if target and Path(target).exists():
                    response = music.play_file(target)
                else:
                    response = music.play_folder(str(Path.home() / "Music"))
            elif action == "stop_music":
                response = music.stop()

        elif action_type == "math":
            if action == "calculate":
                response = Calculator.evaluate(target)
            elif action == "currency":
                parts = target.split(":")
                if len(parts) == 3:
                    response = Calculator.convert_currency(float(parts[0]), parts[1], parts[2])
                else:
                    response = "Use: convert 100 USD to BDT"

        elif action_type == "text":
            if action == "translate":
                parts = target.split(":")
                if len(parts) == 2:
                    response = Translator.translate(parts[0], parts[1])
                else:
                    response = "Use: translate hello to bn"

        elif action_type == "fun":
            if action == "joke":
                lang = self.voice.detect_language(text)
                response = Jokes.get_joke(lang)
            elif action == "fact":
                response = Jokes.get_fact()
            elif action == "coin":
                response = Jokes.flip_coin()
            elif action == "dice":
                response = Jokes.roll_dice()

        elif action_type == "tool":
            if action == "clipboard":
                response = clipboard.get_history()
            elif action == "timer":
                response = alarm_timer.set_timer(int(target), "Timer finished!")
            elif action == "reminder":
                parts = target.split(":")
                if len(parts) == 2:
                    response = CalendarReminder.add_reminder(parts[0], parts[1])
                else:
                    response = "Use: remind me to call mom at 2026-08-01 14:30"
            elif action == "ocr":
                response = OCR.extract_from_screenshot()
            elif action == "record":
                response = VoiceRecorder.record(5)

        elif action_type == "network":
            if action == "wifi":
                if target == "on":
                    response = NetworkControl.wifi_on()
                elif target == "off":
                    response = NetworkControl.wifi_off()
                else:
                    response = NetworkControl.wifi_status()
            elif action == "bluetooth":
                if target == "on":
                    response = NetworkControl.bluetooth_on()
                else:
                    response = NetworkControl.bluetooth_off()

        elif action_type == "doc":
            if action == "read_pdf":
                response = PDFReader.read_pdf(target)

        elif action_type == "ai_chat":
            self._ask_ai(text)
            return

        if response:
            self.display_response(response)
            asyncio.create_task(self.voice.speak(response))

    def _ask_ai(self, text: str, is_code: bool = False):
        self.status_label.setText("● Thinking...")
        self.status_label.setStyleSheet("color: #f9e2af;")
        self.typing.show()
        self.orb.set_active(True)
        self.worker = AIWorker(self.brain, text)
        self.worker.signals.response_ready.connect(
            lambda r: self.on_ai_response(r, is_code)
        )
        self.worker.start()

    def on_ai_response(self, response: str, is_code: bool = False):
        self.display_response(response)
        self.status_label.setText("● Ready")
        self.status_label.setStyleSheet("color: #a6e3a1;")
        self.typing.hide()
        self.orb.set_active(False)

        if is_code:
            # Extract and save code
            blocks = CodeGenerator.extract_code_blocks(response)
            if blocks:
                code_text = "\n\n".join([b[1] for b in blocks])
                self._last_code = code_text
                result = CodeGenerator.create_project("generated_project", response)
                self.display_response(result)

        asyncio.create_task(self.voice.speak(response))

    def display_response(self, text: str):
        self.chat_display.append(f"<b style='color:#a6e3a1'>Poo:</b> {text}")
        self.chat_display.append("")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
