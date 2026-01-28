"""
Knowledge Graph Builder
Constructs and maintains a graph database of tool relationships and dependencies
for advanced KAG (Knowledge-Augmented Generation) discovery.
"""

import logging
from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass
from collections import defaultdict
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@dataclass
class ToolNode:
    """Represents a tool/MCP in the knowledge graph."""
    id: str
    name: str
    category: str
    capabilities: List[str]
    connected_tenants: Set[str]
    
@dataclass
class ToolRelationship:
    """Represents a relationship between two tools."""
    source_tool: str
    target_tool: str
    relationship_type: str  # 'feeds_into', 'depends_on', 'complements', 'conflicts_with'
    strength: float  # 0.0 to 1.0
    evidence_count: int


class KnowledgeGraph:
    """
    Graph database of tool relationships and dependencies.
    Used for advanced pattern detection and integration gap analysis.
    """
    
    def __init__(self):
        self.nodes: Dict[str, ToolNode] = {}
        self.edges: List[ToolRelationship] = []
        self.adjacency: Dict[str, List[str]] = defaultdict(list)
    
    def add_node(self, node: ToolNode):
        """Add a tool node to the graph."""
        self.nodes[node.id] = node
        logger.debug(f"Added node: {node.name}")
    
    def add_edge(self, edge: ToolRelationship):
        """Add a relationship edge to the graph."""
        self.edges.append(edge)
        self.adjacency[edge.source_tool].append(edge.target_tool)
        logger.debug(f"Added edge: {edge.source_tool} -> {edge.target_tool} ({edge.relationship_type})")
    
    def find_integration_gaps(self) -> List[Dict[str, Any]]:
        """
        Identify missing integrations that would create value.
        Uses graph traversal to find disconnected but complementary tools.
        """
        gaps = []
        
        # Find tools that are commonly used together but not connected
        for node_id, node in self.nodes.items():
            # Get tools used by the same tenants
            related_tools = self._find_cooccurring_tools(node)
            
            # Check which ones aren't connected
            connected = set(self.adjacency.get(node_id, []))
            
            for related_tool in related_tools:
                if related_tool.id not in connected and related_tool.id != node_id:
                    # Found a gap!
                    gaps.append({
                        "source": node.name,
                        "target": related_tool.name,
                        "reason": "frequently_used_together",
                        "tenant_overlap": len(node.connected_tenants & related_tool.connected_tenants),
                        "suggested_workflow": self._suggest_integration_workflow(node, related_tool)
                    })
        
        return gaps
    
    def find_workflow_chains(self, start_tool: str, max_depth: int = 3) -> List[List[str]]:
        """
        Find potential workflow chains starting from a given tool.
        Uses DFS to discover multi-step automation opportunities.
        """
        chains = []
        
        def dfs(current: str, path: List[str], depth: int):
            if depth >= max_depth:
                if len(path) > 1:
                    chains.append(path.copy())
                return
            
            for neighbor in self.adjacency.get(current, []):
                if neighbor not in path:  # Avoid cycles
                    path.append(neighbor)
                    dfs(neighbor, path, depth + 1)
                    path.pop()
        
        dfs(start_tool, [start_tool], 0)
        return chains
    
    def detect_redundant_patterns(self) -> List[Dict[str, Any]]:
        """
        Identify patterns where users are manually doing what could be automated.
        """
        redundancies = []
        
        # Look for manual data transfer patterns
        # Example: If users have both Shopify and Mailchimp but no automation,
        # they're likely manually syncing customer data
        
        for node_id, node in self.nodes.items():
            if node.category == "ecommerce":
                # Check if they have marketing tools but no automation
                marketing_tools = [
                    n for n in self.nodes.values()
                    if n.category == "marketing" and 
                    len(n.connected_tenants & node.connected_tenants) > 0
                ]
                
                for marketing_tool in marketing_tools:
                    # Check if there's an automation edge
                    has_automation = any(
                        e.source_tool == node_id and e.target_tool == marketing_tool.id
                        for e in self.edges
                    )
                    
                    if not has_automation:
                        redundancies.append({
                            "source": node.name,
                            "target": marketing_tool.name,
                            "pattern": "manual_data_sync",
                            "affected_tenants": len(node.connected_tenants & marketing_tool.connected_tenants),
                            "suggested_automation": "customer_data_sync_workflow"
                        })
        
        return redundancies
    
    def calculate_tool_centrality(self) -> Dict[str, float]:
        """
        Calculate centrality scores for each tool.
        High centrality = critical integration point.
        """
        centrality = {}
        
        for node_id in self.nodes:
            # Simple degree centrality
            in_degree = sum(1 for e in self.edges if e.target_tool == node_id)
            out_degree = len(self.adjacency.get(node_id, []))
            centrality[node_id] = (in_degree + out_degree) / max(len(self.nodes) - 1, 1)
        
        return centrality
    
    def _find_cooccurring_tools(self, node: ToolNode) -> List[ToolNode]:
        """Find tools that are used by the same tenants."""
        cooccurring = []
        
        for other_node in self.nodes.values():
            if other_node.id != node.id:
                overlap = len(node.connected_tenants & other_node.connected_tenants)
                if overlap > 0:
                    cooccurring.append(other_node)
        
        return cooccurring
    
    def _suggest_integration_workflow(self, source: ToolNode, target: ToolNode) -> str:
        """Suggest a workflow name for integrating two tools."""
        return f"{source.name} to {target.name} Auto-Sync"


class KnowledgeGraphBuilder:
    """
    Builds and maintains the knowledge graph from platform data.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.graph = KnowledgeGraph()
    
    async def build_graph(self) -> KnowledgeGraph:
        """
        Build the knowledge graph from current platform state.
        """
        logger.info("Building knowledge graph...")
        
        # Load all MCPs and their connections
        from app.models.mcp import Mcp
        from app.models.onboarding import OnboardingSession
        
        mcps = self.db.query(Mcp).all()
        
        # Create nodes for each MCP
        for mcp in mcps:
            # Find tenants using this MCP
            sessions = self.db.query(OnboardingSession).filter(
                OnboardingSession.tools['selectedMcps'].astext.contains(mcp.slug)
            ).all()
            
            tenant_ids = {s.tenant_id for s in sessions if s.tenant_id}
            
            node = ToolNode(
                id=mcp.slug,
                name=mcp.name,
                category=mcp.category_id or "general",
                capabilities=mcp.capabilities or [],
                connected_tenants=tenant_ids
            )
            self.graph.add_node(node)
        
        # Infer relationships from co-usage patterns
        await self._infer_relationships()
        
        logger.info(f"Knowledge graph built: {len(self.graph.nodes)} nodes, {len(self.graph.edges)} edges")
        return self.graph
    
    async def _infer_relationships(self):
        """
        Infer tool relationships from usage patterns.
        """
        # For each pair of tools used by the same tenant, create a relationship
        for node_id, node in self.graph.nodes.items():
            for other_id, other_node in self.graph.nodes.items():
                if node_id >= other_id:  # Avoid duplicates
                    continue
                
                overlap = len(node.connected_tenants & other_node.connected_tenants)
                if overlap > 0:
                    # Determine relationship type based on categories
                    rel_type = self._determine_relationship_type(node, other_node)
                    strength = overlap / max(len(node.connected_tenants), len(other_node.connected_tenants))
                    
                    edge = ToolRelationship(
                        source_tool=node_id,
                        target_tool=other_id,
                        relationship_type=rel_type,
                        strength=strength,
                        evidence_count=overlap
                    )
                    self.graph.add_edge(edge)
    
    def _determine_relationship_type(self, node1: ToolNode, node2: ToolNode) -> str:
        """
        Determine the type of relationship between two tools.
        """
        # Simple heuristics based on categories
        if node1.category == "ecommerce" and node2.category == "marketing":
            return "feeds_into"
        elif node1.category == "analytics" and node2.category in ["marketing", "ecommerce"]:
            return "monitors"
        elif node1.category == node2.category:
            return "complements"
        else:
            return "related"


async def build_platform_knowledge_graph(db: Session) -> KnowledgeGraph:
    """
    Helper function to build the knowledge graph.
    """
    builder = KnowledgeGraphBuilder(db)
    return await builder.build_graph()
