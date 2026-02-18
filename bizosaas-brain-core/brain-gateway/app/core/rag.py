import os
import json
import httpx
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app.core.vault import get_config_val

logger = logging.getLogger(__name__)

class RAGService:
    """
    RAG Service for managing Knowledge Augmented Generation (KAG)
    and Vector retrieval for AI Agents using pgvector.
    """
    
    def __init__(self):
        self.db_url = get_config_val("VECTOR_DB_URL") or get_config_val("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/bizoholic"
        self.openai_api_key = get_config_val("OPENAI_API_KEY")
        self.engine = sa.create_engine(self.db_url, pool_pre_ping=True, pool_recycle=300, pool_size=5, max_overflow=10)
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
        """Fetch embeddings from configured provider (Together, OpenRouter, or OpenAI)"""
        api_key = get_config_val("TOGETHER_API_KEY") or get_config_val("OPENAI_API_KEY")
        
        if not api_key:
            logger.warning("No embedding API key set, returning mock embeddings")
            return [0.0] * 1536
            
        async with httpx.AsyncClient() as client:
            try:
                # Determine endpoint and model
                if get_config_val("TOGETHER_API_KEY"):
                    url = "https://api.together.xyz/v1/embeddings"
                    model = "togethercomputer/m2-bert-80M-8k-retrieval" # Together default
                elif api_key.startswith("sk-or-"):
                    url = "https://openrouter.ai/api/v1/embeddings"
                    model = "openai/text-embedding-3-small"
                else:
                    url = "https://api.openai.com/v1/embeddings"
                    model = "text-embedding-3-small"

                response = await client.post(
                    url,
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"input": text, "model": model},
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()["data"][0]["embedding"]
            except Exception as e:
                logger.error(f"Embedding error with {url}: {e}")
                # Fallback to local zeros with correct dimensions (1536)
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
                
                # Trigger KAG extraction via Temporal Workflow
                try:
                    from temporalio.client import Client
                    import os
                    
                    async def trigger_kag_workflow():
                        try:
                            # Connect to Temporal
                            temporal_url = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
                            namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
                            api_key = os.getenv("TEMPORAL_API_KEY")
                            
                            client = await Client.connect(
                                temporal_url,
                                namespace=namespace,
                                api_key=api_key,
                                tls=bool(api_key)
                            )
                            
                            # Execute Workflow - pass arguments as a list for positional arguments
                            await client.execute_workflow(
                                "KAGExtractionWorkflow",
                                args=[int(doc_id), content, tenant_id],
                                id=f"kag-extract-{doc_id}",
                                task_queue="brain-tasks"
                            )
                        except Exception as e:
                            logger.error(f"Failed to trigger KAG Temporal workflow: {e}")

                    # Launch as a background task to avoid blocking the API response
                    import asyncio
                    asyncio.create_task(trigger_kag_workflow())
                    
                except Exception as ke:
                    logger.warning(f"KAG extraction trigger setup failed: {ke}")
                
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
