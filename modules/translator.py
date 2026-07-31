"""Translation utility"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Translator:
    @staticmethod
    def translate(text: str, target_lang: str = "en", source_lang: str = "auto") -> str:
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            return translator.translate(text)
        except ImportError:
            # Fallback using requests
            try:
                import requests
                url = "https://translate.googleapis.com/translate_a/single"
                params = {
                    "client": "gtx",
                    "sl": source_lang,
                    "tl": target_lang,
                    "dt": "t",
                    "q": text
                }
                r = requests.get(url, params=params, timeout=10)
                data = r.json()
                translated = "".join([s[0] for s in data[0]])
                return translated
            except Exception as e:
                return f"Translation error: {e}"
        except Exception as e:
            return f"Translation error: {e}"

    @staticmethod
    def detect_language(text: str) -> str:
        try:
            from deep_translator import GoogleTranslator
            return GoogleTranslator().detect(text)
        except:
            bengali_range = range(0x0980, 0x09FF)
            if any(ord(c) in bengali_range for c in text):
                return "bn"
            return "en"
