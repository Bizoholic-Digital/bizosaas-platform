from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport
import uvicorn
import asyncio
import os
import httpx
from typing import Any, Dict, List, Optional
from mcp.server.models import InitializationOptions
from mcp.server import Server, NotificationOptions
import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

# Configuration
MEESHO_API_KEY = os.getenv("MEESHO_API_KEY")
MEESHO_BASE_URL = "https://ext.meesho.com/api/v1"

server = Server("meesho-mcp")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available Meesho tools."""
    return [
        types.Tool(
            name="list_orders",
            description="List recent orders from Meesho Supplier Panel",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filter by status (e.g., 'pending', 'shipped')"},
                }
            }
        ),
        types.Tool(
            name="publish_listing",
            description="Publish a product listing to Meesho with AI-optimized content",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Optimized product title"},
                    "description": {"type": "string", "description": "Product description"},
                    "price": {"type": "integer", "description": "Selling price in INR"},
                    "sku": {"type": "string", "description": "Original Shopify SKU"},
                    "category_id": {"type": "string", "description": "Meesho Category ID"}
                },
                "required": ["title", "price", "category_id"]
            }
        ),
        types.Tool(
            name="update_inventory",
            description="Update stock levels on Meesho",
            inputSchema={
                "type": "object",
                "properties": {
                    "sku": {"type": "string", "description": "Product SKU"},
                    "quantity": {"type": "integer", "description": "New stock quantity"}
                },
                "required": ["sku", "quantity"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for Meesho."""
    try:
        if name == "list_orders":
            # Mocking Meesho API call
            return [types.TextContent(type="text", text="Fetched 2 pending orders from Meesho: [M10293, M10294]")]

        elif name == "publish_listing":
            title = arguments.get("title")
            price = arguments.get("price")
            # In actual implementation: send POST to MEESHO_BASE_URL/products
            return [types.TextContent(type="text", text=f"Successfully queued listing for '{title}' at ₹{price} on Meesho. Status: Under Review")]

        elif name == "update_inventory":
            sku = arguments.get("sku")
            qty = arguments.get("quantity")
            return [types.TextContent(type="text", text=f"Updated Meesho stock for {sku} to {qty} units.")]

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
                server_name="meesho-mcp",
                server_version="1.0.0",
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
