import os

import httpx
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

mcp = FastMCP(
    name="Malpedia",
    instructions="The primary goal of Malpedia is to provide a resource for rapid identification and actionable context when investigating malware. Openness to curated contributions shall ensure an accountable level of quality in order to foster meaningful and reproducible research.",
    dependencies=["httpx"]
)

API_KEY = os.getenv("MALPEDIA_API_KEY")

BASE_URL = "https://malpedia.caad.fkie.fraunhofer.de/api/"
MALPEDIA_CLIENT = httpx.AsyncClient(base_url=BASE_URL, headers={'Authorization': f'apitoken {API_KEY}'}, timeout=10.0)

@mcp.tool()
async def find_actor(actor: str) -> Dict[str, Any]:
    """
    Name: find_actor
    Description: Provide a list of all actor names and associated synonyms where a part of the name is matched.
    Parameters:
    actor - The actor name to query for
    """
    # test actor: "Gh0stTimes"
    endpoint = f"/find/actor/{actor}"
    try:
        response = await MALPEDIA_CLIENT.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve actor info. Check the input format."}
    except httpx.RequestError as e:
        return {"error": f"Network error during Malpedia API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}  

@mcp.tool()
async def find_family(family: str) -> Dict[str, Any]:
    """
    Name: find_family
    Description: Provide a list of all family names and associated synonyms where a part of the name is matched.
    Parameters:
    family - The family name to query for
    """
    # test txid: "Gh0stRAT"
    endpoint = f"/find/family/{family}"
    try:
        response = await MALPEDIA_CLIENT.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve family info. Check the input format."}
    except httpx.RequestError as e:
        return {"error": f"Network error during Malpedia API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}  

@mcp.tool()
async def get_actor(actor_id: str) -> Dict[str, Any]:
    """
    Name: get_actor
    Description: Retrieve detailed information about a specific actor using its Malpedia ID.
    Parameters:
    actor_id - The Malpedia ID of the actor to retrieve.
    """
    endpoint = f"/get/actor/{actor_id}"
    try:
        response = await MALPEDIA_CLIENT.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve actor info. Check the input format."}
    except httpx.RequestError as e:
        return {"error": f"Network error during Malpedia API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

@mcp.tool()
async def get_family(family_id: str) -> Dict[str, Any]:
    """
    Name: get_family
    Description: Retrieve detailed information about a specific family using its Malpedia ID.
    Parameters:
    family_id - The Malpedia ID of the family to retrieve.
    """
    endpoint = f"/get/family/{family_id}"
    try:
        response = await MALPEDIA_CLIENT.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve family info. Check the input format."}
    except httpx.RequestError as e:
        return {"error": f"Network error during Malpedia API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}    

@mcp.tool()
async def get_yara_for_family(family_id: str) -> Dict[str, Any]:
    """
    Name: get_yara_for_family
    Description: Retrieve YARA rules for a specific family using its Malpedia ID.
    Parameters:
    family_id - The Malpedia ID of the family to retrieve YARA rules for.
    """
    endpoint = f"/get/yara/{family_id}"
    try:
        response = await MALPEDIA_CLIENT.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve YARA rules. Check the input format."}
    except httpx.RequestError as e:
        return {"error": f"Network error during Malpedia API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

if __name__ == "__main__":
    print("Starting Malpedia MCP Server...")
    mcp.run(transport="stdio")