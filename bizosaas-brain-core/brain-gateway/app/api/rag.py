from fastapi import APIRouter, HTTPException, Depends, Body
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
    tenant_id: Optional[str] = "global"

class LinkRequest(BaseModel):
    source_id: int
    target_id: int
    rel_type: str
    weight: float = 1.0
    metadata: Optional[Dict[str, Any]] = None

class MemoryStoreRequest(BaseModel):
    content: str
    agent_id: str
    tenant_id: str
    metadata: Optional[Dict[str, Any]] = None

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

@router.post("/link")
async def link_chunks(request: LinkRequest):
    """Create a KAG link between two knowledge chunks"""
    from app.core.kag_service import kag_service
    kag_service.link_chunks(
        source_id=request.source_id,
        target_id=request.target_id,
        rel_type=request.rel_type,
        weight=request.weight,
        metadata=request.metadata
    )
    return {"status": "success"}

@router.get("/related/{chunk_id}")
async def get_related_knowledge(chunk_id: int, depth: int = 1):
    """Retrieve knowledge chunks related to the given chunk ID via KAG"""
    from app.core.kag_service import kag_service
    results = await kag_service.get_related_knowledge(chunk_id=chunk_id, depth=depth)
    return {"related": results}

@router.post("/memory/store")
async def store_memory(request: MemoryStoreRequest):
    """Store agent long-term memory"""
    doc_id = await rag.rag_service.store_memory(
        content=request.content,
        agent_id=request.agent_id,
        tenant_id=request.tenant_id,
        metadata=request.metadata
    )
    if doc_id:
        return {"id": doc_id, "status": "success"}
    else:
        raise HTTPException(status_code=500, detail="Failed to store memory")

@router.post("/memory/long-term")
async def retrieve_long_term_memory(request: RetrieveRequest):
    """Retrieve relevant long-term memories"""
    memories = await rag.rag_service.retrieve_long_term_memory(
        query=request.query,
        agent_id=request.agent_id,
        tenant_id=request.tenant_id or "global",
        limit=request.limit
    )
    return {"memories": memories}

@router.post("/search")
async def hybrid_search(query: str, filters: Optional[Dict[str, Any]] = Body(None)):
    """Perform hybrid search with optional metadata filters"""
    results = await rag.rag_service.hybrid_search(query, filters=filters)
    return {"results": results}
