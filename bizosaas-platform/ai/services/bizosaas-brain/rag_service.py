"""
RAG (Retrieval Augmented Generation) Service
Provides semantic search and knowledge retrieval using pgvector and OpenAI embeddings
"""

import os
import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import asyncpg
import openai
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class RAGService:
    """
    RAG Service for semantic document retrieval and knowledge management
    Features:
    - Document embedding generation
    - Vector similarity search
    - Hybrid search (vector + keyword)
    - Query caching for performance
    - Self-learning feedback loop
    """

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        db_url: Optional[str] = None,
        embedding_model: str = "text-embedding-ada-002",
        embedding_dimensions: int = 1536,
        use_openrouter: bool = True,
        tenant_id: Optional[str] = None
    ):
        """
        Initialize RAG service

        Args:
            openai_api_key: OpenAI/OpenRouter API key for embeddings
            db_url: PostgreSQL connection URL
            embedding_model: Embedding model name
            embedding_dimensions: Embedding vector dimensions
            use_openrouter: Whether to use OpenRouter API (default: True)
            tenant_id: Tenant ID for retrieving tenant-specific API keys from Vault
        """
        self.use_openrouter = use_openrouter
        self.tenant_id = tenant_id

        # Get API key - check Vault first if tenant_id provided
        self.api_key = self._get_api_key(openai_api_key, tenant_id)

        self.db_url = db_url or os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:Bizoholic2024Alagiri@bizosaas-postgres-unified:5432/bizosaas"
        )
        self.embedding_model = embedding_model
        self.embedding_dimensions = embedding_dimensions

        # Initialize OpenAI-compatible client (works with OpenRouter too)
        if self.use_openrouter:
            # OpenRouter uses OpenAI-compatible API
            self.openai_client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            logger.info(f"RAG Service initialized with OpenRouter - model: {embedding_model}")
        else:
            # Direct OpenAI
            self.openai_client = AsyncOpenAI(api_key=self.api_key)
            logger.info(f"RAG Service initialized with OpenAI - model: {embedding_model}")

        # Database connection pool
        self.db_pool: Optional[asyncpg.Pool] = None

    def _get_api_key(self, provided_key: Optional[str], tenant_id: Optional[str]) -> str:
        """
        Get API key with priority: provided > tenant Vault > platform Vault > env var

        Args:
            provided_key: Directly provided API key
            tenant_id: Tenant ID for Vault lookup

        Returns:
            API key to use
        """
        # 1. Use provided key if available
        if provided_key:
            return provided_key

        # 2. Try to get tenant-specific key from Vault
        if tenant_id:
            try:
                from vault_client import get_vault_client
                vault = get_vault_client()
                tenant_secrets = vault.get_secret(f"tenants/{tenant_id}/api-keys/openrouter")
                if tenant_secrets and "api_key" in tenant_secrets:
                    logger.info(f"Using tenant-specific OpenRouter key for {tenant_id}")
                    return tenant_secrets["api_key"]
            except Exception as e:
                logger.warning(f"Could not retrieve tenant key from Vault: {e}")

        # 3. Try to get platform OpenRouter key from Vault
        try:
            from vault_client import get_vault_client
            vault = get_vault_client()
            platform_secrets = vault.get_secret("platform/openrouter-api-key")
            if platform_secrets and "api_key" in platform_secrets:
                logger.info("Using platform OpenRouter key from Vault")
                return platform_secrets["api_key"]
        except Exception as e:
            logger.warning(f"Could not retrieve platform key from Vault: {e}")

        # 4. Fallback to environment variable
        key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        if key:
            logger.info("Using API key from environment variable")
            return key

        # 5. Return placeholder (will fail at runtime but allows initialization)
        logger.warning("No API key found - using placeholder")
        return "placeholder-api-key"

    async def initialize(self):
        """Initialize database connection pool"""
        if not self.db_pool:
            self.db_pool = await asyncpg.create_pool(
                self.db_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("RAG Service database pool created")

    async def close(self):
        """Close database connections"""
        if self.db_pool:
            await self.db_pool.close()
            logger.info("RAG Service database pool closed")

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using OpenRouter/OpenAI

        Args:
            text: Input text to embed

        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Clean and prepare text
            text = text.strip()
            if not text:
                raise ValueError("Empty text provided for embedding")

            # Generate embedding with OpenRouter/OpenAI
            extra_kwargs = {}
            if self.use_openrouter:
                # OpenRouter-specific headers for better tracking
                extra_kwargs["extra_headers"] = {
                    "HTTP-Referer": "https://bizosaas.com",
                    "X-Title": "BizOSaaS RAG Service"
                }

            response = await self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text,
                **extra_kwargs
            )

            embedding = response.data[0].embedding

            logger.debug(f"Generated embedding for text length: {len(text)} using {self.embedding_model}")
            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding with {self.embedding_model}: {e}")
            raise

    async def add_document(
        self,
        document_id: str,
        content: str,
        title: Optional[str] = None,
        source: Optional[str] = None,
        source_type: Optional[str] = None,
        tenant_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add document to vector store with embedding

        Args:
            document_id: Unique document identifier
            content: Document content to embed
            title: Document title
            source: Source identifier (e.g., "crm_lead_123")
            source_type: Source type (crm, ecommerce, directory, cms)
            tenant_id: Tenant identifier for multi-tenancy
            metadata: Additional metadata as JSON

        Returns:
            Dict with document information
        """
        try:
            # Generate embedding
            embedding = await self.generate_embedding(content)

            # Store in database
            async with self.db_pool.acquire() as conn:
                result = await conn.fetchrow("""
                    INSERT INTO rag_documents (
                        document_id, title, content, content_embedding,
                        source, source_type, tenant_id, metadata
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (document_id)
                    DO UPDATE SET
                        title = EXCLUDED.title,
                        content = EXCLUDED.content,
                        content_embedding = EXCLUDED.content_embedding,
                        source = EXCLUDED.source,
                        source_type = EXCLUDED.source_type,
                        metadata = EXCLUDED.metadata,
                        updated_at = CURRENT_TIMESTAMP
                    RETURNING id, document_id, created_at, updated_at
                """, document_id, title, content, embedding, source, source_type,
                tenant_id, metadata or {})

            logger.info(f"Added document: {document_id} (source: {source_type})")

            return {
                "id": result["id"],
                "document_id": result["document_id"],
                "created_at": result["created_at"].isoformat(),
                "updated_at": result["updated_at"].isoformat(),
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error adding document {document_id}: {e}")
            raise

    async def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        tenant_id: Optional[str] = None,
        source_type: Optional[str] = None,
        min_similarity: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Semantic search using vector similarity

        Args:
            query: Search query text
            top_k: Number of results to return
            tenant_id: Filter by tenant
            source_type: Filter by source type
            min_similarity: Minimum cosine similarity threshold

        Returns:
            List of matching documents with similarity scores
        """
        try:
            # Generate query embedding
            query_embedding = await self.generate_embedding(query)

            # Build SQL query with filters
            where_clauses = []
            params = [query_embedding, top_k]
            param_count = 2

            if tenant_id:
                param_count += 1
                where_clauses.append(f"tenant_id = ${param_count}")
                params.append(tenant_id)

            if source_type:
                param_count += 1
                where_clauses.append(f"source_type = ${param_count}")
                params.append(source_type)

            where_clause = " AND " + " AND ".join(where_clauses) if where_clauses else ""

            # Perform vector similarity search
            async with self.db_pool.acquire() as conn:
                results = await conn.fetch(f"""
                    SELECT
                        document_id,
                        title,
                        content,
                        source,
                        source_type,
                        metadata,
                        1 - (content_embedding <=> $1) as similarity,
                        created_at
                    FROM rag_documents
                    WHERE 1=1 {where_clause}
                    ORDER BY content_embedding <=> $1
                    LIMIT $2
                """, *params)

            # Filter by minimum similarity and format results
            documents = []
            for row in results:
                similarity = float(row["similarity"])
                if similarity >= min_similarity:
                    documents.append({
                        "document_id": row["document_id"],
                        "title": row["title"],
                        "content": row["content"],
                        "source": row["source"],
                        "source_type": row["source_type"],
                        "metadata": row["metadata"],
                        "similarity": similarity,
                        "created_at": row["created_at"].isoformat()
                    })

            logger.info(f"Semantic search returned {len(documents)} results for query: {query[:50]}")
            return documents

        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            raise

    async def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        tenant_id: Optional[str] = None,
        source_type: Optional[str] = None,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search combining vector similarity and keyword matching

        Args:
            query: Search query
            top_k: Number of results
            tenant_id: Filter by tenant
            source_type: Filter by source type
            vector_weight: Weight for vector similarity (0-1)
            keyword_weight: Weight for keyword matching (0-1)

        Returns:
            List of documents with hybrid scores
        """
        try:
            # Get semantic search results
            semantic_results = await self.semantic_search(
                query, top_k=top_k*2, tenant_id=tenant_id,
                source_type=source_type, min_similarity=0.5
            )

            # Generate query embedding for vector search
            query_embedding = await self.generate_embedding(query)

            # Build keyword search query
            where_clauses = []
            params = [f"%{query}%"]
            param_count = 1

            if tenant_id:
                param_count += 1
                where_clauses.append(f"tenant_id = ${param_count}")
                params.append(tenant_id)

            if source_type:
                param_count += 1
                where_clauses.append(f"source_type = ${param_count}")
                params.append(source_type)

            where_clause = " AND " + " AND ".join(where_clauses) if where_clauses else ""

            # Perform keyword search
            async with self.db_pool.acquire() as conn:
                keyword_results = await conn.fetch(f"""
                    SELECT
                        document_id,
                        title,
                        content,
                        source,
                        source_type,
                        metadata,
                        created_at,
                        ts_rank(
                            to_tsvector('english', title || ' ' || content),
                            plainto_tsquery('english', $1)
                        ) as keyword_score
                    FROM rag_documents
                    WHERE (title ILIKE $1 OR content ILIKE $1) {where_clause}
                    ORDER BY keyword_score DESC
                    LIMIT {top_k*2}
                """, query, *params[1:])

            # Combine and re-rank results
            combined_scores = {}

            # Add semantic scores
            for doc in semantic_results:
                doc_id = doc["document_id"]
                combined_scores[doc_id] = {
                    "document": doc,
                    "vector_score": doc["similarity"],
                    "keyword_score": 0.0
                }

            # Add keyword scores
            for row in keyword_results:
                doc_id = row["document_id"]
                keyword_score = float(row["keyword_score"]) if row["keyword_score"] else 0.0

                if doc_id in combined_scores:
                    combined_scores[doc_id]["keyword_score"] = keyword_score
                else:
                    combined_scores[doc_id] = {
                        "document": {
                            "document_id": row["document_id"],
                            "title": row["title"],
                            "content": row["content"],
                            "source": row["source"],
                            "source_type": row["source_type"],
                            "metadata": row["metadata"],
                            "created_at": row["created_at"].isoformat()
                        },
                        "vector_score": 0.0,
                        "keyword_score": keyword_score
                    }

            # Calculate hybrid scores
            results = []
            for doc_id, scores in combined_scores.items():
                hybrid_score = (
                    vector_weight * scores["vector_score"] +
                    keyword_weight * scores["keyword_score"]
                )

                result = scores["document"].copy()
                result["hybrid_score"] = hybrid_score
                result["vector_score"] = scores["vector_score"]
                result["keyword_score"] = scores["keyword_score"]
                results.append(result)

            # Sort by hybrid score and return top_k
            results.sort(key=lambda x: x["hybrid_score"], reverse=True)
            results = results[:top_k]

            logger.info(f"Hybrid search returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Error in hybrid search: {e}")
            raise

    async def get_document_stats(self, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics about indexed documents"""
        try:
            async with self.db_pool.acquire() as conn:
                if tenant_id:
                    stats = await conn.fetchrow("""
                        SELECT
                            COUNT(*) as total_documents,
                            COUNT(DISTINCT source_type) as source_types,
                            COUNT(DISTINCT tenant_id) as tenants
                        FROM rag_documents
                        WHERE tenant_id = $1
                    """, tenant_id)
                else:
                    stats = await conn.fetchrow("""
                        SELECT
                            COUNT(*) as total_documents,
                            COUNT(DISTINCT source_type) as source_types,
                            COUNT(DISTINCT tenant_id) as tenants
                        FROM rag_documents
                    """)

                return {
                    "total_documents": stats["total_documents"],
                    "source_types": stats["source_types"],
                    "tenants": stats["tenants"]
                }
        except Exception as e:
            logger.error(f"Error getting document stats: {e}")
            raise


# Singleton instance
_rag_service: Optional[RAGService] = None

async def get_rag_service() -> RAGService:
    """Get or create RAG service singleton"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
        await _rag_service.initialize()
    return _rag_service