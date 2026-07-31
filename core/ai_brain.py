"""AI Brain: OpenAI / Ollama integration with memory"""
import logging
from typing import List, Dict, Any
from openai import OpenAI
import ollama
from config.settings import SETTINGS
from database.db_manager import db

logger = logging.getLogger(__name__)

class AIBrain:
    def __init__(self):
        self.provider = SETTINGS.DEFAULT_AI_PROVIDER
        self.openai_client = OpenAI(api_key=SETTINGS.OPENAI_API_KEY) if SETTINGS.OPENAI_API_KEY else None

        self.system_prompt = """You are Poo, a helpful Windows AI assistant. 
You understand Bengali (বাংলা), English, and Banglish naturally.
Keep responses concise but helpful. You can generate code, control Windows, and answer questions.
When generating code, wrap it in markdown code blocks with the language specified.
If the user speaks Bengali, reply in Bengali. If English, reply in English."""

    def _build_messages(self, user_input: str) -> List[Dict[str, str]]:
        messages = [{"role": "system", "content": self.system_prompt}]
        context = db.get_recent_context(limit=5)
        for item in context:
            messages.append({"role": "user", "content": item["user"]})
            messages.append({"role": "assistant", "content": item["ai"]})
        messages.append({"role": "user", "content": user_input})
        return messages

    async def think(self, user_input: str) -> str:
        messages = self._build_messages(user_input)
        response = ""
        try:
            if self.provider == "openai" and self.openai_client:
                resp = self.openai_client.chat.completions.create(
                    model=SETTINGS.OPENAI_MODEL,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1500
                )
                response = resp.choices[0].message.content
            elif self.provider == "ollama":
                resp = ollama.chat(model=SETTINGS.OLLAMA_MODEL, messages=messages)
                response = resp['message']['content']
            else:
                response = "No AI provider configured. Set OPENAI_API_KEY or start Ollama."
        except Exception as e:
            logger.error(f"AI error: {e}")
            response = "Sorry, I'm having trouble thinking right now."

        db.save_conversation(user_input, response)
        return response

    def set_provider(self, provider: str):
        self.provider = provider
        db.set_memory("ai_provider", provider)
