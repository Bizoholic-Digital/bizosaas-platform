
import asyncio
import logging
import os
from app.dependencies import SessionLocal
from app.services.knowledge_graph import KnowledgeGraphBuilder, ToolRelationship

logging.basicConfig(level=logging.INFO)

async def verify():
    db = SessionLocal()
    try:
        builder = KnowledgeGraphBuilder(db)
        
        # 1. Build initial graph
        print(">>> Building initial graph...")
        graph = await builder.build_graph()
        initial_edge_count = len(graph.edges)
        print(f"Initial edges: {initial_edge_count}")
        
        # 2. Record a simulated interaction
        source = "brave-search"
        target = "google-drive"
        print(f">>> Recording interaction: {source} -> {target}")
        graph.record_interaction(db, source, target, success=True)
        
        # 3. Check DB directly
        from app.models.mcp import KagRelationship
        db_rel = db.query(KagRelationship).filter(
            KagRelationship.source_tool == source,
            KagRelationship.target_tool == target
        ).first()
        
        if db_rel:
            print(f"SUCCESS: Relationship found in DB. Strength: {db_rel.strength}, Evidence: {db_rel.evidence_count}")
        else:
            print("FAILURE: Relationship NOT found in DB.")
            return

        # 4. Rebuild graph and check if edge is loaded
        print(">>> Rebuilding graph to verify persistence...")
        new_builder = KnowledgeGraphBuilder(db)
        new_graph = await new_builder.build_graph()
        
        edge = next((e for e in new_graph.edges if e.source_tool == source and e.target_tool == target), None)
        if edge:
            print(f"SUCCESS: Persistent edge loaded. Strength: {edge.strength:.2f}")
        else:
            print("FAILURE: Persistent edge NOT loaded into graph.")

    except Exception as e:
        print(f"CRITICAL ERROR during verification: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(verify())
