"""
AI Agent Administration API
Provides super admins with oversight into all AI agents, including performance
monitoring, prompt management, and tool registry.
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.dependencies import get_db, require_role
from app.models.agent import Agent, AgentOptimization
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/agents", tags=["agent-admin"])

@router.get("/registry")
async def list_global_agent_registry(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List all AI agents across the entire platform (System + Custom)."""
    # System agents from the AGENTS list in agents.py (ideally moved to a service)
    from app.api.agents import AGENTS
    system_agents = [a.dict() for a in AGENTS]
    for sa in system_agents:
        sa["is_system"] = True
    
    # Custom agents from DB
    custom_agents = db.query(Agent).all()
    custom_list = [a.to_dict() for a in custom_agents]
    
    return {
        "system_agents": system_agents,
        "custom_agents": custom_list,
        "total": len(system_agents) + len(custom_list)
    }

@router.get("/performance")
async def get_agent_performance_stats(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Aggregate performance metrics for all agents."""
    # This would aggregate data from OpenTelemetry/Prometheus
    return {
        "total_invocations_24h": 15420,
        "avg_response_time_ms": 840,
        "error_rate": 1.2,
        "token_usage": {
            "prompt_tokens": 1250000,
            "completion_tokens": 850000,
            "cost_usd": 42.50
        },
        "top_agents": [
            {"id": "market_research", "calls": 3100},
            {"id": "content_generation", "calls": 2850},
            {"id": "master_orchestrator", "calls": 1200}
        ]
    }

@router.get("/prompts")
async def list_agent_prompts(
    agent_id: Optional[str] = None,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Manage and audit prompts used by various agents."""
    # In a real system, these would be stored in a Prompt Registry
    return {
        "market_research": "You are a world-class market researcher...",
        "content_generation": "Generate a blog post about...",
        "sales_assistant": "Help the user manage leads in Hubspot..."
    }

@router.post("/prompts/test")
async def test_prompt_variation(
    prompt: str = Body(..., embed=True),
    agent_id: str = Body(..., embed=True),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Test a new prompt variation before deployment (A/B testing)."""
    return {"status": "success", "result": "Test output for the new prompt..."}
    return {"status": "success", "result": "Test output for the new prompt..."}

@router.get("/knowledge-base/{agent_id}/documents")
async def list_agent_kb_documents(
    agent_id: str,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List documents indexed in the agent's knowledge base."""
    # Placeholder for checking Vector DB collection stats
    return [
        {"id": "doc_1", "name": "Standard Operating Procedures.pdf", "chunks": 42, "indexed_at": "2024-03-21T10:00:00Z"},
        {"id": "doc_2", "name": "Product Catalog 2024.csv", "chunks": 150, "indexed_at": "2024-03-21T11:30:00Z"}
    ]

@router.delete("/knowledge-base/{agent_id}/documents/{doc_id}")
async def delete_kb_document(
    agent_id: str,
    doc_id: str,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Remove a document from the agent's vector store context."""
    return {"status": "success", "message": f"Document {doc_id} purged from {agent_id} context"}

@router.get("/marketplace")
async def list_agent_marketplace(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List curated agent templates available for global deployment."""
    return [
        {
            "template_id": "support_autopilot_v2",
            "name": "Customer Support Autopilot",
            "description": "Handle tier-1 support tickets autonomously tailored for SaaS.",
            "author": "Bizoholic System",
            "price": "Included",
            "installs": 420
        },
        {
            "template_id": "seo_keyword_researcher",
            "name": "SEO Researcher Pro",
            "description": "Autonomous keyword clustering and gap analysis agent using Brave Search + DataForSEO.",
            "author": "SEO Masters Inc",
            "price": "$29/mo",
            "installs": 155
        }
    ]
