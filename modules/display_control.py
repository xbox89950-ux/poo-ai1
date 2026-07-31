"""Display brightness and wallpaper control"""
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class DisplayControl:
    @staticmethod
    def set_brightness(level: int) -> str:
        """level: 0-100"""
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except ImportError:
            # Fallback using WMI
            try:
                import wmi
                c = wmi.WMI(namespace='wmi')
                methods = c.WmiMonitorBrightnessMethods()[0]
                methods.WmiSetBrightness(level, 0)
                return f"Brightness set to {level}%"
            except Exception as e:
                return f"Brightness error: {e}"

    @staticmethod
    def get_brightness() -> str:
        try:
            import screen_brightness_control as sbc
            return f"Current brightness: {sbc.get_brightness()[0]}%"
        except:
            return "Cannot read brightness"

    @staticmethod
    def set_wallpaper(path: str) -> str:
        try:
            import ctypes
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(Path(path).absolute()), 3)
            return f"Wallpaper changed to {path}"
        except Exception as e:
            return f"Wallpaper error: {e}"
