#!/usr/bin/env python3

import logging
import os
from typing import Any, List

import aiohttp
from mcp.server.fastmcp import FastMCP

NAME="yarahub-simple-mcp"

mcp = FastMCP(NAME)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(NAME)

YARAHUB_BASE_URL="https://yaraify-api.abuse.ch/api/v1/"
YARAHUB_AUTH_KEY = os.getenv("YARAHUB_AUTH_KEY")


@mcp.tool()
async def search_yara_rules(search_term: str) -> List[Any]:
    """
    Name: search_yara_rules
    Description: Returns a sequence of Yara rules matching a given term
    Parameters:
    term (required): The string to search for 
    """
    # https://yaraify.abuse.ch/api/#get-yara -> iterate here:
    # https://yaraify.abuse.ch/api/#download-yara 
    payload = {
        "query": "get_yara",
        "search_term": search_term
    }
    headers = {
        "Auth-Key": YARAHUB_AUTH_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            YARAHUB_BASE_URL,
            data=payload,
            headers=headers
            ) as response:
            result = await response.json()
    data = []
    for item in result['data']:
        for task in data.get('data', {}).get('tasks', []):
            for static_result in task.get('static_results', []):
                if static_result.get('yarahub_uuid', False):
                    yarahub_uuid = static_result['yarahub_uuid']
                    payload = {
                        "query": "get_yara_rule",
                        "uuid": yarahub_uuid
                    }
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            YARAHUB_BASE_URL,
                            data=payload,
                            headers=headers
                        ) as response:
                            rule_result = await response.text()
                            data.append(rule_result)
    return data

def main() -> None:
    logger.info("Starting simple YaraHub MCP server")
    mcp.run(transport='stdio')        

if __name__ == "__main__":
    main()