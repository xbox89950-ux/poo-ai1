"""Web search and browsing utilities"""
import logging
import webbrowser
import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

logger = logging.getLogger(__name__)

class WebSearch:
    @staticmethod
    def search_google(query: str) -> str:
        encoded = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded}"
        webbrowser.open(url)
        return f"Searching Google for: {query}"

    @staticmethod
    def search_youtube(query: str) -> str:
        encoded = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url)
        return f"Searching YouTube for: {query}"

    @staticmethod
    def open_website(url: str) -> str:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opening: {url}"

    @staticmethod
    def read_webpage(url: str) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            lines = [l for l in text.splitlines() if l.strip()]
            return "\n".join(lines[:50])
        except Exception as e:
            return f"Error reading page: {e}"

    @staticmethod
    def summarize_webpage(url: str) -> str:
        content = WebSearch.read_webpage(url)
        if content.startswith("Error"):
            return content
        return f"Page content (first part):\n{content[:2000]}..."
