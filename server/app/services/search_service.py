import requests
from app.core.config import TAVILY_API_KEY

def tavily_search(keyword):

    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": keyword,
            "search_depth": "advanced"
        }
    )

    return response.json()