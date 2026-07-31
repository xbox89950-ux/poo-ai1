"""Settings dialog"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QCheckBox, QPushButton, QTabWidget, QWidget
)
from config.settings import SETTINGS
from database.db_manager import db

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Poo Settings")
        self.setMinimumSize(500, 400)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        ai_layout.addWidget(QLabel("AI Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["openai", "ollama"])
        self.provider_combo.setCurrentText(SETTINGS.DEFAULT_AI_PROVIDER)
        ai_layout.addWidget(self.provider_combo)
        ai_layout.addWidget(QLabel("OpenAI API Key:"))
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.setText(SETTINGS.OPENAI_API_KEY)
        ai_layout.addWidget(self.api_key)
        ai_layout.addStretch()
        tabs.addTab(ai_tab, "AI")
        voice_tab = QWidget()
        v_layout = QVBoxLayout(voice_tab)
        self.wake_check = QCheckBox("Enable Wake Word")
        self.wake_check.setChecked(True)
        v_layout.addWidget(self.wake_check)
        v_layout.addStretch()
        tabs.addTab(voice_tab, "Voice")
        sys_tab = QWidget()
        s_layout = QVBoxLayout(sys_tab)
        self.auto_start = QCheckBox("Start with Windows")
        self.auto_start.setChecked(SETTINGS.AUTO_START)
        s_layout.addWidget(self.auto_start)
        s_layout.addStretch()
        tabs.addTab(sys_tab, "System")
        layout.addWidget(tabs)
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def save_settings(self):
        db.save_setting("ai_provider", self.provider_combo.currentText())
        db.save_setting("openai_key", self.api_key.text())
        self.accept()
