import asyncio
import os
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock environment for testing if needed
os.environ["CURRENT_TIME"] = "2026-02-16T10:00:00Z"

async def test_hybrid_rag():
    try:
        # Import services
        # We need to ensure we can import from app.core
        sys.path.append(os.path.join(os.getcwd()))
        
        # Load Vault secrets first
        from main import load_vault_secrets_sync
        load_vault_secrets_sync()
        logger.info("Vault secrets loaded")
        
        from app.core.rag import rag_service
        from app.core.kag_service import kag_service
        
        logger.info("--- Testing Knowledge Ingestion ---")
        content = "Bizoholic is a leading provider of SaaS solutions for digital transformation. They partner with Thrillring for gaming experiences."
        metadata = {"source": "test_script", "category": "company_info"}
        tenant_id = "test_tenant"
        
        doc_id = await rag_service.ingest_knowledge(content, metadata, tenant_id=tenant_id)
        logger.info(f"Ingested document ID: {doc_id}")
        
        # Wait a bit for background task (extraction) to potentially start
        await asyncio.sleep(2)
        
        logger.info("--- Testing Hybrid Retrieval ---")
        query = "Tell me about Bizoholic and its partners"
        context = await rag_service.retrieve_context(query, filters={"tenant_id": tenant_id})
        
        logger.info(f"Retrieved {len(context)} context chunks")
        for i, chunk in enumerate(context):
            logger.info(f"Chunk {i+1}: {chunk[:100]}...")
            
        if len(context) > 0:
            logger.info("SUCCESS: Hybrid RAG retrieved context.")
        else:
            logger.warning("WARNING: No context retrieved.")

        logger.info("--- Testing Graph Fallback (SQL) ---")
        # Manually link if extraction didn't run (mocking extraction result)
        if doc_id:
            await kag_service.link_chunks(
                source_id=int(doc_id),
                target_id=999999, # Mock entity
                rel_type="PARTNER_OF",
                metadata={"target_label": "Thrillring"}
            )
            logger.info("Manually linked chunks for verification")
            
            related = await kag_service.get_related_knowledge(int(doc_id))
            logger.info(f"Related knowledge found: {len(related)}")
            for rel in related:
                logger.info(f"Relation: {rel['relationship']} with target ID {rel['id']}")

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_hybrid_rag())
