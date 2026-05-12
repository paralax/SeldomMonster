#!/usr/bin/env python3

import ipaddress
import logging
from typing import Any, Dict, List

import aiohttp
from mcp.server.fastmcp import FastMCP

NAME="otx-simple-mcp"

mcp = FastMCP(NAME)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(NAME)

OTX_BASE_URL="https://otx.alienvault.com/api/v1"

@mcp.tool()
async def pdns_for_hostname(hostname: str) -> List[Dict[str, Any]]:
    """
    Name: pdns_for_hostname
    Description: Returns the known DNS history for a given hostname.
    Parameters:
    hostname (required): The hostname to search for 
    """
    url = f"{OTX_BASE_URL}/indicators/hostname/{hostname}/passive_dns"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
    logger.info(f"pdns_for_hostname {hostname}: {result}")
    data = []
    for item in result['passive_dns']:
        if item['address'] == "NXDOMAIN":
            continue
        for key in ("indicator_link", "flag_url", ):
            item.pop(key)
        data.append(item)
    return data[:10]

@mcp.tool()
async def subdomains_for_domain(domain: str) -> List[Dict[str, Any]]:
    """
    Name: subdomains_for_domain
    Description: Returns the known subdomains for a given domain name.
    Parameters:
    domain (required): The domain name to search for 
    """
    url = f"{OTX_BASE_URL}/indicators/domain/{domain}/passive_dns"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
    logger.info(f"subdomains_for_domain {domain}: {result}")
    data = []
    for item in result['passive_dns']:
        if item['address'] == "NXDOMAIN" or item['asset_type'] != 'hostname':
            continue
        if item.get('hostname', []).endswith(domain):
            for key in ("indicator_link", "flag_url", ):
                item.pop(key)
            data.append(item)
    return data[:10]

@mcp.tool()
async def pdns_for_ip(ip: str) -> List[Dict[str, Any]]:
    """
    Name: pdns_for_ip
    Description: Returns the known DNS history for a given IPv4 or IPv6 address.
    Parameters:
    ip (required): The IP address to search for 
    """
    try:
        version = ipaddress.ip_address(ip).version
    except ValueError:
        raise
    url = f"{OTX_BASE_URL}/indicators/IPv{version}/{ip}/passive_dns"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
    print(f"pdns_for_ip {ip}: {type(result)} {result}")
    data = []
    for item in result['passive_dns']:
        if item['address'] == "NXDOMAIN" or item['asset_type'] != 'hostname':
            continue
        for key in ("indicator_link", "flag_url", ):
            item.pop(key)
        data.append(item)
    return data[:10]

@mcp.tool()
async def geo_for_ip(ip: str) -> Dict[str, Any]:
    """
    Name: geo_for_ip
    Description: Returns the known geolocation info for a given IP address.
    Parameters:
    ip (required): The IP address to search for 
    """
    try:
        version = ipaddress.ip_address(ip).version
    except ValueError:
        raise
    url = f"{OTX_BASE_URL}/indicators/IPv{version}/{ip}/geo"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    logger.info(f"geo_for_ip {ip}: {result}")
    return result

@mcp.tool()
async def reputation_for_ip(ip: str) -> Dict[str, Any]:
    """
    Name: reputation_for_ip
    Description: Returns the security vendor reputaion info for a given IP address.
    Parameters:
    ip (required): The IP address to search for 
    """
    try:
        version = ipaddress.ip_address(ip).version
    except ValueError:
        raise
    url = f"{OTX_BASE_URL}/indicators/IPv{version}/{ip}/reputation"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    logger.info(f"reputation_for_ip {ip}: {result}")
    return result

@mcp.tool()
async def malware_for_ip(ip: str) -> Dict[str, Any]:
    """
    Name: malware_for_ip
    Description: Returns info about the malware associated with a given IP address.
    Parameters:
    ip (required): The IP address to search for 
    """
    try:
        version = ipaddress.ip_address(ip).version
    except ValueError:
        raise
    url = f"{OTX_BASE_URL}/indicators/IPv{version}/{ip}/malware"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    logger.info(f"malware_for_ip {ip}: {result}")
    return result # .get('data', [])

@mcp.tool()
async def url_list_for_ip(ip: str) -> Dict[str, Any]:
    """
    Name: url_list_for_ip
    Description: Returns info about the malware associated with a given IP address.
    Parameters:
    ip (required): The IP address to search for 
    """
    try:
        version = ipaddress.ip_address(ip).version
    except ValueError:
        raise
    url = f"{OTX_BASE_URL}/indicators/IPv{version}/{ip}/url_list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    logger.info(f"url_list_for_ip {ip}: {result}")
    return result # .get('url_list', [])

@mcp.tool()
async def malware_for_domain(domain: str) -> Dict[str, Any]:
    """
    Name: malware_for_domain
    Description: Returns info about the malware associated with a given domain name.
    Parameters:
    ip (required): The domain name to search for 
    """
    url = f"{OTX_BASE_URL}/indicators/domain/{domain}/malware"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    logger.info(f"malware_for_domain {domain}: {result}")
    return result # .get('data', [])


@mcp.tool()
async def url_list_for_domain(domain: str) -> Dict[str, Any]:
    """
    Name: url_list_for_domain
    Description: Returns info about the URLs associated with a given domain name.
    Parameters:
    ip (required): The domain name to search for 
    """
    url = f"{OTX_BASE_URL}/indicators/domain/{domain}/url_list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    logger.info(f"url_list_for_domain {domain}: {result}")
    return result # .get('url_list', [])


@mcp.tool()
async def passive_dns_for_domain(domain: str) -> Dict[str, Any]:
    """
    Name: passive_dns_for_domain
    Description: Returns info about the hostnames associated with a given domain name.
    Parameters:
    ip (required): The domain name to search for 
    """
    url = f"{OTX_BASE_URL}/indicators/domain/{domain}/passive_dns"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    logger.info(f"passive_dns_for_domain {domain}: {result}")
    return result # .get('passive_dns', [])


@mcp.tool()
async def analysis_for_file(sample_hash: str) -> Dict[str, Any]:
    """
    Name: analysis_for_file
    Description: Returns info about the sample given a hash.
    Parameters:
    ip (required): The hash value to search for 
    """
    url = f"{OTX_BASE_URL}/indicators/file/{sample_hash}/analysis"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    logger.info(f"analysis_for_file {sample_hash}: {result}")
    return result # .get('analysis', [])


@mcp.tool()
async def get_cve(cve: str) -> List[Dict[str, Any]]:
    """
    Name: get_cve
    Description: Returns the known information for a given CVE.
    Parameters:
    cve (required): The CVE to search for 
    """    
    url = f"{OTX_BASE_URL}/indicators/cve/{cve}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
    return result

"""
TODO
https://otx.alienvault.com/api

- url URLs
- file hashes 
"""

def main() -> None:
    logger.info("Starting OTX simple MCP server")
    mcp.run(transport='stdio')        

if __name__ == "__main__":
    main()