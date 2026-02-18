import logging
from typing import Dict, Any, List
from temporalio import activity
from app.core.kag_service import kag_service
from app.core.intelligence import call_ai_agent_with_rag

logger = logging.getLogger(__name__)

@activity.defn(name="extract_relations_activity")
async def extract_relations_activity(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Activity to extract entities and relationships using the RelationExtractionAgent.
    """
    content = data.get("content")
    chunk_id = data.get("chunk_id")
    tenant_id = data.get("tenant_id", "global")
    
    if not content:
        return {"relationships": []}

    try:
        # Call the specialized RelationExtractionAgent via intelligence layer
        extraction_result = await call_ai_agent_with_rag(
            agent_type="relation_extraction",
            task_description=f"Extract entities and relationships from knowledge chunk {chunk_id}",
            payload={"content": content, "chunk_id": chunk_id},
            tenant_id=tenant_id,
            use_rag=False, # Avoid circular RAG dependencies during extraction
            auto_ingest=False
        )
        
        if not extraction_result or "relationships" not in extraction_result:
            logger.warning(f"No relationships extracted for chunk {chunk_id}")
            return {"relationships": []}

        return extraction_result
        
    except Exception as e:
        logger.error(f"Failed to extract relations for chunk {chunk_id} in activity: {e}")
        raise e

@activity.defn(name="link_graph_activity")
async def link_graph_activity(data: Dict[str, Any]) -> int:
    """
    Activity to link the current chunk to extracted entities in the graph.
    """
    chunk_id = data.get("chunk_id")
    relationships = data.get("relationships", [])
    link_count = 0
    
    for rel in relationships:
        try:
            rel_type = rel.get("type", "RELATED_TO")
            target_label = rel.get("target_label", "Unknown")
            
            # Using the deterministic hash logic for mock ID for now
            target_id = abs(hash(target_label)) % 1000000
            
            await kag_service.link_chunks(
                source_id=chunk_id,
                target_id=target_id,
                rel_type=rel_type,
                weight=rel.get("weight", 1.0),
                metadata={"target_label": target_label, "extracted": True}
            )
            link_count += 1
        except Exception as e:
            logger.error(f"Failed to link relationship in activity for chunk {chunk_id}: {e}")
            # We continue with other links even if one fails
            
    return link_count
