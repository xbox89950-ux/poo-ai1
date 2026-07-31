"""OCR - Extract text from images"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class OCR:
    @staticmethod
    def extract_text(image_path: str) -> str:
        try:
            import pytesseract
            from PIL import Image

            # Set tesseract path for Windows
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='eng+ben')
            return f"Extracted text:\n{text[:1000]}"
        except ImportError:
            return "pytesseract not installed. Run: pip install pytesseract pillow"
        except Exception as e:
            return f"OCR error: {e}"

    @staticmethod
    def extract_from_screenshot() -> str:
        try:
            import pyautogui
            from PIL import Image
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

            screenshot = pyautogui.screenshot()
            text = pytesseract.image_to_string(screenshot, lang='eng+ben')
            return f"Screenshot text:\n{text[:1000]}"
        except Exception as e:
            return f"Screenshot OCR error: {e}"
