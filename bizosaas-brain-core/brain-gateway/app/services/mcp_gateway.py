import httpx
import logging
import os
import importlib
from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.mcp import UserMcpInstallation, McpRegistry

logger = logging.getLogger(__name__)

class MCPGateway:
    """
    Modular MCP Gateway Layer.
    Responsible for connecting AI agents to active MCP servers.
    Handles tool discovery and execution across multiple MCP transports.
    """
    
    def __init__(self, db: Session):
        self.db = db

    async def list_tools(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Aggregates tools from all active MCP installations for a user.
        """
        installations = self.db.query(UserMcpInstallation).filter(
            UserMcpInstallation.user_id == user_id,
            UserMcpInstallation.status == "active"
        ).all()
        
        all_tools = []
        for inst in installations:
            try:
                tools = await self._fetch_tools_from_server(inst)
                # Enrich tools with MCP metadata
                for tool in tools:
                    tool["mcp_slug"] = inst.mcp.slug
                    tool["mcp_name"] = inst.mcp.name
                all_tools.extend(tools)
            except Exception as e:
                logger.error(f"Failed to fetch tools for MCP {inst.mcp.slug}: {e}")
                
        return all_tools

    async def call_tool(self, user_id: str, mcp_slug: str, tool_name: str, arguments: Dict[str, Any], source_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes a specific tool call on an MCP server.
        Automatically records the interaction in the Knowledge Graph for KAG feedback.
        """
        installation = self.db.query(UserMcpInstallation).filter(
            UserMcpInstallation.user_id == user_id,
            UserMcpInstallation.status == "active"
        ).join(McpRegistry).filter(McpRegistry.slug == mcp_slug).first()
        
        if not installation:
            raise ValueError(f"Active MCP installation for '{mcp_slug}' not found for user {user_id}")
            
        success = False
        try:
            result = await self._execute_tool_on_server(installation, tool_name, arguments)
            success = True
            return result
        except Exception as e:
            logger.error(f"Tool call failed: {e}")
            raise
        finally:
            # KAG Feedback Loop: Record the interaction
            if source_id:
                try:
                    from app.services.knowledge_graph import KnowledgeGraph
                    kg = KnowledgeGraph()
                    kg.record_interaction(self.db, source_id, mcp_slug, success=success)
                except Exception as kag_e:
                    logger.warning(f"Failed to record KAG interaction: {kag_e}")

    async def _fetch_tools_from_server(self, installation: UserMcpInstallation) -> List[Dict[str, Any]]:
        """
        Fetches the list of tools from the MCP server's endpoint.
        """
        endpoint = self._get_mcp_endpoint(installation)
        if not endpoint:
            return []

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                # MCP standard usually has a /tools or similar list endpoint
                # For simplified proxying, we assume /tools/list 
                # or following the SSE/POST pattern.
                response = await client.get(f"{endpoint}/tools")
                if response.status_code == 200:
                    data = response.json()
                    return data.get("tools", [])
                return []
            except Exception as e:
                logger.warning(f"Could not reach MCP {installation.mcp.slug} at {endpoint}: {e}")
                return []

    async def _execute_tool_on_server(self, installation: UserMcpInstallation, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a tool execution request to the MCP server.
        """
        endpoint = self._get_mcp_endpoint(installation)
        if not endpoint:
            raise ValueError(f"No endpoint configured for MCP {installation.mcp.slug}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{endpoint}/tools/call",
                json={
                    "name": tool_name,
                    "arguments": arguments
                }
            )
            response.raise_for_status()
            return response.json()

    def _get_mcp_endpoint(self, installation: UserMcpInstallation) -> Optional[str]:
        """
        Determines the endpoint URL for a given MCP installation.
        """
        # 1. Check user-specific installation config override
        config = installation.config or {}
        endpoint = config.get("api_endpoint") or config.get("url")
        
        if endpoint:
            return endpoint
            
        # 2. Check global registry default config
        registry_config = installation.mcp.mcp_config or {}
        endpoint = registry_config.get("url") or registry_config.get("api_endpoint")
        
        if endpoint:
            return endpoint
            
        # 3. Fallback to service discovery pattern (e.g. docker-compose service name)
        # This assumes the containers are reachable within the same network
        return f"http://{installation.mcp.slug}:8000"
