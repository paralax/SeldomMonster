# https://www.ransomware.live/api

import logging
from typing import Any, Dict, List

import aiohttp
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ransomware-live-mcp")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ransomware-live-mcp")

RANSOMWARE_LIVE_BASE_URL="https://api.ransomware.live/v2"

"""
async def fetch_data(url: str) -> List[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return data
"""

@mcp.tool()
async def recentcyberattacks() -> List[Dict[str, Any]]:
    """
    Name: recentcyberattacks
    Description: List recently added cyberattacks
    Parameters: None
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/recentcyberattacks"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]

@mcp.tool()
async def search_ransomware(term: str) -> List[Dict[str, Any]]:
    """
    Name: search_ransomware
    Description: Search ransomware victim announcements by keyword. Returns a list of events describing the date, claim URL, victim's country, name, and industry, and the attacking group.
    Parameters:
    term (required): The string to search for 
    """
    logger.info(f"Querying ransomware events for term: {term}")
    url = f"{RANSOMWARE_LIVE_BASE_URL}/searchvictims/{term}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]

@mcp.tool()
async def recent_ransomware() -> List[Dict[str, Any]]:
    """
    Name: recent_ransomware
    Description: Latest disclosed victims for all groups. Returns a list of events describing the date, claim URL, victim's country, name, and industry, and the attacking group.
    Parameters:
    None
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/recentvictims"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]

@mcp.tool()
async def groupvictims(group: str) -> List[Dict[str, Any]]:
    """
    Name: groupvictims
    Description: Search the latest disclosed victims by group. Returns a list of events describing the date, claim URL, victim's country, name, and industry, and the attacking group.
    Parameters:
    group (required): The group to search for 
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/groupvictims/{group}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]

@mcp.tool()
async def groupdetails(group: str) -> List[Dict[str, Any]]:
    """
    Name: groupdetails
    Description: Details about a ransomware group. 
    Parameters:
    group (required): The group to search for 
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/group/{group}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]   

@mcp.tool()
async def searchvictims(term: str) -> List[Dict[str, Any]]:
    """
    Name: searchvictims
    Description: Search for ransomware events by victim name. Returns a list of events describing the date, claim URL, victim's country, name, and industry, and the attacking group.
    Parameters:
    term (required): The victim term to search for 
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/searchvictims/{term}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]   

@mcp.tool()
async def sectorvictims(sector: str) -> List[Dict[str, Any]]:
    """
    Name: sectorvictims
    Description: Search for ransomware events by victim sector. Returns a list of events describing the date, claim URL, victim's country, name, and industry, and the attacking group.
    Parameters:
    sector (required): The sector term to search for 
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/sectorvictims/{sector}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]

@mcp.tool()
async def sector_country_victims(sector: str, countrycode: str) -> List[Dict[str, Any]]:
    """
    Name: sector_country_victims
    Description: Search for ransomware events by victim sector and country. Returns a list of events describing the date, claim URL, victim's country, name, and industry, and the attacking group.
    Parameters:
    sector (required): The sector term to search for 
    countrycode (required): The sector term to search for as a 2-letter country code
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/sectorvictims/{sector}/{countrycode}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]  

@mcp.tool()
async def group_yara_rules(group: str) -> List[Dict[str, Any]]:
    """
    Name: group_yara_rules
    Description: Search for Yara rules associated with a ransomware group
    Parameters:
    group (required): The sector term to search for 
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/yara/{group}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
    return data 

@mcp.tool()
async def countrycyberattacks(countrycode: str) -> List[Dict[str, Any]]:
    """
    Name: countrycyberattacks
    Description: Search for victims by country code. Returns a list of events describing the date, claim URL, victim's country, name, and industry, and the attacking group.
    Parameters:
    group (required): The two letter country code to search for 
    """
    url = f"{RANSOMWARE_LIVE_BASE_URL}/countrycyberattacks/{countrycode}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return list(data)[:10]  

def main() -> None:
    logger.info("Starting ransomware.live MCP server")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()