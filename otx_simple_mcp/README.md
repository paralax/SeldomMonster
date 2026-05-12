# Simple OTX MCP Server

nothing fancy just naked API calls, returns JSON 

# Configuration

"Simple OTX": {
      "command": "/Library/Frameworks/Python.framework/Versions/3.13/bin/uv",
      "args": [
        "--directory",
        "/Users/josenazario/code/mcp-cti/mcp_simple_mcp",
        "run",
        "python",
        "server.py"
      ],
      "env": {
        "OTX_API_KEY": "d99fd502426fdd9a71a6536ec12ee91c9506cdd8bc3072c16dbc8a1796f1bdf1",
        "SSL_CERT_FILE": "/private/etc/ssl/cert.pem"
      }
    },