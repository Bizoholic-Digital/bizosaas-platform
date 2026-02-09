from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport
import uvicorn
import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

from mcp.server.models import InitializationOptions
from mcp.server import Server, NotificationOptions

import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

# Configuration
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SCOPES = ['https://www.googleapis.com/auth/drive']

server = Server("google-drive")

def get_drive_service():
    if not SERVICE_ACCOUNT_JSON:
        raise Exception("GOOGLE_SERVICE_ACCOUNT_JSON not configured")
    
    info = json.loads(SERVICE_ACCOUNT_JSON)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available Google Drive tools."""
    return [
        types.Tool(
            name="list_files",
            description="List files in Google Drive",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query (Drive API format)", "default": ""},
                    "pageSize": {"type": "integer", "description": "Number of files to return", "default": 10}
                }
            }
        ),
        types.Tool(
            name="upload_file",
            description="Upload a file to Google Drive",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the file"},
                    "content": {"type": "string", "description": "Text content of the file"},
                    "mimeType": {"type": "string", "description": "MIME type", "default": "text/plain"},
                    "parentId": {"type": "string", "description": "Folder ID to upload to", "default": None}
                },
                "required": ["name", "content"]
            }
        ),
        types.Tool(
            name="get_file_content",
            description="Get the content of a file from Google Drive",
            inputSchema={
                "type": "object",
                "properties": {
                    "fileId": {"type": "string", "description": "The ID of the file"}
                },
                "required": ["fileId"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for Google Drive."""
    try:
        service = get_drive_service()
        
        if name == "list_files":
            q = arguments.get("query", "")
            pageSize = arguments.get("pageSize", 10)
            results = service.files().list(
                q=q, pageSize=pageSize, fields="nextPageToken, files(id, name, mimeType)"
            ).execute()
            items = results.get('files', [])
            
            output = []
            for item in items:
                output.append(f"{item['name']} ({item['id']}) [{item['mimeType']}]")
            
            return [types.TextContent(type="text", text="\n".join(output) if output else "No files found.")]

        elif name == "upload_file":
            file_metadata = {'name': arguments.get("name")}
            if arguments.get("parentId"):
                file_metadata['parents'] = [arguments.get("parentId")]
                
            content = arguments.get("content", "")
            media = MediaFileUpload(
                io.BytesIO(content.encode()),
                mimetype=arguments.get("mimeType", "text/plain"),
                resumable=True
            )
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return [types.TextContent(type="text", text=f"File uploaded successfully. ID: {file.get('id')}")]

        elif name == "get_file_content":
            file_id = arguments.get("fileId")
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            return [types.TextContent(type="text", text=fh.getvalue().decode('utf-8'))]

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
                server_name="google-drive",
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
