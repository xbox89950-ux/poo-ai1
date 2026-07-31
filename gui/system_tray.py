"""System tray icon and menu"""
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None, window=None):
        super().__init__(parent)
        self.main_window = window
        self.setToolTip("Poo AI Assistant")
        self.menu = QMenu()
        actions = [
            ("Open Assistant", self.show_window),
            ("Start Listening", self.start_listening),
            ("Stop Listening", self.stop_listening),
            None,
            ("Settings", self.open_settings),
            ("Restart", self.restart_app),
            ("Exit", self.exit_app),
        ]
        for item in actions:
            if item is None:
                self.menu.addSeparator()
            else:
                name, callback = item
                action = QAction(name, self)
                action.triggered.connect(callback)
                self.menu.addAction(action)
        self.setContextMenu(self.menu)
        self.activated.connect(self.on_activated)

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()

    def show_window(self):
        if self.main_window:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()

    def start_listening(self):
        if self.main_window:
            self.main_window.start_listening()

    def stop_listening(self):
        if self.main_window:
            self.main_window.stop_listening()

    def open_settings(self):
        pass

    def restart_app(self):
        import os
        import sys
        os.execl(sys.executable, sys.executable, *sys.argv)

    def exit_app(self):
        QApplication.instance().quit()
