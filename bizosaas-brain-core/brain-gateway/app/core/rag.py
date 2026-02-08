import os
import json
import httpx
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class RAGService:
    """
    RAG Service for managing Knowledge Augmented Generation (KAG)
    and Vector retrieval for AI Agents using pgvector.
    """
    
    def __init__(self):
        self.db_url = os.getenv("VECTOR_DB_URL") or os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/bizoholic"
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.engine = sa.create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self._init_db()

    def _init_db(self):
        """Ensure pgvector extension and table exist"""
        try:
            with self.engine.connect() as conn:
                conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.execute(sa.text("""
                    CREATE TABLE IF NOT EXISTS knowledge_chunks (
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        embedding vector(1536),
                        metadata JSONB,
                        tenant_id TEXT,
                        agent_id TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                logger.info("RAG database initialized")
        except Exception as e:
            # We log but continue, as the DB might be read-only or extension already exists
            logger.error(f"Failed to initialize RAG database: {e}")

    async def _get_embeddings(self, text: str) -> List[float]:
        """Fetch embeddings from OpenAI"""
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set, returning mock embeddings")
            return [0.0] * 1536
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.openai.com/v1/embeddings",
                    headers={"Authorization": f"Bearer {self.openai_api_key}"},
                    json={"input": text, "model": "text-embedding-3-small"},
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()["data"][0]["embedding"]
            except Exception as e:
                logger.error(f"OpenAI embedding error: {e}")
                return [0.0] * 1536

    async def ingest_knowledge(self, content: str, metadata: Dict[str, Any], tenant_id: str = "global", agent_id: str = "global") -> str:
        """Store knowledge chunk with its embedding"""
        embedding = await self._get_embeddings(content)
        
        with self.Session() as session:
            try:
                result = session.execute(
                    sa.text("""
                        INSERT INTO knowledge_chunks (content, embedding, metadata, tenant_id, agent_id)
                        VALUES (:content, :embedding, :metadata, :tenant_id, :agent_id)
                        RETURNING id
                    """),
                    {
                        "content": content,
                        "embedding": str(embedding),
                        "metadata": json.dumps(metadata or {}),
                        "tenant_id": tenant_id,
                        "agent_id": agent_id
                    }
                )
                doc_id = str(result.scalar())
                session.commit()
                return doc_id
            except Exception as e:
                logger.error(f"Failed to ingest knowledge: {e}")
                session.rollback()
                return ""

    async def retrieve_context(self, query: str, agent_id: str = "global", limit: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[str]:
        """Retrieve most relevant knowledge chunks using cosine similarity and metadata filters"""
        query_embedding = await self._get_embeddings(query)
        
        filter_clause = "agent_id = :agent_id OR agent_id = 'global'"
        params = {
            "query_embedding": str(query_embedding),
            "agent_id": agent_id,
            "limit": limit
        }

        if filters:
            for key, value in filters.items():
                # Simple JSONB containment check for metadata
                filter_clause += f" AND metadata @> :{key}_filter"
                params[f"{key}_filter"] = json.dumps({key: value})
        
        with self.Session() as session:
            try:
                result = session.execute(
                    sa.text(f"""
                        SELECT content, 1 - (embedding <=> :query_embedding) as similarity
                        FROM knowledge_chunks
                        WHERE {filter_clause}
                        ORDER BY embedding <=> :query_embedding
                        LIMIT :limit
                    """),
                    params
                )
                
                return [row.content for row in result]
            except Exception as e:
                logger.error(f"Failed to retrieve context: {e}")
                return []

    async def hybrid_search(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[str]:
        """Combines Vector Search + Metadata filtering (Hybrid placeholder)"""
        # In a real hybrid search, we would also use ts_vector for full-text search
        # For now, we enhance the vector search with optional metadata filters
        return await self.retrieve_context(query, filters=filters)

    async def store_memory(self, content: str, agent_id: str, tenant_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Specific method for storing agent long-term memory (conversations, decisions)"""
        ext_metadata = metadata or {}
        ext_metadata["type"] = "memory"
        ext_metadata["timestamp"] = datetime.utcnow().isoformat()
        
        return await self.ingest_knowledge(
            content=content,
            metadata=ext_metadata,
            tenant_id=tenant_id,
            agent_id=agent_id
        )

    async def retrieve_long_term_memory(self, query: str, agent_id: str, tenant_id: str, limit: int = 10) -> List[str]:
        """Retrieve past memories relevant to the current query/context"""
        filters = {
            "type": "memory",
            "tenant_id": tenant_id
        }
        return await self.retrieve_context(
            query=query,
            agent_id=agent_id,
            limit=limit,
            filters=filters
        )

# Singleton instance
rag_service = RAGService()
