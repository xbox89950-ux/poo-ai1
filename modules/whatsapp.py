"""WhatsApp messaging via pywhatkit"""
import logging
import webbrowser
import urllib.parse
import time
import pyautogui

logger = logging.getLogger(__name__)

class WhatsApp:
    @staticmethod
    def send_message(phone: str, message: str) -> str:
        try:
            import pywhatkit
            pywhatkit.sendwhatmsg_to_instantly(phone, message)
            return f"WhatsApp message sent to {phone}"
        except Exception as e:
            # Fallback: open web whatsapp
            encoded = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded}"
            webbrowser.open(url)
            return f"Opened WhatsApp Web for {phone}. Please send manually."
