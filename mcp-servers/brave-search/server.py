import asyncio
import json
import os
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.models import InitializationOptions
from mcp.server import Notification, Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment variables
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

server = Server("brave-search")

def get_headers() -> Dict[str, str]:
    return {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY or ""
    }

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available Brave Search tools."""
    return [
        types.Tool(
            name="search",
            description="Search the web using Brave Search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "count": {"type": "integer", "description": "Number of results (1-20)", "default": 5}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="local_search",
            description="Search for local places and businesses using Brave Search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "count": {"type": "integer", "description": "Number of results", "default": 5}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for Brave Search."""
    if not BRAVE_API_KEY:
        return [types.TextContent(type="text", text="Error: BRAVE_API_KEY not configured")]

    async with httpx.AsyncClient() as client:
        try:
            if name == "search":
                query = arguments.get("query")
                count = arguments.get("count", 5)
                response = await client.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers=get_headers(),
                    params={"q": query, "count": count}
                )
                response.raise_for_status()
                data = response.json()
                
                results = []
                for result in data.get("web", {}).get("results", []):
                    results.append(f"Title: {result.get('title')}\nURL: {result.get('url')}\nDescription: {result.get('description')}\n")
                
                return [types.TextContent(type="text", text="\n".join(results) if results else "No results found.")]

            elif name == "local_search":
                query = arguments.get("query")
                count = arguments.get("count", 5)
                response = await client.get(
                    "https://api.search.brave.com/res/v1/local/search",
                    headers=get_headers(),
                    params={"q": query, "count": count}
                )
                response.raise_for_status()
                return [types.TextContent(type="text", text=json.dumps(response.json(), indent=2))]

            else:
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

        except httpx.HTTPStatusError as e:
            return [types.TextContent(type="text", text=f"API Error: {e.response.status_code} - {e.response.text}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Unexpected Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="brave-search",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=Notification,
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
