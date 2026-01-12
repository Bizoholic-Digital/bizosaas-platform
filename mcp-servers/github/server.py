import asyncio
import os
from typing import Any, Dict, List, Optional
from github import Github
from mcp.server.models import InitializationOptions
from mcp.server import Notification, Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from dotenv import load_dotenv

load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

server = Server("github-mcp")

def get_github_client():
    if not GITHUB_TOKEN:
        raise Exception("GITHUB_TOKEN not configured")
    return Github(GITHUB_TOKEN)

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available GitHub tools."""
    return [
        types.Tool(
            name="search_repositories",
            description="Search for repositories on GitHub",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="list_issues",
            description="List issues in a repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_name": {"type": "string", "description": "Full repository name (e.g., owner/repo)"},
                    "state": {"type": "string", "description": "Issue state (open, closed, all)", "default": "open"}
                },
                "required": ["repo_name"]
            }
        ),
        types.Tool(
            name="create_issue",
            description="Create a new issue in a repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_name": {"type": "string", "description": "Full repository name"},
                    "title": {"type": "string", "description": "Issue title"},
                    "body": {"type": "string", "description": "Issue body"},
                },
                "required": ["repo_name", "title", "body"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for GitHub."""
    try:
        g = get_github_client()
        
        if name == "search_repositories":
            query = arguments.get("query")
            repos = g.search_repositories(query)
            output = [f"{repo.full_name}: {repo.description}" for repo in repos[:10]]
            return [types.TextContent(type="text", text="\n".join(output) if output else "No repositories found.")]

        elif name == "list_issues":
            repo_name = arguments.get("repo_name")
            state = arguments.get("state", "open")
            repo = g.get_repo(repo_name)
            issues = repo.get_issues(state=state)
            output = [f"#{issue.number} {issue.title} ({issue.state})" for issue in issues[:10]]
            return [types.TextContent(type="text", text="\n".join(output) if output else "No issues found.")]

        elif name == "create_issue":
            repo_name = arguments.get("repo_name")
            title = arguments.get("title")
            body = arguments.get("body")
            repo = g.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body)
            return [types.TextContent(type="text", text=f"Issue created successfully: {issue.html_url}")]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="github-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=Notification,
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
