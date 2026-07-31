"""Date and time utilities"""
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DateTimeUtil:
    @staticmethod
    def get_time() -> str:
        now = datetime.now()
        return f"Current time: {now.strftime('%I:%M %p')}"

    @staticmethod
    def get_date() -> str:
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"

    @staticmethod
    def get_datetime() -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_day() -> str:
        return f"Today is {datetime.now().strftime('%A')}"

    @staticmethod
    def countdown_to(target_date: str) -> str:
        try:
            target = datetime.strptime(target_date, "%Y-%m-%d")
            diff = target - datetime.now()
            days = diff.days
            return f"{days} days until {target_date}"
        except:
            return "Use format: YYYY-MM-DD"
