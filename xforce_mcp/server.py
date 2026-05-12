from base64 import b64encode
import os
import httpx
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

# 1. Initialize FastMCP Server
# FastMCP uses the docstrings and type hints to generate the tool's schema for the LLM.
mcp = FastMCP(
    name="XForceThreatIntelligence",
    instructions="A threat intelligence server for looking up IP reputation and Passive DNS records using the IBM X-Force Exchange API.",
    dependencies=["httpx"]
)

# 2. Configure the HTTP Client (Client is created once for efficiency)
XFORCE_BASE_URL = "https://api.xforce.ibmcloud.com"

# The client is initialized globally and relies on environment variables for auth
# It uses Basic Auth (API Key as user, API Password as password)
try:
    API_KEY = os.environ["XFORCE_API_KEY"]
    API_PASSWORD = os.environ["XFORCE_API_PASSWORD"]
    AUTH = 'Basic ' + b64encode(f"{API_KEY}:{API_PASSWORD}".encode()).decode()
except KeyError:
    print("FATAL: Please set XFORCE_API_KEY and XFORCE_API_PASSWORD environment variables.")
    # In a production server, you would handle this error more gracefully or exit.
    AUTH = None

# Async HTTP Client for non-blocking requests
XFORCE_CLIENT = httpx.AsyncClient(base_url=XFORCE_BASE_URL, headers={'Authorization': AUTH}, timeout=10.0)


# 3. Define the IP Reputation Tool
@mcp.tool()
async def get_ip_reputation(ip_address: str) -> Dict[str, Any]:
    """
    Retrieves the reputation report for a specified IP address.
    The report includes risk score, geolocation, and categorization.
    
    Args:
        ip_address: The IPv4 or IPv6 address to check (e.g., "9.9.9.9").
        
    Returns:
        A dictionary containing the full IP reputation data from X-Force Exchange.
    """
    if not AUTH:
        return {"error": "X-Force API credentials are not configured on the server."}
        
    endpoint = f"/api/ipr/{ip_address}"
    try:
        response = await XFORCE_CLIENT.get(endpoint)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve IP reputation. Check the IP format or API subscription status."}
    except httpx.RequestError as e:
        return {"error": f"Network error during X-Force API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


# 4. Define the Passive DNS Tool
@mcp.tool()
async def get_passive_dns(hostname_or_ip: str) -> Dict[str, Any]:
    """
    Searches for Passive DNS records associated with a given IP address or hostname.
    Passive DNS reveals historical mappings of IPs to domains and vice-versa.
    
    Args:
        hostname_or_ip: The IP address or domain/hostname (e.g., "ibm.com" or "9.9.9.9").
        
    Returns:
        A dictionary containing the passive DNS history for the indicator.
    """
    if not AUTH:
        return {"error": "X-Force API credentials are not configured on the server."}
        
    # X-Force uses the /resolve endpoint for WHOIS/Passive DNS lookups on an indicator
    endpoint = f"/api/url/passive_dns/{hostname_or_ip}"
    try:
        response = await XFORCE_CLIENT.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve Passive DNS. Check the input format or API subscription status."}
    except httpx.RequestError as e:
        return {"error": f"Network error during X-Force API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

if __name__ == "__main__":
    print("Starting X-Force Threat Intelligence FastMCP Server...")
    mcp.run(transport="stdio")
