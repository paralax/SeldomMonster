import httpx
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

# 1. Initialize FastMCP Server
# FastMCP uses the docstrings and type hints to generate the tool's schema for the LLM.
mcp = FastMCP(
    name="Blockchain",
    instructions="A cryptocurrency blockchain server for looking up wallet IDs by the blockchain.com API.",
    dependencies=["httpx"]
)

BASE_URL = "https://blockchain.info"
BLOCKCHAIN_CLIENT = httpx.AsyncClient(base_url=BASE_URL, timeout=10.0)

@mcp.tool()
async def get_wallet_info(address: str) -> Dict[str, Any]:
    """
    Name: get_wallet_info
    Description: Fetches information about a cryptocurrency wallet
    Parameters:
    address - The wallet address, which can be base58 or hash160
    """
    # test address: 1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F
    endpoint = f"/rawaddr/{address}"
    try:
        response = await BLOCKCHAIN_CLIENT.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve wallet info. Check the input format."}
    except httpx.RequestError as e:
        return {"error": f"Network error during blockchain API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}  

@mcp.tool()
async def get_transaction_info(txid: str) -> Dict[str, Any]:
    """
    Name: get_transaction_info
    Description: Fetches information about a transaction
    Parameters:
    txid - The transaction ID
    """
    # test txid: b6f6991d03df0e2e04dafffcd6bc418aac66049e2cd74b80f14ac86db1e3f0da
    endpoint = f"/rawtx/{txid}"
    try:
        response = await BLOCKCHAIN_CLIENT.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code} - Could not retrieve transcation info. Check the input format."}
    except httpx.RequestError as e:
        return {"error": f"Network error during blockchain API call: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}  
    
if __name__ == "__main__":
    print("Starting Blockchain MCP Server...")
    mcp.run(transport="stdio")