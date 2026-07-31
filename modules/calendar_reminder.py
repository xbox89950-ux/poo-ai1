"""Calendar and reminder system"""
import logging
import json
from datetime import datetime, timedelta
from typing import List, Dict
from database.db_manager import db

logger = logging.getLogger(__name__)

class CalendarReminder:
    @staticmethod
    def add_reminder(title: str, datetime_str: str, note: str = "") -> str:
        try:
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            reminder = {
                "title": title,
                "datetime": datetime_str,
                "note": note,
                "created": datetime.now().isoformat()
            }
            existing = db.get_memory("reminders")
            reminders = json.loads(existing) if existing else []
            reminders.append(reminder)
            db.set_memory("reminders", json.dumps(reminders))
            return f"Reminder set: '{title}' at {datetime_str}"
        except ValueError:
            return "Use format: YYYY-MM-DD HH:MM (e.g., 2026-08-01 14:30)"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def list_reminders() -> str:
        existing = db.get_memory("reminders")
        if not existing:
            return "No reminders set"
        reminders = json.loads(existing)
        if not reminders:
            return "No reminders set"
        lines = ["📅 Your Reminders:"]
        for i, r in enumerate(reminders, 1):
            lines.append(f"{i}. {r['title']} - {r['datetime']}")
            if r.get('note'):
                lines.append(f"   Note: {r['note']}")
        return "\n".join(lines)

    @staticmethod
    def delete_reminder(index: int) -> str:
        existing = db.get_memory("reminders")
        if not existing:
            return "No reminders to delete"
        reminders = json.loads(existing)
        if 0 <= index < len(reminders):
            removed = reminders.pop(index)
            db.set_memory("reminders", json.dumps(reminders))
            return f"Deleted: {removed['title']}"
        return "Invalid reminder number"

    @staticmethod
    def check_upcoming() -> str:
        existing = db.get_memory("reminders")
        if not existing:
            return "No upcoming reminders"
        reminders = json.loads(existing)
        now = datetime.now()
        upcoming = []
        for r in reminders:
            try:
                r_dt = datetime.strptime(r["datetime"], "%Y-%m-%d %H:%M")
                if r_dt > now and r_dt < now + timedelta(hours=24):
                    upcoming.append(r)
            except:
                pass
        if not upcoming:
            return "No reminders in next 24 hours"
        lines = ["⏰ Upcoming (24h):"]
        for r in upcoming:
            lines.append(f"- {r['title']} at {r['datetime']}")
        return "\n".join(lines)
