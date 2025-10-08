"""
Elasticsearch RAG Setup for BizOSaaS Platform
Integrates Elasticsearch with Cohere for advanced RAG capabilities
"""

import asyncio
from typing import List, Dict, Any, Optional
from elasticsearch import AsyncElasticsearch
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ElasticsearchRAGManager:
    """Manages Elasticsearch for Cohere RAG integration"""

    def __init__(
        self,
        elasticsearch_url: str = "http://localhost:9200",
        index_prefix: str = "bizosaas"
    ):
        self.client = AsyncElasticsearch(elasticsearch_url)
        self.index_prefix = index_prefix
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """Initialize Elasticsearch indices for RAG"""
        await self._create_document_index()
        await self._create_conversation_index()
        await self._create_analytics_index()

    async def _create_document_index(self):
        """Create index for RAG documents"""
        index_name = f"{self.index_prefix}_documents"

        mapping = {
            "mappings": {
                "properties": {
                    "tenant_id": {"type": "keyword"},
                    "document_id": {"type": "keyword"},
                    "title": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword"}}
                    },
                    "content": {"type": "text"},
                    "metadata": {"type": "object", "enabled": True},
                    "document_type": {"type": "keyword"},
                    "source": {"type": "keyword"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"},
                    "embedding_model": {"type": "keyword"},
                    "chunk_index": {"type": "integer"},
                    "parent_document_id": {"type": "keyword"},
                    "tags": {"type": "keyword"},
                    "language": {"type": "keyword"}
                }
            },
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 1,
                "analysis": {
                    "analyzer": {
                        "default": {
                            "type": "standard"
                        }
                    }
                }
            }
        }

        try:
            if not await self.client.indices.exists(index=index_name):
                await self.client.indices.create(index=index_name, body=mapping)
                self.logger.info(f"Created index: {index_name}")
            else:
                self.logger.info(f"Index already exists: {index_name}")
        except Exception as e:
            self.logger.error(f"Error creating document index: {e}")

    async def _create_conversation_index(self):
        """Create index for conversation history"""
        index_name = f"{self.index_prefix}_conversations"

        mapping = {
            "mappings": {
                "properties": {
                    "tenant_id": {"type": "keyword"},
                    "conversation_id": {"type": "keyword"},
                    "user_id": {"type": "keyword"},
                    "message": {"type": "text"},
                    "role": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "model": {"type": "keyword"},
                    "provider": {"type": "keyword"},
                    "token_count": {"type": "integer"},
                    "cost": {"type": "float"},
                    "documents_retrieved": {"type": "integer"},
                    "rerank_score": {"type": "float"}
                }
            },
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            }
        }

        try:
            if not await self.client.indices.exists(index=index_name):
                await self.client.indices.create(index=index_name, body=mapping)
                self.logger.info(f"Created index: {index_name}")
        except Exception as e:
            self.logger.error(f"Error creating conversation index: {e}")

    async def _create_analytics_index(self):
        """Create index for RAG analytics"""
        index_name = f"{self.index_prefix}_rag_analytics"

        mapping = {
            "mappings": {
                "properties": {
                    "tenant_id": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "query": {"type": "text"},
                    "num_results": {"type": "integer"},
                    "retrieval_latency_ms": {"type": "float"},
                    "rerank_latency_ms": {"type": "float"},
                    "total_latency_ms": {"type": "float"},
                    "provider": {"type": "keyword"},
                    "success": {"type": "boolean"},
                    "error_message": {"type": "text"},
                    "top_score": {"type": "float"},
                    "avg_score": {"type": "float"}
                }
            },
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            }
        }

        try:
            if not await self.client.indices.exists(index=index_name):
                await self.client.indices.create(index=index_name, body=mapping)
                self.logger.info(f"Created index: {index_name}")
        except Exception as e:
            self.logger.error(f"Error creating analytics index: {e}")

    async def index_document(
        self,
        tenant_id: str,
        document_id: str,
        title: str,
        content: str,
        metadata: Dict[str, Any] = None,
        document_type: str = "general",
        source: str = "manual",
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """Index a document for RAG retrieval"""
        index_name = f"{self.index_prefix}_documents"

        document = {
            "tenant_id": tenant_id,
            "document_id": document_id,
            "title": title,
            "content": content,
            "metadata": metadata or {},
            "document_type": document_type,
            "source": source,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "tags": tags or [],
            "language": "en"
        }

        try:
            result = await self.client.index(
                index=index_name,
                id=document_id,
                body=document
            )

            self.logger.info(f"Indexed document: {document_id}")
            return {
                "success": True,
                "document_id": document_id,
                "result": result
            }
        except Exception as e:
            self.logger.error(f"Error indexing document: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def search_documents(
        self,
        tenant_id: str,
        query: str,
        size: int = 10,
        document_type: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Search documents using Elasticsearch"""
        index_name = f"{self.index_prefix}_documents"

        # Build query
        must_clauses = [
            {"match": {"tenant_id": tenant_id}},
            {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "content"],
                    "type": "best_fields"
                }
            }
        ]

        if document_type:
            must_clauses.append({"match": {"document_type": document_type}})

        if tags:
            must_clauses.append({"terms": {"tags": tags}})

        search_body = {
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "size": size,
            "sort": [
                {"_score": {"order": "desc"}},
                {"updated_at": {"order": "desc"}}
            ]
        }

        start_time = datetime.utcnow()

        try:
            result = await self.client.search(
                index=index_name,
                body=search_body
            )

            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000

            # Extract documents
            documents = []
            for hit in result['hits']['hits']:
                documents.append({
                    "document_id": hit['_id'],
                    "score": hit['_score'],
                    "title": hit['_source']['title'],
                    "content": hit['_source']['content'],
                    "metadata": hit['_source'].get('metadata', {}),
                    "document_type": hit['_source']['document_type']
                })

            # Log analytics
            await self._log_analytics(
                tenant_id=tenant_id,
                query=query,
                num_results=len(documents),
                retrieval_latency_ms=latency_ms,
                provider="elasticsearch",
                success=True,
                top_score=documents[0]['score'] if documents else 0.0,
                avg_score=sum(d['score'] for d in documents) / len(documents) if documents else 0.0
            )

            return {
                "success": True,
                "documents": documents,
                "total": result['hits']['total']['value'],
                "latency_ms": latency_ms
            }

        except Exception as e:
            self.logger.error(f"Error searching documents: {e}")

            await self._log_analytics(
                tenant_id=tenant_id,
                query=query,
                num_results=0,
                retrieval_latency_ms=0,
                provider="elasticsearch",
                success=False,
                error_message=str(e)
            )

            return {
                "success": False,
                "error": str(e),
                "documents": []
            }

    async def log_conversation(
        self,
        tenant_id: str,
        conversation_id: str,
        user_id: str,
        message: str,
        role: str,
        model: str,
        provider: str,
        token_count: int,
        cost: float,
        documents_retrieved: int = 0,
        rerank_score: float = 0.0
    ):
        """Log conversation for analytics"""
        index_name = f"{self.index_prefix}_conversations"

        document = {
            "tenant_id": tenant_id,
            "conversation_id": conversation_id,
            "user_id": user_id,
            "message": message,
            "role": role,
            "timestamp": datetime.utcnow().isoformat(),
            "model": model,
            "provider": provider,
            "token_count": token_count,
            "cost": cost,
            "documents_retrieved": documents_retrieved,
            "rerank_score": rerank_score
        }

        try:
            await self.client.index(index=index_name, body=document)
        except Exception as e:
            self.logger.error(f"Error logging conversation: {e}")

    async def _log_analytics(
        self,
        tenant_id: str,
        query: str,
        num_results: int,
        retrieval_latency_ms: float,
        provider: str,
        success: bool,
        rerank_latency_ms: float = 0.0,
        error_message: str = None,
        top_score: float = 0.0,
        avg_score: float = 0.0
    ):
        """Log RAG analytics"""
        index_name = f"{self.index_prefix}_rag_analytics"

        document = {
            "tenant_id": tenant_id,
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "num_results": num_results,
            "retrieval_latency_ms": retrieval_latency_ms,
            "rerank_latency_ms": rerank_latency_ms,
            "total_latency_ms": retrieval_latency_ms + rerank_latency_ms,
            "provider": provider,
            "success": success,
            "error_message": error_message,
            "top_score": top_score,
            "avg_score": avg_score
        }

        try:
            await self.client.index(index=index_name, body=document)
        except Exception as e:
            self.logger.error(f"Error logging analytics: {e}")

    async def get_analytics_summary(
        self,
        tenant_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get RAG analytics summary"""
        index_name = f"{self.index_prefix}_rag_analytics"

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"tenant_id": tenant_id}},
                        {
                            "range": {
                                "timestamp": {
                                    "gte": f"now-{days}d/d"
                                }
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "avg_latency": {"avg": {"field": "total_latency_ms"}},
                "avg_results": {"avg": {"field": "num_results"}},
                "success_rate": {
                    "terms": {"field": "success"}
                },
                "provider_breakdown": {
                    "terms": {"field": "provider"}
                }
            },
            "size": 0
        }

        try:
            result = await self.client.search(index=index_name, body=query)

            return {
                "total_queries": result['hits']['total']['value'],
                "avg_latency_ms": result['aggregations']['avg_latency']['value'],
                "avg_results": result['aggregations']['avg_results']['value'],
                "success_rate": result['aggregations']['success_rate']['buckets'],
                "provider_breakdown": result['aggregations']['provider_breakdown']['buckets']
            }
        except Exception as e:
            self.logger.error(f"Error getting analytics summary: {e}")
            return {}

    async def close(self):
        """Close Elasticsearch connection"""
        await self.client.close()


# Integration with Cohere Rerank
class CohereElasticsearchRAG:
    """Combines Elasticsearch retrieval with Cohere reranking"""

    def __init__(
        self,
        es_manager: ElasticsearchRAGManager,
        cohere_api_key: str
    ):
        self.es_manager = es_manager
        self.cohere_api_key = cohere_api_key

    async def retrieve_and_rerank(
        self,
        tenant_id: str,
        query: str,
        top_k: int = 10,
        rerank_top_n: int = 3,
        model: str = "rerank-english-v3.0"
    ) -> Dict[str, Any]:
        """Retrieve documents from Elasticsearch and rerank with Cohere"""
        import aiohttp

        # Step 1: Retrieve documents from Elasticsearch
        search_result = await self.es_manager.search_documents(
            tenant_id=tenant_id,
            query=query,
            size=top_k
        )

        if not search_result['success'] or not search_result['documents']:
            return {
                "success": False,
                "error": "No documents found",
                "documents": []
            }

        # Step 2: Rerank with Cohere
        documents_text = [doc['content'] for doc in search_result['documents']]

        rerank_start = datetime.utcnow()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.cohere.ai/v1/rerank",
                    headers={
                        "Authorization": f"Bearer {self.cohere_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "query": query,
                        "documents": documents_text,
                        "top_n": rerank_top_n,
                        "return_documents": True
                    }
                ) as response:
                    rerank_result = await response.json()
        except Exception as e:
            logger.error(f"Cohere rerank error: {e}")
            return {
                "success": False,
                "error": str(e),
                "documents": search_result['documents']
            }

        rerank_end = datetime.utcnow()
        rerank_latency_ms = (rerank_end - rerank_start).total_seconds() * 1000

        # Step 3: Combine results
        reranked_documents = []
        for item in rerank_result.get('results', []):
            original_doc = search_result['documents'][item['index']]
            reranked_documents.append({
                **original_doc,
                "rerank_score": item['relevance_score']
            })

        # Log analytics
        await self.es_manager._log_analytics(
            tenant_id=tenant_id,
            query=query,
            num_results=len(reranked_documents),
            retrieval_latency_ms=search_result['latency_ms'],
            rerank_latency_ms=rerank_latency_ms,
            provider="elasticsearch+cohere",
            success=True,
            top_score=reranked_documents[0]['rerank_score'] if reranked_documents else 0.0,
            avg_score=sum(d['rerank_score'] for d in reranked_documents) / len(reranked_documents) if reranked_documents else 0.0
        )

        return {
            "success": True,
            "documents": reranked_documents,
            "retrieval_latency_ms": search_result['latency_ms'],
            "rerank_latency_ms": rerank_latency_ms,
            "total_latency_ms": search_result['latency_ms'] + rerank_latency_ms
        }
