"""Windows startup integration"""
import os
import sys
import logging
from pathlib import Path
import winreg as reg

logger = logging.getLogger(__name__)

class StartupManager:
    APP_NAME = "PooAI"
    REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

    @staticmethod
    def get_executable_path() -> str:
        if getattr(sys, 'frozen', False):
            return sys.executable
        return str(Path(sys.argv[0]).resolve())

    @staticmethod
    def enable_startup():
        try:
            exe_path = StartupManager.get_executable_path()
            with reg.OpenKey(reg.HKEY_CURRENT_USER, StartupManager.REG_PATH, 0, reg.KEY_SET_VALUE) as key:
                reg.SetValueEx(key, StartupManager.APP_NAME, 0, reg.REG_SZ, exe_path)
            return "Auto-start enabled"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def disable_startup():
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, StartupManager.REG_PATH, 0, reg.KEY_SET_VALUE) as key:
                try:
                    reg.DeleteValue(key, StartupManager.APP_NAME)
                    return "Auto-start disabled"
                except FileNotFoundError:
                    return "Auto-start was not enabled"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def is_startup_enabled() -> bool:
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, StartupManager.REG_PATH, 0, reg.KEY_READ) as key:
                reg.QueryValueEx(key, StartupManager.APP_NAME)
                return True
        except:
            return False
