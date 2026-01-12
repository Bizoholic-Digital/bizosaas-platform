import asyncio
import os
from typing import Any, Dict, List, Optional
import boto3
from mcp.server.models import InitializationOptions
from mcp.server import Notification, Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

server = Server("s3-storage-mcp")

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY")
    )

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available S3 tools."""
    return [
        types.Tool(
            name="list_buckets",
            description="List all buckets",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="list_objects",
            description="List objects in a bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "prefix": {"type": "string", "default": ""}
                },
                "required": ["bucket"]
            }
        ),
        types.Tool(
            name="upload_file",
            description="Upload a file to S3",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "file_path": {"type": "string"},
                    "object_name": {"type": "string"}
                },
                "required": ["bucket", "file_path", "object_name"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for S3."""
    try:
        s3 = get_s3_client()
        if name == "list_buckets":
            response = s3.list_buckets()
            buckets = [b['Name'] for b in response.get('Buckets', [])]
            return [types.TextContent(type="text", text=f"Buckets: {', '.join(buckets)}")]
        # ... Other tools ...
        return [types.TextContent(type="text", text=f"Tool {name} called but integration is partial.")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="s3-storage-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=Notification,
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
