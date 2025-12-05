"""
Real-time Workflow Visualization Service
Handles workflow state streaming, Mermaid.js diagram generation, and performance metrics
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set, Optional, Any
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from database import get_db_connection

logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class WorkflowNode:
    """Represents a workflow node/agent"""
    id: str
    name: str
    type: str  # agent, task, decision, etc.
    status: AgentStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    input_data: Dict[str, Any] = None
    output_data: Dict[str, Any] = None
    error: Optional[str] = None
    metrics: Dict[str, float] = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "input_data": self.input_data or {},
            "output_data": self.output_data or {},
            "error": self.error,
            "metrics": self.metrics or {}
        }

@dataclass
class WorkflowEdge:
    """Represents a connection between workflow nodes"""
    from_node: str
    to_node: str
    condition: Optional[str] = None
    data_flow: Dict[str, Any] = None

    def to_dict(self):
        return {
            "from_node": self.from_node,
            "to_node": self.to_node,
            "condition": self.condition,
            "data_flow": self.data_flow or {}
        }

@dataclass
class WorkflowState:
    """Complete workflow state for visualization"""
    workflow_id: str
    company_id: str
    workflow_type: str
    status: WorkflowStatus
    nodes: Dict[str, WorkflowNode]
    edges: List[WorkflowEdge]
    start_time: datetime
    end_time: Optional[datetime] = None
    progress_percentage: float = 0.0
    current_node: Optional[str] = None
    estimated_completion: Optional[datetime] = None
    performance_metrics: Dict[str, float] = None

    def to_dict(self):
        return {
            "workflow_id": self.workflow_id,
            "company_id": self.company_id,
            "workflow_type": self.workflow_type,
            "status": self.status.value,
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "edges": [e.to_dict() for e in self.edges],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "progress_percentage": self.progress_percentage,
            "current_node": self.current_node,
            "estimated_completion": self.estimated_completion.isoformat() if self.estimated_completion else None,
            "performance_metrics": self.performance_metrics or {}
        }

class MermaidGenerator:
    """Generates Mermaid.js diagrams from workflow states"""
    
    @staticmethod
    def generate_workflow_diagram(workflow_state: WorkflowState) -> str:
        """Generate Mermaid.js flowchart from workflow state"""
        lines = ["graph TD"]
        
        # Add nodes with status-based styling
        for node_id, node in workflow_state.nodes.items():
            status_class = f"class{node.status.value.capitalize()}"
            node_label = f"{node.name}"
            
            # Add duration if available
            if node.duration:
                node_label += f"\\n({node.duration:.1f}s)"
            
            # Node shape based on type
            if node.type == "agent":
                lines.append(f'    {node_id}["{node_label}"]:::{status_class}')
            elif node.type == "decision":
                lines.append(f'    {node_id}{"{"}"{node_label}"{"}"}:::{status_class}')
            elif node.type == "task":
                lines.append(f'    {node_id}(("{node_label}")):::{status_class}')
            else:
                lines.append(f'    {node_id}["{node_label}"]:::{status_class}')
        
        # Add edges with conditions
        for edge in workflow_state.edges:
            if edge.condition:
                lines.append(f'    {edge.from_node} -->|{edge.condition}| {edge.to_node}')
            else:
                lines.append(f'    {edge.from_node} --> {edge.to_node}')
        
        # Add CSS classes for status styling
        lines.extend([
            "",
            "    classDef classIdle fill:#e1e5e9,stroke:#6c757d",
            "    classDef classWorking fill:#fff3cd,stroke:#ffc107,stroke-width:3px",
            "    classDef classWaiting fill:#d1ecf1,stroke:#17a2b8",
            "    classDef classCompleted fill:#d4edda,stroke:#28a745",
            "    classDef classFailed fill:#f8d7da,stroke:#dc3545"
        ])
        
        # Highlight current node
        if workflow_state.current_node:
            lines.append(f"    classDef currentNode stroke:#007bff,stroke-width:4px")
            lines.append(f"    class {workflow_state.current_node} currentNode")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_performance_chart(performance_data: Dict[str, Any]) -> str:
        """Generate Mermaid.js chart for performance metrics"""
        if not performance_data:
            return ""
        
        # Generate a simple bar chart representation
        lines = ["graph LR"]
        
        for metric, value in performance_data.items():
            if isinstance(value, (int, float)):
                bar_length = min(int(value * 10), 100)  # Scale for visualization
                lines.append(f'    {metric}["{metric}: {value}"] --> Bar{metric}["{"|" * (bar_length // 10)}"]')
        
        return "\n".join(lines)

class WorkflowVisualizationManager:
    """Manages real-time workflow visualization and WebSocket connections"""
    
    def __init__(self):
        # WebSocket connections organized by company_id
        self.connections: Dict[str, Set[WebSocket]] = {}
        # Active workflow states
        self.workflow_states: Dict[str, WorkflowState] = {}
        # Performance metrics cache
        self.performance_cache: Dict[str, Dict[str, float]] = {}
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        
    async def connect_user(self, websocket: WebSocket, user_id: str, company_id: str, platforms: List[str]):
        """Connect a user to workflow visualization updates"""
        await websocket.accept()
        
        # Add to company connections
        if company_id not in self.connections:
            self.connections[company_id] = set()
        self.connections[company_id].add(websocket)
        
        # Store connection metadata
        self.connection_metadata[websocket] = {
            "user_id": user_id,
            "company_id": company_id,
            "platforms": platforms,
            "connected_at": datetime.utcnow(),
            "last_heartbeat": datetime.utcnow()
        }
        
        # Send initial workflow states
        await self._send_initial_workflows(websocket, company_id)
        
        logger.info(f"User {user_id} connected to workflow visualization for company {company_id}")
    
    def disconnect_user(self, websocket: WebSocket):
        """Disconnect a user from workflow visualization"""
        metadata = self.connection_metadata.get(websocket)
        if metadata:
            company_id = metadata["company_id"]
            user_id = metadata["user_id"]
            
            # Remove from connections
            if company_id in self.connections:
                self.connections[company_id].discard(websocket)
                if not self.connections[company_id]:
                    del self.connections[company_id]
            
            # Clean up metadata
            del self.connection_metadata[websocket]
            
            logger.info(f"User {user_id} disconnected from workflow visualization")
    
    async def _send_initial_workflows(self, websocket: WebSocket, company_id: str):
        """Send current workflow states to newly connected client"""
        company_workflows = {
            wf_id: wf_state.to_dict() 
            for wf_id, wf_state in self.workflow_states.items()
            if wf_state.company_id == company_id
        }
        
        if company_workflows:
            await self._send_to_websocket(websocket, {
                "type": "initial_workflows",
                "workflows": company_workflows,
                "timestamp": datetime.utcnow().isoformat()
            })
    
    async def update_workflow_state(self, workflow_state: WorkflowState):
        """Update workflow state and broadcast to connected clients"""
        self.workflow_states[workflow_state.workflow_id] = workflow_state
        
        # Generate Mermaid diagram
        mermaid_diagram = MermaidGenerator.generate_workflow_diagram(workflow_state)
        
        # Prepare update message
        update_message = {
            "type": "workflow_update",
            "workflow_id": workflow_state.workflow_id,
            "company_id": workflow_state.company_id,
            "workflow_state": workflow_state.to_dict(),
            "mermaid_diagram": mermaid_diagram,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Broadcast to all company connections
        await self._broadcast_to_company(workflow_state.company_id, update_message)
    
    async def update_agent_status(self, workflow_id: str, agent_id: str, status: AgentStatus, 
                                 metrics: Optional[Dict[str, float]] = None):
        """Update individual agent status within a workflow"""
        if workflow_id not in self.workflow_states:
            logger.warning(f"Workflow {workflow_id} not found for agent update")
            return
        
        workflow_state = self.workflow_states[workflow_id]
        
        if agent_id not in workflow_state.nodes:
            logger.warning(f"Agent {agent_id} not found in workflow {workflow_id}")
            return
        
        # Update agent status
        agent_node = workflow_state.nodes[agent_id]
        old_status = agent_node.status
        agent_node.status = status
        
        # Update timing
        if status == AgentStatus.WORKING and old_status != AgentStatus.WORKING:
            agent_node.start_time = datetime.utcnow()
        elif status in [AgentStatus.COMPLETED, AgentStatus.FAILED]:
            agent_node.end_time = datetime.utcnow()
            if agent_node.start_time:
                agent_node.duration = (agent_node.end_time - agent_node.start_time).total_seconds()
        
        # Update metrics
        if metrics:
            agent_node.metrics = metrics
        
        # Update workflow progress
        await self._update_workflow_progress(workflow_state)
        
        # Broadcast update
        await self.update_workflow_state(workflow_state)
    
    async def _update_workflow_progress(self, workflow_state: WorkflowState):
        """Calculate and update overall workflow progress"""
        total_nodes = len(workflow_state.nodes)
        completed_nodes = sum(1 for node in workflow_state.nodes.values() 
                             if node.status == AgentStatus.COMPLETED)
        
        workflow_state.progress_percentage = (completed_nodes / total_nodes) * 100
        
        # Find current working node
        working_nodes = [node.id for node in workflow_state.nodes.values() 
                        if node.status == AgentStatus.WORKING]
        workflow_state.current_node = working_nodes[0] if working_nodes else None
        
        # Update workflow status
        if completed_nodes == total_nodes:
            workflow_state.status = WorkflowStatus.COMPLETED
            workflow_state.end_time = datetime.utcnow()
        elif any(node.status == AgentStatus.FAILED for node in workflow_state.nodes.values()):
            workflow_state.status = WorkflowStatus.FAILED
        elif any(node.status == AgentStatus.WORKING for node in workflow_state.nodes.values()):
            workflow_state.status = WorkflowStatus.RUNNING
    
    async def update_performance_metrics(self, company_id: str, metrics: Dict[str, float]):
        """Update performance metrics for a company"""
        self.performance_cache[company_id] = {
            **self.performance_cache.get(company_id, {}),
            **metrics,
            "last_updated": datetime.utcnow().timestamp()
        }
        
        # Generate performance chart
        performance_chart = MermaidGenerator.generate_performance_chart(metrics)
        
        # Broadcast performance update
        await self._broadcast_to_company(company_id, {
            "type": "performance_update",
            "company_id": company_id,
            "metrics": metrics,
            "performance_chart": performance_chart,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def _broadcast_to_company(self, company_id: str, message: Dict[str, Any]):
        """Broadcast message to all connections for a company"""
        if company_id not in self.connections:
            return
        
        disconnected = []
        
        for websocket in self.connections[company_id].copy():
            try:
                await self._send_to_websocket(websocket, message)
            except Exception as e:
                logger.error(f"Failed to send message to WebSocket: {e}")
                disconnected.append(websocket)
        
        # Clean up disconnected WebSockets
        for websocket in disconnected:
            self.disconnect_user(websocket)
    
    async def _send_to_websocket(self, websocket: WebSocket, message: Dict[str, Any]):
        """Send message to a specific WebSocket with error handling"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"WebSocket send failed: {e}")
            raise
    
    async def handle_websocket_message(self, websocket: WebSocket, message: Dict[str, Any]):
        """Handle incoming WebSocket messages"""
        message_type = message.get("type")
        
        if message_type == "ping":
            # Update heartbeat
            if websocket in self.connection_metadata:
                self.connection_metadata[websocket]["last_heartbeat"] = datetime.utcnow()
            
            await self._send_to_websocket(websocket, {
                "type": "pong",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        elif message_type == "subscribe_workflow":
            workflow_id = message.get("workflow_id")
            if workflow_id and workflow_id in self.workflow_states:
                workflow_state = self.workflow_states[workflow_id]
                await self._send_to_websocket(websocket, {
                    "type": "workflow_subscribed",
                    "workflow_id": workflow_id,
                    "workflow_state": workflow_state.to_dict(),
                    "mermaid_diagram": MermaidGenerator.generate_workflow_diagram(workflow_state)
                })
        
        elif message_type == "request_performance_metrics":
            metadata = self.connection_metadata.get(websocket)
            if metadata:
                company_id = metadata["company_id"]
                metrics = self.performance_cache.get(company_id, {})
                performance_chart = MermaidGenerator.generate_performance_chart(metrics)
                
                await self._send_to_websocket(websocket, {
                    "type": "performance_metrics",
                    "company_id": company_id,
                    "metrics": metrics,
                    "performance_chart": performance_chart,
                    "timestamp": datetime.utcnow().isoformat()
                })
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get current connection statistics"""
        total_connections = sum(len(conns) for conns in self.connections.values())
        
        return {
            "total_connections": total_connections,
            "companies_connected": len(self.connections),
            "active_workflows": len(self.workflow_states),
            "performance_cache_size": len(self.performance_cache),
            "connection_details": {
                company_id: {
                    "connections": len(conns),
                    "active_workflows": len([wf for wf in self.workflow_states.values() 
                                           if wf.company_id == company_id])
                }
                for company_id, conns in self.connections.items()
            }
        }
    
    async def create_workflow_template(self, workflow_type: str, platform: str) -> Dict[str, Any]:
        """Create workflow template for different platforms"""
        templates = {
            "bizoholic": {
                "marketing_campaign": {
                    "nodes": {
                        "research": {"name": "Market Research", "type": "agent"},
                        "strategy": {"name": "Campaign Strategy", "type": "agent"},
                        "content": {"name": "Content Creation", "type": "agent"},
                        "approval": {"name": "Content Approval", "type": "decision"},
                        "execution": {"name": "Campaign Execution", "type": "agent"},
                        "monitoring": {"name": "Performance Monitoring", "type": "agent"}
                    },
                    "edges": [
                        {"from_node": "research", "to_node": "strategy"},
                        {"from_node": "strategy", "to_node": "content"},
                        {"from_node": "content", "to_node": "approval"},
                        {"from_node": "approval", "to_node": "execution", "condition": "approved"},
                        {"from_node": "approval", "to_node": "content", "condition": "rejected"},
                        {"from_node": "execution", "to_node": "monitoring"}
                    ]
                }
            },
            "coreldove": {
                "product_sourcing": {
                    "nodes": {
                        "discovery": {"name": "Product Discovery", "type": "agent"},
                        "validation": {"name": "Product Validation", "type": "agent"},
                        "analysis": {"name": "Competitive Analysis", "type": "agent"},
                        "pricing": {"name": "Pricing Strategy", "type": "agent"},
                        "listing": {"name": "Product Listing", "type": "agent"}
                    },
                    "edges": [
                        {"from_node": "discovery", "to_node": "validation"},
                        {"from_node": "validation", "to_node": "analysis"},
                        {"from_node": "analysis", "to_node": "pricing"},
                        {"from_node": "pricing", "to_node": "listing"}
                    ]
                }
            },
            "thrillring": {
                "content_workflow": {
                    "nodes": {
                        "ideation": {"name": "Content Ideation", "type": "agent"},
                        "creation": {"name": "Content Creation", "type": "agent"},
                        "review": {"name": "Quality Review", "type": "decision"},
                        "optimization": {"name": "SEO Optimization", "type": "agent"},
                        "publishing": {"name": "Content Publishing", "type": "agent"}
                    },
                    "edges": [
                        {"from_node": "ideation", "to_node": "creation"},
                        {"from_node": "creation", "to_node": "review"},
                        {"from_node": "review", "to_node": "optimization", "condition": "approved"},
                        {"from_node": "review", "to_node": "creation", "condition": "needs_revision"},
                        {"from_node": "optimization", "to_node": "publishing"}
                    ]
                }
            }
        }
        
        return templates.get(platform, {}).get(workflow_type, {})

# Global visualization manager instance
visualization_manager = WorkflowVisualizationManager()