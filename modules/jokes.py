"""Jokes and fun facts"""
import random
import logging
import requests

logger = logging.getLogger(__name__)

class Jokes:
    BENGALI_JOKES = [
        "একজন প্রোগ্রামার কেন গাছে উঠলো? — কারণ সে বাগ (bug) ধরতে চাইছিলো!",
        "কম্পিউটার কেন ঠান্ডা খাবার পছন্দ করে? — কারণ এর মধ্যে অনেক ফ্যান (fan) আছে!",
        "বাংলাদেশের সবচেয়ে দ্রুত ইন্টারনেট কোথায়? — যেখানে রাউটারের পাশে বসে!",
        "একজন ডেভেলপার কেন বিয়ে করলো না? — কারণ সে commit করতে ভয় পায়!",
        "কেন পাইথন সাপের মতো? — কারণ সে কামড়ায় না, শুধু squeeze করে!",
    ]

    ENGLISH_JOKES = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the developer go broke? Because he used up all his cache!",
        "Why do Java developers wear glasses? Because they don't C#!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        "Why was the function sad? It didn't get any calls!",
    ]

    @staticmethod
    def get_joke(lang: str = "en") -> str:
        if lang == "bn":
            return random.choice(Jokes.BENGALI_JOKES)
        return random.choice(Jokes.ENGLISH_JOKES)

    @staticmethod
    def get_fact() -> str:
        try:
            r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=5)
            return r.json().get("text", "No fact available")
        except:
            facts = [
                "Honey never spoils. Archaeologists have found 3000-year-old honey still edible!",
                "Octopuses have three hearts and blue blood!",
                "Bananas are berries, but strawberries are not!",
            ]
            return random.choice(facts)

    @staticmethod
    def flip_coin() -> str:
        return random.choice(["Heads!", "Tails!"])

    @staticmethod
    def roll_dice(sides: int = 6) -> str:
        return f"Rolled: {random.randint(1, sides)}"
