from langchain.tools import tool
import requests
import os

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent or real-time information.
    """
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": os.getenv("TAVILY_API_KEY"),
        "query": query,
        "max_results": 3
    }
    response = requests.post(url, json=payload)
    data = response.json()

    return "\n".join([item["content"] for item in data.get("results", [])])
