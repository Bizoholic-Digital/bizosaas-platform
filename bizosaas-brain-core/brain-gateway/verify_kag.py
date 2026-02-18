import asyncio
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def verify_kag():
    print("--- Knowledge Graph (KAG) Verification ---")
    
    # 1. Check Neo4j Connectivity (via KagService)
    from app.core.kag_service import kag_service
    if kag_service.neo4j_driver:
        print("✅ Neo4j Driver initialized and connected.")
    else:
        print("❌ Neo4j Driver NOT initialized. Check credentials in .env.")
        # We can still continue to test SQL fallback
    
    # 2. Test RAG Ingestion with KAG trigger
    from app.core.rag import rag_service
    content = "Bizoholic is a digital platform that partners with AWS to provide cloud solutions."
    metadata = {"source": "kag_test"}
    tenant_id = "test_tenant"
    
    print(f"\nIngesting test knowledge: '{content}'")
    doc_id = await rag_service.ingest_knowledge(content, metadata, tenant_id=tenant_id)
    
    if doc_id:
        print(f"✅ Knowledge ingested. ID: {doc_id}")
    else:
        print("❌ Knowledge ingestion failed.")
        return

    # Wait for background task (KAG extraction) to at least start/finish
    print("Waiting for KAG extraction background task...")
    await asyncio.sleep(10) # Extraction calls an AI agent, so it takes time
    
    # 3. Verify Links in PostgreSQL
    from sqlalchemy import text
    with kag_service.engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM knowledge_links WHERE source_id = :id"), {"id": int(doc_id)})
        links = result.fetchall()
        print(f"\nPostgreSQL Links found: {len(links)}")
        for link in links:
            print(f" - Relationship: {link.relationship_type}, TargetID: {link.target_id}")

    # 4. Verify Links in Neo4j
    if kag_service.neo4j_driver:
        print("\nChecking Neo4j links...")
        related = await kag_service.get_related_knowledge(int(doc_id))
        print(f"Neo4j Related Chunks found: {len(related)}")
        for rel in related:
            print(f" - Relationship: {rel['relationship']}, TargetID: {rel['id']}")
            
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    asyncio.run(verify_kag())
