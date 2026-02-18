import logging
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Any, Optional
import os

logger = logging.getLogger(__name__)

class KAGService:
    """
    Knowledge Augmented Generation (KAG) Service.
    Manages relationships between knowledge chunks to provide richer context.
    """
    
    def __init__(self):
        self.db_url = os.getenv("VECTOR_DB_URL") or os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/bizoholic"
        self.engine = sa.create_engine(self.db_url, pool_pre_ping=True, pool_recycle=300, pool_size=5, max_overflow=10)
        self.Session = sessionmaker(bind=self.engine)
        self._init_db()

    def _init_db(self):
        """Ensure knowledge_links table exists"""
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

    def link_chunks(self, source_id: int, target_id: int, rel_type: str, weight: float = 1.0, metadata: Optional[Dict] = None):
        """Create a link between two knowledge chunks"""
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
                logger.error(f"Failed to link chunks: {e}")
                session.rollback()

    async def get_related_knowledge(self, chunk_id: int, depth: int = 1) -> List[Dict[str, Any]]:
        """Retrieve knowledge chunks related to the given chunk ID"""
        # This performs a recursive graph traversal in SQL (CTE)
        with self.Session() as session:
            try:
                result = session.execute(
                    sa.text("""
                        WITH RECURSIVE knowledge_graph AS (
                            -- Anchor: direct links from source
                            SELECT target_id, relationship_type, weight, 1 as level
                            FROM knowledge_links
                            WHERE source_id = :chunk_id
                            
                            UNION
                            
                            -- Recursive: follow links up to depth
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
                logger.error(f"Failed to retrieve related knowledge: {e}")
                return []

# Singleton instance
kag_service = KAGService()
