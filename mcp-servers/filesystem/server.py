from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport
import uvicorn
import asyncio
import os
import shutil
from typing import Any, Dict, List, Optional

from mcp.server.models import InitializationOptions
from mcp.server import Server, NotificationOptions

import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

# The directory the server is allowed to access
ALLOWED_DIRECTORY = os.getenv("FILESYSTEM_ROOT", "/data")

server = Server("filesystem")

def is_safe_path(path: str) -> bool:
    full_path = os.path.abspath(os.path.join(ALLOWED_DIRECTORY, path))
    return full_path.startswith(os.path.abspath(ALLOWED_DIRECTORY))

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available Filesystem tools."""
    return [
        types.Tool(
            name="list_directory",
            description="List contents of a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to list", "default": "."}
                }
            }
        ),
        types.Tool(
            name="read_file",
            description="Read the contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to file"}
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to file"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for Filesystem."""
    path = arguments.get("path", ".")
    
    if not is_safe_path(path):
        return [types.TextContent(type="text", text="Error: Path outside of allowed directory")]

    full_path = os.path.join(ALLOWED_DIRECTORY, path)

    try:
        if name == "list_directory":
            items = os.listdir(full_path)
            return [types.TextContent(type="text", text="\n".join(items))]

        elif name == "read_file":
            with open(full_path, "r") as f:
                content = f.read()
            return [types.TextContent(type="text", text=content)]

        elif name == "write_file":
            content = arguments.get("content", "")
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            return [types.TextContent(type="text", text=f"File written successfully: {path}")]

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
                server_name="filesystem",
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
