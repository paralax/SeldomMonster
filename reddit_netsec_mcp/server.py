import logging
import json
import time
from typing import Any, Dict, List
from urllib.parse import quote

import aiohttp
from mcp.server.fastmcp import FastMCP

SERVER_NAME = "reddit-netsec-mcp"

mcp = FastMCP(SERVER_NAME)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(SERVER_NAME)

SUBREDDITS = [
    "blueteamsec",
    "netsec",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

@mcp.tool()
async def get_recent_headlines() -> List[Dict[str, Any]]:
    """
    Name: get_recent_headlines
    Description: Returns the most recent cybersecurity headlines from the appropriate subreddits
    Parameters: None
    """
    data = {}
    for sub in SUBREDDITS:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.reddit.com/r/{sub}.json", headers=HEADERS) as response:
                resp = await response.json()
                for entry in resp['data']['children']:
                    data[entry['data']["url"]] = {
                        "url": entry['data']["url"],
                        "date": time.asctime(time.gmtime(entry['data']["created_utc"])),
                        "title": entry['data']["title"],
                        "text": entry['data']["selftext"],
                    }
    return list(data.values())[:10]

@mcp.tool()
async def search_cybersecurity(term: str) -> List[Dict[str, Any]]:
    """
    Name: search_cybersecurity
    Description: Returns search results for the term the cybersecurity headlines from the appropriate subreddits
    Parameters:
        term (required): The string to search for
    """
    data = {}
    term = quote(term)
    for sub in SUBREDDITS:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.reddit.com/r/blueteamsec/search.json?q={term}&restrict_sr=on&sort=relevance&t=all",
                headers=HEADERS
            ) as response:
                resp = await response.json()
                for entry in resp['data']['children']:
                    data[entry['data']["url"]] = {
                        "url": entry['data']["url"],
                        "date": time.asctime(time.gmtime(entry['data']["created_utc"])),
                        "title": entry['data']["title"],
                        "text": entry['data']["selftext"],
                    }
    return list(data.values())[:10]


"""
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
agent_reddit = LlmAgent(
    # LiteLLM connects to local Ollama server
    model=LiteLlm(model="ollama/gemma3:latest"),
    name="agent_reddit",
    description="Reddit cybersecurity news service.",
    instruction="You are Reddit communicating with Gemma, report back what Reddits says about cybersecurity news. Provide a bulleted list from the results with dates, headlines, and URLs.",
    tools=[search_cybersecurity, get_recent_headlines],
)

root_agent=agent_reddit
"""


def main() -> None:
    logger.info("Starting Reddit Netsec MCP server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
