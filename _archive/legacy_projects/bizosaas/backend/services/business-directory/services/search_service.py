"""
AI-Powered Search Service
Handles semantic search, vector embeddings, and intelligent search capabilities
"""

from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
import asyncio
from datetime import datetime
import redis.asyncio as redis

from ..models import BusinessListing
from ..core.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class SearchService:
    """
    AI-powered search service with semantic and hybrid search capabilities
    """
    
    def __init__(self):
        self.embedding_model = None
        self.redis_client = None
        self._model_loading = False
        self._model_loaded = False
    
    async def initialize(self):
        """Initialize the search service components"""
        try:
            # Initialize Redis client
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                health_check_interval=30
            )
            
            # Load embedding model asynchronously
            await self._load_embedding_model()
            
            logger.info("Search service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize search service: {e}")
            raise
    
    async def _load_embedding_model(self):
        """Load the sentence transformer model"""
        if self._model_loading or self._model_loaded:
            return
        
        self._model_loading = True
        try:
            # Load model in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            self.embedding_model = await loop.run_in_executor(
                None,
                lambda: SentenceTransformer(settings.EMBEDDING_MODEL)
            )
            self._model_loaded = True
            logger.info(f"Loaded embedding model: {settings.EMBEDDING_MODEL}")
            
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
        finally:
            self._model_loading = False
    
    async def generate_embedding(self, business: BusinessListing) -> Optional[List[float]]:
        """Generate vector embedding for a business listing"""
        try:
            if not self._model_loaded:
                await self._load_embedding_model()
            
            if not business.search_content:
                business.update_search_content()
            
            if not business.search_content:
                logger.warning(f"No search content for business {business.id}")
                return None
            
            # Generate embedding
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None,
                lambda: self.embedding_model.encode(business.search_content).tolist()
            )
            
            # Update business with embedding
            business.search_vector = embedding
            
            # Cache embedding
            await self._cache_embedding(str(business.id), embedding)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding for business {business.id}: {e}")
            return None
    
    async def semantic_search(
        self,
        query: str,
        tenant_id: str,
        limit: int = 20,
        similarity_threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None,
        db: AsyncSession
    ) -> List[BusinessListing]:
        """Perform semantic search using vector similarity"""
        try:
            if not self._model_loaded:
                await self._load_embedding_model()
            
            # Generate query embedding
            loop = asyncio.get_event_loop()
            query_embedding = await loop.run_in_executor(
                None,
                lambda: self.embedding_model.encode(query).tolist()
            )
            
            # Set tenant context
            await db.execute(
                text("SELECT set_config('app.current_tenant_id', :tenant_id, false)"),
                {"tenant_id": tenant_id}
            )
            
            # Build semantic search query using pgvector
            similarity_query = text(f\"\"\"\n                SELECT \n                    bl.*,\n                    (bl.search_vector <=> :query_vector) as distance,\n                    (1 - (bl.search_vector <=> :query_vector)) as similarity\n                FROM business_listings bl\n                WHERE \n                    bl.tenant_id = :tenant_id\n                    AND bl.is_deleted = false\n                    AND bl.status = 'active'\n                    AND bl.search_vector IS NOT NULL\n                    AND (1 - (bl.search_vector <=> :query_vector)) >= :threshold\n                ORDER BY bl.search_vector <=> :query_vector\n                LIMIT :limit\n            \"\"\")\n            \n            result = await db.execute(similarity_query, {\n                \"query_vector\": query_embedding,\n                \"tenant_id\": tenant_id,\n                \"threshold\": similarity_threshold,\n                \"limit\": limit\n            })\n            \n            # Convert results to BusinessListing objects\n            businesses = []\n            for row in result:\n                business = BusinessListing()\n                for column in BusinessListing.__table__.columns:\n                    setattr(business, column.name, getattr(row, column.name))\n                \n                # Add similarity score as attribute\n                business.similarity_score = getattr(row, 'similarity', 0.0)\n                businesses.append(business)\n            \n            logger.info(f\"Semantic search for '{query}' returned {len(businesses)} results\")\n            return businesses\n            \n        except Exception as e:\n            logger.error(f\"Semantic search failed: {e}\")\n            return []\n    \n    async def hybrid_search(\n        self,\n        query: str,\n        tenant_id: str,\n        limit: int = 20,\n        semantic_weight: float = 0.7,\n        keyword_weight: float = 0.3,\n        filters: Optional[Dict[str, Any]] = None,\n        db: AsyncSession\n    ) -> List[BusinessListing]:\n        \"\"\"Perform hybrid search combining semantic and keyword search\"\"\"\n        try:\n            # Get semantic search results\n            semantic_results = await self.semantic_search(\n                query, tenant_id, limit * 2, db=db\n            )\n            \n            # Get keyword search results\n            keyword_results = await self.keyword_search(\n                query, tenant_id, limit * 2, db=db\n            )\n            \n            # Combine and rank results\n            combined_results = self._combine_search_results(\n                semantic_results,\n                keyword_results,\n                semantic_weight,\n                keyword_weight\n            )\n            \n            # Apply filters if provided\n            if filters:\n                combined_results = await self._apply_search_filters(\n                    combined_results, filters, db\n                )\n            \n            return combined_results[:limit]\n            \n        except Exception as e:\n            logger.error(f\"Hybrid search failed: {e}\")\n            return []\n    \n    async def keyword_search(\n        self,\n        query: str,\n        tenant_id: str,\n        limit: int = 20,\n        db: AsyncSession\n    ) -> List[BusinessListing]:\n        \"\"\"Perform keyword-based search using PostgreSQL full-text search\"\"\"\n        try:\n            # Set tenant context\n            await db.execute(\n                text(\"SELECT set_config('app.current_tenant_id', :tenant_id, false)\"),\n                {\"tenant_id\": tenant_id}\n            )\n            \n            # Prepare search terms\n            search_terms = query.lower().strip()\n            \n            # Build full-text search query\n            search_query = text(f\"\"\"\n                SELECT \n                    bl.*,\n                    ts_rank(\n                        to_tsvector('english', \n                            COALESCE(bl.name, '') || ' ' ||\n                            COALESCE(bl.description, '') || ' ' ||\n                            COALESCE(bl.short_description, '') || ' ' ||\n                            COALESCE(bl.city, '') || ' ' ||\n                            COALESCE(bl.state, '')\n                        ),\n                        plainto_tsquery('english', :search_terms)\n                    ) as rank\n                FROM business_listings bl\n                WHERE \n                    bl.tenant_id = :tenant_id\n                    AND bl.is_deleted = false\n                    AND bl.status = 'active'\n                    AND (\n                        to_tsvector('english', \n                            COALESCE(bl.name, '') || ' ' ||\n                            COALESCE(bl.description, '') || ' ' ||\n                            COALESCE(bl.short_description, '') || ' ' ||\n                            COALESCE(bl.city, '') || ' ' ||\n                            COALESCE(bl.state, '')\n                        ) @@ plainto_tsquery('english', :search_terms)\n                        OR bl.name ILIKE :fuzzy_search\n                        OR bl.city ILIKE :fuzzy_search\n                    )\n                ORDER BY rank DESC, bl.is_featured DESC, bl.rating_average DESC\n                LIMIT :limit\n            \"\"\")\n            \n            result = await db.execute(search_query, {\n                \"search_terms\": search_terms,\n                \"fuzzy_search\": f\"%{search_terms}%\",\n                \"tenant_id\": tenant_id,\n                \"limit\": limit\n            })\n            \n            # Convert results to BusinessListing objects\n            businesses = []\n            for row in result:\n                business = BusinessListing()\n                for column in BusinessListing.__table__.columns:\n                    setattr(business, column.name, getattr(row, column.name))\n                \n                # Add rank score as attribute\n                business.keyword_score = getattr(row, 'rank', 0.0)\n                businesses.append(business)\n            \n            logger.info(f\"Keyword search for '{query}' returned {len(businesses)} results\")\n            return businesses\n            \n        except Exception as e:\n            logger.error(f\"Keyword search failed: {e}\")\n            return []\n    \n    async def suggest_businesses(\n        self,\n        query: str,\n        tenant_id: str,\n        limit: int = 5,\n        db: AsyncSession\n    ) -> List[Dict[str, Any]]:\n        \"\"\"Get business suggestions for autocomplete\"\"\"\n        try:\n            # Set tenant context\n            await db.execute(\n                text(\"SELECT set_config('app.current_tenant_id', :tenant_id, false)\"),\n                {\"tenant_id\": tenant_id}\n            )\n            \n            # Build suggestion query\n            suggestion_query = text(\"\"\"\n                SELECT \n                    bl.id,\n                    bl.name,\n                    bl.city,\n                    bl.state,\n                    bl.primary_image,\n                    bl.rating_average,\n                    bl.is_verified\n                FROM business_listings bl\n                WHERE \n                    bl.tenant_id = :tenant_id\n                    AND bl.is_deleted = false\n                    AND bl.status = 'active'\n                    AND (\n                        bl.name ILIKE :search_pattern\n                        OR bl.city ILIKE :search_pattern\n                    )\n                ORDER BY \n                    bl.is_featured DESC,\n                    bl.is_verified DESC,\n                    bl.rating_average DESC,\n                    bl.name\n                LIMIT :limit\n            \"\"\")\n            \n            result = await db.execute(suggestion_query, {\n                \"search_pattern\": f\"{query}%\",\n                \"tenant_id\": tenant_id,\n                \"limit\": limit\n            })\n            \n            suggestions = []\n            for row in result:\n                suggestions.append({\n                    \"id\": str(row.id),\n                    \"name\": row.name,\n                    \"location\": f\"{row.city}, {row.state}\" if row.city and row.state else \"\",\n                    \"image\": row.primary_image,\n                    \"rating\": float(row.rating_average or 0),\n                    \"verified\": row.is_verified\n                })\n            \n            return suggestions\n            \n        except Exception as e:\n            logger.error(f\"Business suggestions failed: {e}\")\n            return []\n    \n    async def get_trending_searches(\n        self,\n        tenant_id: str,\n        limit: int = 10\n    ) -> List[str]:\n        \"\"\"Get trending search queries for a tenant\"\"\"\n        try:\n            cache_key = f\"trending_searches:{tenant_id}\"\n            \n            # Try to get from cache first\n            cached_trends = await self.redis_client.lrange(cache_key, 0, limit - 1)\n            if cached_trends:\n                return cached_trends\n            \n            # If not in cache, return default trending searches\n            default_trends = [\n                \"restaurants\",\n                \"coffee shops\",\n                \"gyms\",\n                \"beauty salons\",\n                \"auto repair\",\n                \"dentists\",\n                \"lawyers\",\n                \"plumbers\",\n                \"electricians\",\n                \"real estate\"\n            ]\n            \n            # Cache the default trends\n            await self.redis_client.lpush(cache_key, *default_trends)\n            await self.redis_client.expire(cache_key, 3600)  # 1 hour\n            \n            return default_trends[:limit]\n            \n        except Exception as e:\n            logger.error(f\"Failed to get trending searches: {e}\")\n            return []\n    \n    async def track_search_query(\n        self,\n        query: str,\n        tenant_id: str,\n        user_id: Optional[str] = None\n    ):\n        \"\"\"Track search queries for analytics and trending\"\"\"\n        try:\n            # Track in Redis for trending analysis\n            trending_key = f\"search_trends:{tenant_id}\"\n            await self.redis_client.zincrby(trending_key, 1, query.lower())\n            await self.redis_client.expire(trending_key, 86400)  # 24 hours\n            \n            # Track user search history if user is authenticated\n            if user_id:\n                history_key = f\"search_history:{user_id}\"\n                search_data = {\n                    \"query\": query,\n                    \"timestamp\": datetime.utcnow().isoformat(),\n                    \"tenant_id\": tenant_id\n                }\n                await self.redis_client.lpush(history_key, str(search_data))\n                await self.redis_client.ltrim(history_key, 0, 99)  # Keep last 100 searches\n                await self.redis_client.expire(history_key, 2592000)  # 30 days\n            \n        except Exception as e:\n            logger.error(f\"Failed to track search query: {e}\")\n    \n    # ============================================================================\n    # Helper Methods\n    # ============================================================================\n    \n    async def _cache_embedding(self, business_id: str, embedding: List[float]):\n        \"\"\"Cache business embedding in Redis\"\"\"\n        try:\n            cache_key = f\"embedding:{business_id}\"\n            embedding_str = \",\".join(map(str, embedding))\n            await self.redis_client.setex(cache_key, 3600, embedding_str)  # 1 hour\n        except Exception as e:\n            logger.warning(f\"Failed to cache embedding: {e}\")\n    \n    async def _get_cached_embedding(self, business_id: str) -> Optional[List[float]]:\n        \"\"\"Get cached business embedding from Redis\"\"\"\n        try:\n            cache_key = f\"embedding:{business_id}\"\n            embedding_str = await self.redis_client.get(cache_key)\n            if embedding_str:\n                return [float(x) for x in embedding_str.split(\",\")]\n        except Exception as e:\n            logger.warning(f\"Failed to get cached embedding: {e}\")\n        return None\n    \n    def _combine_search_results(\n        self,\n        semantic_results: List[BusinessListing],\n        keyword_results: List[BusinessListing],\n        semantic_weight: float,\n        keyword_weight: float\n    ) -> List[BusinessListing]:\n        \"\"\"Combine semantic and keyword search results with weighted scoring\"\"\"\n        business_scores = {}\n        \n        # Score semantic results\n        for i, business in enumerate(semantic_results):\n            score = getattr(business, 'similarity_score', 0.0) * semantic_weight\n            business_scores[business.id] = {\n                'business': business,\n                'score': score,\n                'rank': i + 1\n            }\n        \n        # Score keyword results\n        for i, business in enumerate(keyword_results):\n            keyword_score = getattr(business, 'keyword_score', 0.0) * keyword_weight\n            \n            if business.id in business_scores:\n                # Combine scores\n                business_scores[business.id]['score'] += keyword_score\n            else:\n                business_scores[business.id] = {\n                    'business': business,\n                    'score': keyword_score,\n                    'rank': i + 1\n                }\n        \n        # Sort by combined score\n        sorted_results = sorted(\n            business_scores.values(),\n            key=lambda x: x['score'],\n            reverse=True\n        )\n        \n        return [result['business'] for result in sorted_results]\n    \n    async def _apply_search_filters(\n        self,\n        businesses: List[BusinessListing],\n        filters: Dict[str, Any],\n        db: AsyncSession\n    ) -> List[BusinessListing]:\n        \"\"\"Apply additional filters to search results\"\"\"\n        filtered_businesses = []\n        \n        for business in businesses:\n            # Apply category filter\n            if filters.get('category_id') and business.category_id != filters['category_id']:\n                continue\n            \n            # Apply location filters\n            if filters.get('city') and business.city != filters['city']:\n                continue\n            \n            if filters.get('state') and business.state != filters['state']:\n                continue\n            \n            # Apply verification filter\n            if filters.get('is_verified') is not None and business.is_verified != filters['is_verified']:\n                continue\n            \n            # Apply rating filter\n            if filters.get('min_rating'):\n                rating = float(business.rating_average or 0)\n                if rating < filters['min_rating']:\n                    continue\n            \n            filtered_businesses.append(business)\n        \n        return filtered_businesses\n    \n    async def cleanup(self):\n        \"\"\"Cleanup search service resources\"\"\"\n        try:\n            if self.redis_client:\n                await self.redis_client.close()\n            logger.info(\"Search service cleanup completed\")\n        except Exception as e:\n            logger.error(f\"Search service cleanup error: {e}\")\n\n\n# Global search service instance\nsearch_service = SearchService()"