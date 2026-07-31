"""News fetching via NewsAPI"""
import requests
import logging

logger = logging.getLogger(__name__)
API_KEY = "YOUR_NEWSAPI_KEY"  # Replace with real key
BASE_URL = "https://newsapi.org/v2/top-headlines"

class News:
    @staticmethod
    def get_headlines(country: str = "us", category: str = None, query: str = None) -> str:
        if API_KEY == "YOUR_NEWSAPI_KEY":
            return "Please set NewsAPI key in modules/news.py"
        try:
            params = {"apiKey": API_KEY, "country": country, "pageSize": 5}
            if category:
                params["category"] = category
            if query:
                params["q"] = query
            r = requests.get(BASE_URL, params=params, timeout=10)
            data = r.json()
            if data.get("status") != "ok":
                return f"Error: {data.get('message')}"
            articles = data.get("articles", [])
            if not articles:
                return "No news found."
            lines = ["📰 Latest News:"]
            for i, a in enumerate(articles[:5], 1):
                lines.append(f"{i}. {a['title']} - {a['source']['name']}")
            return "\n".join(lines)
        except Exception as e:
            return f"News error: {e}"
