from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport
import uvicorn
import asyncio
import os
from typing import Any, Dict, List, Optional
from slack_sdk import WebClient
from mcp.server.models import InitializationOptions
from mcp.server import Server, NotificationOptions

import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

# Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

server = Server("slack-mcp")

def get_slack_client():
    if not SLACK_BOT_TOKEN:
        raise Exception("SLACK_BOT_TOKEN not configured")
    return WebClient(token=SLACK_BOT_TOKEN)

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available Slack tools."""
    return [
        types.Tool(
            name="send_message",
            description="Send a message to a Slack channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Channel ID or name"},
                    "text": {"type": "string", "description": "Message text"},
                },
                "required": ["channel", "text"]
            }
        ),
        types.Tool(
            name="list_channels",
            description="List public channels in Slack",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of channels to return", "default": 20}
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for Slack."""
    try:
        client = get_slack_client()
        
        if name == "send_message":
            channel = arguments.get("channel")
            text = arguments.get("text")
            response = client.chat_postMessage(channel=channel, text=text)
            return [types.TextContent(type="text", text=f"Message sent successfully to {channel}. TS: {response['ts']}")]

        elif name == "list_channels":
            limit = arguments.get("limit", 20)
            result = client.conversations_list(types="public_channel", limit=limit)
            channels = result["channels"]
            output = [f"#{c['name']} ({c['id']})" for c in channels]
            return [types.TextContent(type="text", text="\n".join(output) if output else "No channels found.")]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name="slack-mcp",
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
