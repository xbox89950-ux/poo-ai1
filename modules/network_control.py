"""Wi-Fi and Bluetooth control"""
import os
import logging
import subprocess

logger = logging.getLogger(__name__)

class NetworkControl:
    @staticmethod
    def wifi_on() -> str:
        os.system("netsh interface set interface "Wi-Fi" enabled")
        return "Wi-Fi enabled"

    @staticmethod
    def wifi_off() -> str:
        os.system("netsh interface set interface "Wi-Fi" disabled")
        return "Wi-Fi disabled"

    @staticmethod
    def wifi_status() -> str:
        try:
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], 
                                  capture_output=True, text=True, timeout=5)
            lines = result.stdout.split("\n")
            for line in lines:
                if "SSID" in line or "Signal" in line or "State" in line:
                    return line.strip()
            return "Wi-Fi status retrieved"
        except Exception as e:
            return f"Wi-Fi status error: {e}"

    @staticmethod
    def bluetooth_on() -> str:
        # Using Windows settings
        os.system("start ms-settings:bluetooth")
        return "Bluetooth settings opened"

    @staticmethod
    def bluetooth_off() -> str:
        os.system("start ms-settings:bluetooth")
        return "Bluetooth settings opened"

    @staticmethod
    def list_wifi() -> str:
        try:
            result = subprocess.run(["netsh", "wlan", "show", "profiles"], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout
        except Exception as e:
            return f"Error: {e}"
