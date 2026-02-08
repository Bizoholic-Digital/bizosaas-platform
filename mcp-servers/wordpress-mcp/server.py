import os
import httpx
import logging
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.sse import SseServerTransport
import mcp.types as types
from starlette.applications import Starlette
from starlette.routing import Route, Mount
import uvicorn
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wordpress-mcp")

load_dotenv()

# Configuration
BRAIN_GATEWAY_URL = os.getenv("BRAIN_GATEWAY_URL", "http://brain-gateway:8000")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY") # For service-to-service auth

server = Server("wordpress-mcp")

async def call_brain_gateway(method: str, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None):
    """Utility to call Brain Gateway API"""
    headers = {
        "Content-Type": "application/json",
    }
    if INTERNAL_API_KEY:
        headers["X-Internal-API-Key"] = INTERNAL_API_KEY
    
    # In a real multi-tenant scenario, we'd need to pass the tenant context.
    # For now, we assume the gateway identifies the tenant from the context or we're in default dev mode.
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{BRAIN_GATEWAY_URL.rstrip('/')}/api/cms/{endpoint.lstrip('/')}"
        logger.info(f"Calling Brain Gateway: {method} {url}")
        
        try:
            response = await client.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Brain Gateway error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Gateway Error: {e.response.text}")
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            raise Exception(f"Connection failed: {str(e)}")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available WordPress tools."""
    return [
        # --- Content: Pages ---
        types.Tool(
            name="list_pages",
            description="List all pages from WordPress",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="create_page",
            description="Create a new WordPress page",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "slug": {"type": "string"},
                    "content": {"type": "string"},
                    "status": {"type": "string", "enum": ["draft", "publish", "private"], "default": "draft"}
                },
                "required": ["title", "slug"]
            }
        ),
        types.Tool(
            name="update_page",
            description="Update an existing WordPress page",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Page ID"},
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "status": {"type": "string", "enum": ["draft", "publish", "private"]}
                },
                "required": ["id"]
            }
        ),
        types.Tool(
            name="delete_page",
            description="Delete a WordPress page",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"]
            }
        ),

        # --- Content: Posts ---
        types.Tool(
            name="list_posts",
            description="List all blog posts from WordPress",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="create_post",
            description="Create a new WordPress blog post",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "slug": {"type": "string"},
                    "content": {"type": "string"},
                    "excerpt": {"type": "string"},
                    "category": {"type": "string"},
                    "status": {"type": "string", "enum": ["draft", "publish", "private"], "default": "draft"}
                },
                "required": ["title", "slug"]
            }
        ),
        types.Tool(
            name="update_post",
            description="Update an existing WordPress blog post",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Post ID"},
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "status": {"type": "string", "enum": ["draft", "publish", "private"]}
                },
                "required": ["id"]
            }
        ),
        types.Tool(
            name="delete_post",
            description="Delete a WordPress blog post",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"]
            }
        ),

        # --- Media ---
        types.Tool(
            name="list_media",
            description="List all media files from WordPress",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="delete_media",
            description="Delete a media item from WordPress",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"]
            }
        ),

        # --- Plugins ---
        types.Tool(
            name="list_plugins",
            description="List all installed WordPress plugins",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="activate_plugin",
            description="Activate a WordPress plugin",
            inputSchema={
                "type": "object",
                "properties": {"slug": {"type": "string", "description": "Plugin slug"}},
                "required": ["slug"]
            }
        ),
        types.Tool(
            name="deactivate_plugin",
            description="Deactivate a WordPress plugin",
            inputSchema={
                "type": "object",
                "properties": {"slug": {"type": "string", "description": "Plugin slug"}},
                "required": ["slug"]
            }
        ),

        # --- Categories ---
        types.Tool(
            name="list_categories",
            description="List all WordPress categories",
            inputSchema={"type": "object", "properties": {}}
        ),

        # --- Meta Tools ---
        types.Tool(
            name="get_stats",
            description="Get WordPress site statistics (page count, post count, media count)",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_status",
            description="Check connectivity status to WordPress",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent]:
    """Handle tool execution by proxying to Brain Gateway."""
    try:
        if name == "list_pages":
            result = await call_brain_gateway("GET", "/pages")
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "create_page":
            result = await call_brain_gateway("POST", "/pages", json_data=arguments)
            return [types.TextContent(type="text", text=f"Page created: {result.get('id')} - {result.get('title')}")]

        elif name == "update_page":
            page_id = arguments.get("id")
            result = await call_brain_gateway("PUT", f"/pages/{page_id}", json_data=arguments)
            return [types.TextContent(type="text", text=f"Page updated: {page_id}")]

        elif name == "delete_page":
            page_id = arguments.get("id")
            await call_brain_gateway("DELETE", f"/pages/{page_id}")
            return [types.TextContent(type="text", text=f"Page deleted: {page_id}")]

        elif name == "list_posts":
            result = await call_brain_gateway("GET", "/posts")
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "create_post":
            result = await call_brain_gateway("POST", "/posts", json_data=arguments)
            return [types.TextContent(type="text", text=f"Post created: {result.get('id')} - {result.get('title')}")]

        elif name == "update_post":
            post_id = arguments.get("id")
            result = await call_brain_gateway("PUT", f"/posts/{post_id}", json_data=arguments)
            return [types.TextContent(type="text", text=f"Post updated: {post_id}")]

        elif name == "delete_post":
            post_id = arguments.get("id")
            await call_brain_gateway("DELETE", f"/posts/{post_id}")
            return [types.TextContent(type="text", text=f"Post deleted: {post_id}")]

        elif name == "list_media":
            result = await call_brain_gateway("GET", "/media")
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "delete_media":
            media_id = arguments.get("id")
            await call_brain_gateway("DELETE", f"/media/{media_id}")
            return [types.TextContent(type="text", text=f"Media deleted: {media_id}")]

        elif name == "list_plugins":
            result = await call_brain_gateway("GET", "/plugins")
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "activate_plugin":
            slug = arguments.get("slug")
            await call_brain_gateway("POST", f"/plugins/{slug}/activate")
            return [types.TextContent(type="text", text=f"Plugin activated: {slug}")]

        elif name == "deactivate_plugin":
            slug = arguments.get("slug")
            await call_brain_gateway("POST", f"/plugins/{slug}/deactivate")
            return [types.TextContent(type="text", text=f"Plugin deactivated: {slug}")]

        elif name == "list_categories":
            result = await call_brain_gateway("GET", "/categories")
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_stats":
            result = await call_brain_gateway("GET", "/stats")
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_status":
            result = await call_brain_gateway("GET", "/status")
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error executing {name}: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

# SSE Transport Setup
sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name="wordpress-mcp",
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
