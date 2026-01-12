import asyncio
import base64
import json
import os
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment variables
WP_URL = os.getenv("FLUENTCRM_WP_URL")
WP_USER = os.getenv("FLUENTCRM_WP_USER")
WP_APP_PASSWORD = os.getenv("FLUENTCRM_WP_APP_PASSWORD")

server = Server("fluent-crm")

def get_auth_header() -> Dict[str, str]:
    if not WP_USER or not WP_APP_PASSWORD:
        return {}
    credentials = f"{WP_USER}:{WP_APP_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {token}"}

def get_api_url(path: str) -> str:
    base = WP_URL.rstrip("/")
    return f"{base}/wp-json/fluent-crm/v2/{path.lstrip('/')}"

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available FluentCRM tools."""
    return [
        types.Tool(
            name="list_contacts",
            description="List subscribers from FluentCRM",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of contacts to return", "default": 20},
                    "page": {"type": "integer", "description": "Page number", "default": 1}
                }
            }
        ),
        types.Tool(
            name="search_contact",
            description="Search for a contact by email",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Email address to search for"}
                },
                "required": ["email"]
            }
        ),
        types.Tool(
            name="create_contact",
            description="Add a new contact to FluentCRM",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "status": {"type": "string", "enum": ["subscribed", "pending", "unsubscribed"], "default": "subscribed"},
                    "tags": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["email"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for FluentCRM."""
    if not WP_URL:
        return [types.TextContent(type="text", text="Error: FLUENTCRM_WP_URL not configured")]

    async with httpx.AsyncClient() as client:
        try:
            if name == "list_contacts":
                limit = arguments.get("limit", 20)
                page = arguments.get("page", 1)
                response = await client.get(
                    get_api_url("contacts"),
                    headers=get_auth_header(),
                    params={"per_page": limit, "page": page}
                )
                response.raise_for_status()
                return [types.TextContent(type="text", text=json.dumps(response.json(), indent=2))]

            elif name == "search_contact":
                email = arguments.get("email")
                response = await client.get(
                    get_api_url("contacts"),
                    headers=get_auth_header(),
                    params={"search": email}
                )
                response.raise_for_status()
                return [types.TextContent(type="text", text=json.dumps(response.json(), indent=2))]

            elif name == "create_contact":
                payload = {
                    "email": arguments.get("email"),
                    "first_name": arguments.get("first_name", ""),
                    "last_name": arguments.get("last_name", ""),
                    "status": arguments.get("status", "subscribed"),
                    "tags": arguments.get("tags", [])
                }
                response = await client.post(
                    get_api_url("contacts"),
                    headers=get_auth_header(),
                    json=payload
                )
                response.raise_for_status()
                return [types.TextContent(type="text", text=f"Contact created successfully: {json.dumps(response.json(), indent=2)}")]

            else:
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

        except httpx.HTTPStatusError as e:
            return [types.TextContent(type="text", text=f"API Error: {e.response.text}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Unexpected Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fluent-crm",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
