# https://greynoise.readthedocs.io/en/latest/tutorial.html#api-client

import logging
import os
from typing import Any, Dict, List

import aiohttp
from mcp.server.fastmcp import FastMCP

SERVER_NAME = "greynoise-mcp"

mcp = FastMCP(SERVER_NAME)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(SERVER_NAME)
BASE_URL = "https://api.greynoise.io/v3/community/"
HEADERS = {"accept": "application/json", "key": os.getenv("GREYNOISE_API_KEY")}

@mcp.tool()
async def search_one_greynoise(ip: str) -> List[Dict[str, Any]]:
    """
    Name: search_one_greynoise
    Description: Check if a given IP addresses are considered internet noise or have been observed scanning or attacking devices across the Internet.
    Parameters:
    ip (required): The IP addresses to get context from

    Returns:
    A data structure containing information about the IP address including the organization name and if it's bening or suspicious. 
    """
    logger.info(f"Querying GreyNoise events for {ip}")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}{ip}", headers=HEADERS) as response:
            data = await response.text()
    return data

def main() -> None:
    logger.info("Starting GreyNoise MCP server")
    mcp.run(transport="stdio")

"""
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

agent_greynoise = LlmAgent(
    # LiteLLM connects to local Ollama server
    model=LiteLlm(model="ollama/gemma:3b"),
    name="agent_greynoise",
    instructions="You are Greynoise communicating with Gemma",
    tools=[search__one_greynoise],
)
"""

if __name__ == "__main__":
    main()
