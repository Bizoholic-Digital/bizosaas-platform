from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport
import uvicorn
import asyncio
import os
from typing import Any, Dict, List, Optional
from mcp.server.models import InitializationOptions
from mcp.server import Server, NotificationOptions

import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

server = Server("google-ads-mcp")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available Google Ads tools."""
    return [
        types.Tool(
            name="get_campaign_stats",
            description="Get performance statistics for Google Ads campaigns",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Google Ads Customer ID"},
                    "days": {"type": "integer", "description": "Number of days of data", "default": 7}
                },
                "required": ["customer_id"]
            }
        ),
        types.Tool(
            name="list_campaigns",
            description="List campaigns in a Google Ads account",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Google Ads Customer ID"}
                },
                "required": ["customer_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for Google Ads."""
    # Implementation placeholder for Google Ads API interaction
    return [types.TextContent(type="text", text=f"Tool {name} called but integration is in development.")]


sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name="google-ads-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

routes = [
    Route("/sse", endpoint=handle_sse),
    Mount("/messages", app=sse.handle_post_message),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
