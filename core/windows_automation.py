"""Windows automation: apps, system, volume, screenshots"""
import os
import subprocess
import logging
import pyautogui
import psutil
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class WindowsAutomation:
    APP_MAP = {
        "chrome": "chrome", "ক্রোম": "chrome",
        "edge": "msedge", "এজ": "msedge",
        "firefox": "firefox", "ফায়ারফক্স": "firefox",
        "vs code": "code", "ভিএস কোড": "code", "vscode": "code",
        "notepad": "notepad", "নোটপ্যাড": "notepad",
        "paint": "mspaint", "পেইন্ট": "mspaint",
        "calculator": "calc", "ক্যালকুলেটর": "calc",
        "task manager": "taskmgr",
        "cmd": "cmd", "command prompt": "cmd",
        "powershell": "powershell",
        "file explorer": "explorer", "explorer": "explorer",
        "settings": "ms-settings:", "সেটিংস": "ms-settings:",
        "control panel": "control",
        "word": "winword", "excel": "excel", "powerpoint": "powerpnt",
        "spotify": "spotify", "discord": "discord",
    }

    @staticmethod
    def open_app(app_name: str) -> str:
        key = app_name.lower().strip()
        cmd = WindowsAutomation.APP_MAP.get(key, key)
        try:
            if cmd.startswith("ms-"):
                os.system(f"start {cmd}")
            else:
                subprocess.Popen(f"start {cmd}", shell=True)
            return f"Opened {app_name}"
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return f"Sorry, couldn't open {app_name}"

    @staticmethod
    def close_app(app_name: str) -> str:
        key = app_name.lower().strip()
        proc_name = WindowsAutomation.APP_MAP.get(key, key)
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc_name in proc.info['name'].lower():
                    psutil.Process(proc.info['pid']).terminate()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return f"Closed {app_name}" if killed else f"Couldn't find {app_name} running"

    @staticmethod
    def take_screenshot(save_path: Optional[str] = None) -> str:
        if not save_path:
            desktop = Path.home() / "Desktop"
            save_path = desktop / f"poo_screenshot_{os.getpid()}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return f"Screenshot saved to {save_path}"

    @staticmethod
    def control_volume(action: str, amount: int = 10) -> str:
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            if action == "mute":
                volume.SetMute(1, None)
                return "Volume muted"
            elif action == "unmute":
                volume.SetMute(0, None)
                return "Volume unmuted"
            elif action in ("up", "down"):
                current = volume.GetMasterVolumeLevelScalar()
                delta = amount / 100.0
                new_vol = min(1.0, max(0.0, current + (delta if action == "up" else -delta)))
                volume.SetMasterVolumeLevelScalar(new_vol, None)
                return f"Volume {'increased' if action == 'up' else 'decreased'} to {int(new_vol*100)}%"
        except Exception:
            if action == "up":
                pyautogui.press("volumeup", presses=amount//2)
            elif action == "down":
                pyautogui.press("volumedown", presses=amount//2)
            elif action == "mute":
                pyautogui.press("volumemute")
            return f"Volume {action}"

    @staticmethod
    def system_action(action: str) -> str:
        commands = {
            "shutdown": "shutdown /s /t 60",
            "restart": "shutdown /r /t 60",
            "sleep": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0",
            "lock": "rundll32.exe user32.dll,LockWorkStation",
            "hibernate": "shutdown /h",
        }
        if action in commands:
            if action in ("shutdown", "restart"):
                return f"CONFIRM_REQUIRED:{action}"
            os.system(commands[action])
            return f"Executing {action}"
        return "Unknown system action"

    @staticmethod
    def create_folder(path: str) -> str:
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return f"Folder created: {path}"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def empty_recycle_bin() -> str:
        try:
            import winshell
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            return "Recycle bin emptied"
        except Exception:
            os.system("rd /s /q C:\\$Recycle.Bin")
            return "Recycle bin emptied"

    @staticmethod
    def type_text(text: str):
        pyautogui.typewrite(text, interval=0.01)
        return "Typed text"
