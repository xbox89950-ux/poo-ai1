"""Poo AI Assistant - Entry Point"""
import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from config.settings import SETTINGS
from gui.main_window import MainWindow
from gui.system_tray import SystemTrayIcon

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    tray = SystemTrayIcon(window=window)
    tray.show()
    if not SETTINGS.START_MINIMIZED:
        window.show()
    logger.info("Poo AI Assistant started")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
