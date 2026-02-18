import logging
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Any, Optional
import os
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

class KAGService:
    """
    Knowledge Augmented Generation (KAG) Service.
    Manages relationships between knowledge chunks to provide richer context.
    Supports both PostgreSQL (relational links) and Neo4j (high-performance graph).
    """
    
    def __init__(self):
        # Database fallback chain
        self.db_url = os.getenv("VECTOR_DB_URL") or os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/bizoholic"
        self.engine = sa.create_engine(self.db_url, pool_pre_ping=True, pool_recycle=300, pool_size=5, max_overflow=10)
        self.Session = sessionmaker(bind=self.engine)
        
        # Neo4j setup
        self.neo4j_uri = os.getenv("NEO4J_URI", "neo4j+s://42c5bda2.databases.neo4j.io")
        self.neo4j_user = os.getenv("NEO4J_USERNAME", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.neo4j_driver = None
        
        if self.neo4j_password:
            try:
                self.neo4j_driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))
                self.neo4j_driver.verify_connectivity()
                logger.info("Connected to Neo4j Aura Cloud")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
        
        self._init_db()

    def _init_db(self):
        """Ensure knowledge_links table exists in Postgres"""
        try:
            with self.engine.connect() as conn:
                conn.execute(sa.text("""
                    CREATE TABLE IF NOT EXISTS knowledge_links (
                        id SERIAL PRIMARY KEY,
                        source_id INTEGER REFERENCES knowledge_chunks(id) ON DELETE CASCADE,
                        target_id INTEGER REFERENCES knowledge_chunks(id) ON DELETE CASCADE,
                        relationship_type TEXT NOT NULL,
                        weight FLOAT DEFAULT 1.0,
                        metadata JSONB,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(source_id, target_id, relationship_type)
                    )
                """))
                conn.commit()
                logger.info("KAG/Knowledge links table initialized")
        except Exception as e:
            logger.error(f"Failed to initialize KAG database: {e}")

    def close(self):
        if self.neo4j_driver:
            self.neo4j_driver.close()

    def link_chunks(self, source_id: int, target_id: int, rel_type: str, weight: float = 1.0, metadata: Optional[Dict] = None):
        """Create a link between two knowledge chunks in both SQL and Graph DBs"""
        # 1. Store in PostgreSQL for referential integrity
        with self.Session() as session:
            try:
                session.execute(
                    sa.text("""
                        INSERT INTO knowledge_links (source_id, target_id, relationship_type, weight, metadata)
                        VALUES (:source_id, :target_id, :rel_type, :weight, :metadata)
                        ON CONFLICT (source_id, target_id, relationship_type) DO UPDATE SET weight = :weight, metadata = :metadata
                    """),
                    {
                        "source_id": source_id,
                        "target_id": target_id,
                        "rel_type": rel_type,
                        "weight": weight,
                        "metadata": metadata
                    }
                )
                session.commit()
            except Exception as e:
                logger.error(f"Failed to link chunks in SQL: {e}")
                session.rollback()

        # 2. Store in Neo4j for high-performance retrieval
        if self.neo4j_driver:
            try:
                with self.neo4j_driver.session() as session:
                    session.execute_write(
                        self._neo4j_create_rel,
                        source_id,
                        target_id,
                        rel_type,
                        weight,
                        metadata or {}
                    )
            except Exception as e:
                logger.error(f"Failed to link chunks in Neo4j: {e}")

    @staticmethod
    def _neo4j_create_rel(tx, source_id, target_id, rel_type, weight, metadata):
        query = (
            "MERGE (s:Chunk {id: $source_id}) "
            "MERGE (t:Chunk {id: $target_id}) "
            "MERGE (s)-[r:RELATED {type: $rel_type}]->(t) "
            "SET r.weight = $weight, r.metadata = $metadata"
        )
        tx.run(query, source_id=source_id, target_id=target_id, rel_type=rel_type, weight=weight, metadata=metadata)

    async def get_related_knowledge(self, chunk_id: int, depth: int = 1) -> List[Dict[str, Any]]:
        """Retrieve knowledge chunks related to the given chunk ID, preferring Neo4j"""
        if self.neo4j_driver:
            try:
                with self.neo4j_driver.session() as session:
                    result = session.execute_read(self._neo4j_get_related, chunk_id, depth)
                    return result
            except Exception as e:
                logger.error(f"Neo4j retrieval failed: {e}. Falling back to PostgreSQL.")

        # Fallback to PostgreSQL recursive CTE
        with self.Session() as session:
            try:
                result = session.execute(
                    sa.text("""
                        WITH RECURSIVE knowledge_graph AS (
                            SELECT target_id, relationship_type, weight, 1 as level
                            FROM knowledge_links
                            WHERE source_id = :chunk_id
                            UNION
                            SELECT kl.target_id, kl.relationship_type, kl.weight, kg.level + 1
                            FROM knowledge_links kl
                            INNER JOIN knowledge_graph kg ON kl.source_id = kg.target_id
                            WHERE kg.level < :depth
                        )
                        SELECT kc.id, kc.content, kc.metadata, kg.relationship_type, kg.weight
                        FROM knowledge_chunks kc
                        JOIN knowledge_graph kg ON kc.id = kg.target_id
                    """),
                    {"chunk_id": chunk_id, "depth": depth}
                )
                
                return [
                    {
                        "id": row.id,
                        "content": row.content,
                        "metadata": row.metadata,
                        "relationship": row.relationship_type,
                        "weight": row.weight
                    } for row in result
                ]
            except Exception as e:
                logger.error(f"PostgreSQL KAG retrieval failed: {e}")
                return []

    @staticmethod
    def _neo4j_get_related(tx, chunk_id, depth):
        query = (
            "MATCH (s:Chunk {id: $chunk_id})-[r:RELATED*1..$depth]->(t:Chunk) "
            "RETURN t.id AS id, r[size(r)-1].type AS relationship, r[size(r)-1].weight AS weight"
        )
        result = tx.run(query, chunk_id=chunk_id, depth=depth)
        # Note: In a real scenario, we'd still need SQL for the 'content' if not mirrored in Neo4j
        # For Phase 7C, we assuming we might need to join back to SQL or mirror content.
        # Let's mirror minimal data first.
        return [{"id": record["id"], "relationship": record["relationship"], "weight": record["weight"]} for record in result]

    async def extract_and_link(self, chunk_id: int, content: str, tenant_id: str = "global"):
        """
        Extract entities and relationships from content and link them in the graph.
        Uses the RelationExtractionAgent via the intelligence layer.
        """
        from app.core.intelligence import call_ai_agent_with_rag
        
        try:
            # Call the specialized RelationExtractionAgent
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
                return

            relationships = extraction_result.get("relationships", [])
            for rel in relationships:
                # In a real setup, we might need to resolve source_id/target_id to other chunks
                # For now, we link the current chunk to extracted entities or other chunks
                rel_type = rel.get("type", "RELATED_TO")
                target_label = rel.get("target_label", "Unknown") # Assuming agent returns labels
                
                # Mock linking logic for now: link chunk_id to a virtual target representing the entity
                # In a mature KAG, we'd have a separate Entity table/nodes.
                await self.link_chunks(
                    source_id=chunk_id,
                    target_id=abs(hash(target_label)) % 1000000, # Deterministic mock ID
                    rel_type=rel_type,
                    weight=rel.get("weight", 1.0),
                    metadata={"target_label": target_label, "extracted": True}
                )
                
            logger.info(f"Extracted and linked {len(relationships)} relationships for chunk {chunk_id}")
            
        except Exception as e:
            logger.error(f"Failed to extract and link for chunk {chunk_id}: {e}")

# Singleton instance
kag_service = KAGService()
