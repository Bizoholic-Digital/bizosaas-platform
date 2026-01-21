import os
import re

MCP_DIRS = [
    "mcp-servers/brave-search",
    "mcp-servers/filesystem",
    "mcp-servers/fluent-crm",
    "mcp-servers/google-ads",
    "mcp-servers/google-drive",
    "mcp-servers/s3-storage",
    "mcp-servers/slack"
]

SERVER_PY_TEMPLATE_TAIL = """
sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name="{server_name}",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={{}},
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
"""

IMPORTS_TO_ADD = """from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport
import uvicorn
"""

for mcp_dir in MCP_DIRS:
    mcp_dir = os.path.join("/home/alagiri/projects/bizosaas-platform", mcp_dir)
    if not os.path.exists(mcp_dir):
        print(f"Skipping {mcp_dir} (not found)")
        continue
        
    print(f"Processing {mcp_dir}...")
    
    # 1. Update requirements.txt
    req_path = os.path.join(mcp_dir, "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r") as f:
            req_content = f.read()
        if "starlette" not in req_content:
            with open(req_path, "a") as f:
                f.write("\nstarlette\nuvicorn\nsse-starlette\n")
    
    # 2. Update Dockerfile
    docker_path = os.path.join(mcp_dir, "Dockerfile")
    if os.path.exists(docker_path):
        with open(docker_path, "r") as f:
            docker_content = f.read()
        if "EXPOSE 8000" not in docker_content:
            docker_content = docker_content.replace('ENTRYPOINT ["python", "server.py"]', 'EXPOSE 8000\nENTRYPOINT ["python", "server.py"]')
            with open(docker_path, "w") as f:
                f.write(docker_content)

    # 3. Update server.py
    server_path = os.path.join(mcp_dir, "server.py")
    if os.path.exists(server_path):
        with open(server_path, "r") as f:
            content = f.read()
            
        # Parse server name
        match = re.search(r'Server\("([^"]+)"\)', content)
        server_name = match.group(1) if match else "mcp-server"
        
        if "SseServerTransport" not in content:
            # Remove stdio import if exists
            content = content.replace("from mcp.server.stdio import stdio_server", "")
            
            # Use regex to insert imports at the top
            content = IMPORTS_TO_ADD + content
            
            # Remove main function and everything after
            if "async def main():" in content:
                content = content.split("async def main():")[0]
            elif 'if __name__ == "__main__":' in content:
                content = content.split('if __name__ == "__main__":')[0]
            
            # Add new tail
            content += SERVER_PY_TEMPLATE_TAIL.format(server_name=server_name)
            
            with open(server_path, "w") as f:
                f.write(content)

print("Done!")
