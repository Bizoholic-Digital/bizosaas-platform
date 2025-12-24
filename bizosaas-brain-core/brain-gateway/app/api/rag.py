from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.core import rag

router = APIRouter(prefix="/api/brain/rag", tags=["rag"])

class IngestRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None
    tenant_id: str = "global"
    agent_id: str = "global"

class RetrieveRequest(BaseModel):
    query: str
    agent_id: str = "global"
    limit: int = 5

@router.post("/ingest")
async def ingest_knowledge(request: IngestRequest):
    """Ingest knowledge chunk into vector database"""
    doc_id = await rag.rag_service.ingest_knowledge(
        content=request.content,
        metadata=request.metadata,
        tenant_id=request.tenant_id,
        agent_id=request.agent_id
    )
    if doc_id:
        return {"id": doc_id, "status": "success"}
    else:
        raise HTTPException(status_code=500, detail="Failed to ingest knowledge")

@router.post("/retrieve")
async def retrieve_context(request: RetrieveRequest):
    """Retrieve relevant context for a query"""
    context = await rag.rag_service.retrieve_context(
        query=request.query,
        agent_id=request.agent_id,
        limit=request.limit
    )
    return {"context": context}

@router.post("/search")
async def hybrid_search(query: str):
    """Perform hybrid search"""
    results = await rag.rag_service.hybrid_search(query)
    return {"results": results}
