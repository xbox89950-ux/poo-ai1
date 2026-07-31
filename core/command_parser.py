"""Parse natural language (BN/EN/Banglish) into structured actions"""
import re
import logging
from typing import Tuple, Optional
from core.windows_automation import WindowsAutomation

logger = logging.getLogger(__name__)

class CommandParser:
    PATTERNS = {
        # === WINDOWS AUTOMATION ===
        "open_app": [
            r"(?:open|launch|start|খোলো|চালু করো|চালাও)\s+(.+)",
            r"(?:show me|দেখাও)\s+(.+)"
        ],
        "close_app": [
            r"(?:close|quit|exit|বন্ধ করো)\s+(.+)"
        ],
        "screenshot": [
            r"(?:screenshot|screen shot|স্ক্রিনশট|screenshot নাও|screen shot নাও)"
        ],
        "volume": [
            r"(?:volume|sound|আওয়াজ|ভলিউম)\s+(up|down|mute|unmute|বাড়াও|কমাও|বন্ধ করো|চালু করো)",
            r"(?:mute|unmute|বন্ধ করো|চালু করো)\s+(?:volume|sound|আওয়াজ)?"
        ],
        "system": [
            r"(?:shutdown|restart|sleep|lock|hibernate|বন্ধ করো|রিস্টার্ট|লক করো)\s+(?:computer|pc|কম্পিউটার)?"
        ],
        "create_folder": [
            r"(?:create|make|তৈরি করো)\s+(?:a\s+)?(?:folder|directory|ফোল্ডার)\s+(?:in|at|এ|তে)?\s*(.*)"
        ],
        "empty_trash": [
            r"(?:empty|clean|খালি করো)\s+(?:trash|recycle|রিসাইকেল|বিন)"
        ],
        "type": [
            r"(?:type|লিখো)\s+(.+)"
        ],

        # === WEB & SEARCH ===
        "search_web": [
            r"(?:search|google|খুঁজো|সার্চ করো)\s+(?:for|এ)?\s*(.+)"
        ],
        "youtube": [
            r"(?:youtube|ইউটিউব)\s+(?:search|খুঁজো)?\s*(.*)"
        ],
        "open_website": [
            r"(?:open|go to|visit|খোলো)\s+(?:website|site|ওয়েবসাইট)?\s*(.+\..+)"
        ],

        # === CODE ===
        "code": [
            r"(?:generate|create|write|বানাও|লিখো)\s+(?:a\s+)?(.+?)\s+(?:code|program|app|script|প্রোগ্রাম)"
        ],
        "run_code": [
            r"(?:run|execute|চালাও)\s+(?:this\s+)?(?:code|program|প্রোগ্রাম)"
        ],

        # === WEATHER ===
        "weather": [
            r"(?:weather|temperature|আবহাওয়া|তাপমাত্রা)\s+(?:in|of|এ|এর)?\s*(.*)"
        ],

        # === NEWS ===
        "news": [
            r"(?:news|খবর|সংবাদ)"
        ],

        # === SYSTEM INFO ===
        "system_info": [
            r"(?:system info|pc info|computer info|cpu|ram|battery|সিস্টেম|কম্পিউটার তথ্য)"
        ],

        # === DISPLAY ===
        "brightness": [
            r"(?:brightness|screen|ডিসপ্লে)\s+(?:set|adjust|কমাও|বাড়াও)?\s*(\d+)?"
        ],
        "wallpaper": [
            r"(?:wallpaper|background|ওয়ালপেপার)\s+(?:set|change|পাল্টাও)?\s*(.*)"
        ],

        # === MUSIC ===
        "play_music": [
            r"(?:play|music|song|গান|বাজাও)\s+(?:music|song|গান)?\s*(.*)"
        ],
        "stop_music": [
            r"(?:stop|pause)\s+(?:music|song|গান)"
        ],

        # === CALCULATOR ===
        "calculate": [
            r"(?:calculate|compute|solve|হিসাব|গণনা)\s+(.+)"
        ],
        "currency": [
            r"(?:convert|currency|মুদ্রা)\s+(\d+)\s*(\w+)\s+(?:to|in|to|এ)\s*(\w+)"
        ],

        # === TRANSLATION ===
        "translate": [
            r"(?:translate|অনুবাদ)\s+(.+)\s+(?:to|in|এ)\s*(\w+)"
        ],

        # === TIME ===
        "time": [
            r"(?:time|what time|সময়|কত বাজে)"
        ],
        "date": [
            r"(?:date|day|today|তারিখ|আজ কত)"
        ],

        # === JOKES ===
        "joke": [
            r"(?:joke|funny|jokes|কৌতুক|মজা)"
        ],

        # === CLIPBOARD ===
        "clipboard": [
            r"(?:clipboard|copy history|ক্লিপবোর্ড)"
        ],

        # === WIFI ===
        "wifi": [
            r"(?:wifi|wi-fi|ওয়াইফাই)\s*(on|off|চালু|বন্ধ|status|status)?"
        ],

        # === BLUETOOTH ===
        "bluetooth": [
            r"(?:bluetooth|ব্লুটুথ)\s*(on|off|চালু|বন্ধ)?"
        ],

        # === TIMER ===
        "timer": [
            r"(?:timer|set timer|টাইমার)\s+(\d+)\s*(?:seconds|minutes|hours|second|minute|hour|সেকেন্ড|মিনিট|ঘণ্টা)?"
        ],

        # === REMINDER ===
        "reminder": [
            r"(?:remind|reminder|মনে করিয়ে)\s+(?:me\s+)?(?:to|about|যে)?\s*(.+)\s+(?:at|on|এ)\s*(.+)",
            r"(?:add reminder|reminder add|রিমাইন্ডার)\s+(.+)\s+(?:at|on|এ)\s*(.+)"
        ],

        # === PDF ===
        "read_pdf": [
            r"(?:read|open|খোলো)\s+(?:pdf|পিডিএফ)\s*(.*)"
        ],

        # === OCR ===
        "ocr": [
            r"(?:ocr|read text|text from|screenshot text|ছবি থেকে লেখা)"
        ],

        # === EMAIL ===
        "email": [
            r"(?:send email|email|ইমেইল)\s+(?:to|কে)?\s*(.+)"
        ],

        # === WHATSAPP ===
        "whatsapp": [
            r"(?:whatsapp|message|মেসেজ)\s+(?:to|কে)?\s*(.+)"
        ],

        # === VOICE RECORD ===
        "record": [
            r"(?:record|voice record|রেকর্ড|অডিও রেকর্ড)"
        ],

        # === FACTS ===
        "fact": [
            r"(?:fact|facts|trivia|তথ্য|জানা)"
        ],

        # === COIN/DICE ===
        "coin": [
            r"(?:flip coin|coin flip|মুদ্রা|টস)"
        ],
        "dice": [
            r"(?:roll dice|dice|পাশা)"
        ],
    }

    @staticmethod
    def parse(command: str) -> Tuple[str, Optional[str], Optional[str]]:
        cmd_lower = command.lower().strip()

        for intent, patterns in CommandParser.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, cmd_lower, re.IGNORECASE)
                if match:
                    groups = match.groups()

                    # Windows automation
                    if intent == "open_app":
                        return ("automation", "open_app", groups[0].strip())
                    elif intent == "close_app":
                        return ("automation", "close_app", groups[0].strip())
                    elif intent == "screenshot":
                        return ("automation", "screenshot", None)
                    elif intent == "volume":
                        vol = groups[0].strip()
                        mapping = {"বাড়াও": "up", "কমাও": "down", "বন্ধ করো": "mute", "চালু করো": "unmute"}
                        return ("automation", "volume", mapping.get(vol, vol))
                    elif intent == "system":
                        return ("system", "confirm", match.group(0))
                    elif intent == "create_folder":
                        return ("automation", "create_folder", groups[0].strip() if groups else None)
                    elif intent == "empty_trash":
                        return ("automation", "empty_trash", None)
                    elif intent == "type":
                        return ("automation", "type", groups[0].strip())

                    # Web
                    elif intent == "search_web":
                        return ("web", "search_google", groups[0].strip())
                    elif intent == "youtube":
                        return ("web", "search_youtube", groups[0].strip() if groups and groups[0] else "music")
                    elif intent == "open_website":
                        return ("web", "open_website", groups[0].strip())

                    # Code
                    elif intent == "code":
                        return ("code", "generate", groups[0].strip())
                    elif intent == "run_code":
                        return ("code", "run", None)

                    # Weather
                    elif intent == "weather":
                        city = groups[0].strip() if groups and groups[0] else "Dhaka"
                        return ("info", "weather", city)

                    # News
                    elif intent == "news":
                        return ("info", "news", None)

                    # System Info
                    elif intent == "system_info":
                        return ("info", "system_info", None)

                    # Display
                    elif intent == "brightness":
                        level = groups[0] if groups and groups[0] else "50"
                        return ("control", "brightness", level)
                    elif intent == "wallpaper":
                        return ("control", "wallpaper", groups[0].strip() if groups and groups[0] else "")

                    # Music
                    elif intent == "play_music":
                        return ("media", "play_music", groups[0].strip() if groups and groups[0] else "")
                    elif intent == "stop_music":
                        return ("media", "stop_music", None)

                    # Calculator
                    elif intent == "calculate":
                        return ("math", "calculate", groups[0].strip())
                    elif intent == "currency":
                        return ("math", "currency", f"{groups[0]}:{groups[1]}:{groups[2]}")

                    # Translation
                    elif intent == "translate":
                        return ("text", "translate", f"{groups[0]}:{groups[1]}")

                    # Time
                    elif intent == "time":
                        return ("info", "time", None)
                    elif intent == "date":
                        return ("info", "date", None)

                    # Jokes
                    elif intent == "joke":
                        return ("fun", "joke", None)

                    # Clipboard
                    elif intent == "clipboard":
                        return ("tool", "clipboard", None)

                    # Network
                    elif intent == "wifi":
                        action = groups[0] if groups and groups[0] else "status"
                        mapping = {"চালু": "on", "বন্ধ": "off", "status": "status"}
                        return ("network", "wifi", mapping.get(action, action))
                    elif intent == "bluetooth":
                        action = groups[0] if groups and groups[0] else "on"
                        mapping = {"চালু": "on", "বন্ধ": "off"}
                        return ("network", "bluetooth", mapping.get(action, action))

                    # Timer
                    elif intent == "timer":
                        return ("tool", "timer", groups[0])

                    # Reminder
                    elif intent == "reminder":
                        return ("tool", "reminder", f"{groups[0]}:{groups[1]}")

                    # PDF
                    elif intent == "read_pdf":
                        return ("doc", "read_pdf", groups[0].strip() if groups and groups[0] else "")

                    # OCR
                    elif intent == "ocr":
                        return ("tool", "ocr", None)

                    # Email
                    elif intent == "email":
                        return ("comm", "email", groups[0].strip() if groups else "")

                    # WhatsApp
                    elif intent == "whatsapp":
                        return ("comm", "whatsapp", groups[0].strip() if groups else "")

                    # Record
                    elif intent == "record":
                        return ("tool", "record", None)

                    # Fact
                    elif intent == "fact":
                        return ("fun", "fact", None)

                    # Coin/Dice
                    elif intent == "coin":
                        return ("fun", "coin", None)
                    elif intent == "dice":
                        return ("fun", "dice", None)

        return ("ai_chat", None, command)

    @staticmethod
    def execute_automation(action: str, target: Optional[str]) -> str:
        if action == "open_app":
            return WindowsAutomation.open_app(target)
        elif action == "close_app":
            return WindowsAutomation.close_app(target)
        elif action == "screenshot":
            return WindowsAutomation.take_screenshot()
        elif action == "volume":
            return WindowsAutomation.control_volume(target or "up")
        elif action == "create_folder":
            if not target:
                target = str(Path.home() / "Desktop" / "New Folder")
            return WindowsAutomation.create_folder(target)
        elif action == "empty_trash":
            return WindowsAutomation.empty_recycle_bin()
        elif action == "type":
            return WindowsAutomation.type_text(target or "")
        elif action == "system_action":
            return WindowsAutomation.system_action(target)
        return "Unknown automation"
