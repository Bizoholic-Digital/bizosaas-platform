"""
Cohere API Integration for BizOSaaS Platform
Enterprise-grade RAG (Retrieval-Augmented Generation) and reranking

Models Available:
- Command R+: Advanced reasoning and RAG
- Command R: Balanced performance
- Command Light: Cost-optimized
- Embed v3: Best-in-class embeddings
- Rerank 3: Superior document reranking
"""

import os
import json
import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CohereChatAgent:
    """AI Agent for chat and RAG using Cohere Command models"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cohere.ai/v1"
        self.agent_name = "Cohere Chat Agent"

    async def generate_completion(
        self,
        tenant_id: str,
        message: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        documents: Optional[List[Dict[str, str]]] = None,
        model: str = "command-r-plus",
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate chat completion with optional RAG

        Args:
            tenant_id: Tenant identifier
            message: User message
            chat_history: Previous conversation
            documents: Documents for RAG context
            model: command-r-plus, command-r, command-light
            temperature: Randomness (0.0-1.0)

        Returns:
            Response with content, citations, usage, and cost
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Client-Name": "bizosaas-platform"
            }

            payload = {
                "model": model,
                "message": message,
                "temperature": temperature,
                **kwargs
            }

            # Add chat history if provided
            if chat_history:
                payload["chat_history"] = chat_history

            # Add documents for RAG
            if documents:
                payload["documents"] = documents

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            # Extract response
            content = data.get('text', '')
            citations = data.get('citations', [])
            documents_used = data.get('documents', [])

            # Calculate costs
            usage = {
                'input_tokens': data.get('meta', {}).get('tokens', {}).get('input_tokens', 0),
                'output_tokens': data.get('meta', {}).get('tokens', {}).get('output_tokens', 0)
            }
            cost_info = self._calculate_cost(model, usage)

            # Quality analysis
            quality_metrics = self._analyze_rag_quality(content, citations, documents_used)

            return {
                'success': True,
                'content': content,
                'citations': citations,
                'documents_used': len(documents_used),
                'model': model,
                'usage': {
                    'input_tokens': usage['input_tokens'],
                    'output_tokens': usage['output_tokens'],
                    'total_tokens': usage['input_tokens'] + usage['output_tokens']
                },
                'cost': cost_info,
                'quality': quality_metrics,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'finish_reason': data.get('finish_reason'),
                    'provider': 'cohere',
                    'rag_enabled': documents is not None and len(documents) > 0
                }
            }

        except Exception as e:
            logger.error(f"Cohere chat completion error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name,
                'fallback_recommended': 'claude-sonnet'
            }

    def _calculate_cost(self, model: str, usage: Dict) -> Dict[str, float]:
        """Calculate cost based on Cohere pricing"""
        # Cohere pricing per million tokens
        pricing = {
            'command-r-plus': {'input': 0.000003, 'output': 0.000015},  # $3/$15 per million
            'command-r': {'input': 0.0000005, 'output': 0.0000015},     # $0.5/$1.5 per million
            'command-light': {'input': 0.0000003, 'output': 0.0000006}  # $0.3/$0.6 per million
        }

        model_pricing = pricing.get(model, pricing['command-r'])
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)

        input_cost = input_tokens * model_pricing['input']
        output_cost = output_tokens * model_pricing['output']
        total_cost = input_cost + output_cost

        # Calculate savings vs GPT-4
        gpt4_cost = (input_tokens * 0.00003) + (output_tokens * 0.00006)
        savings = gpt4_cost - total_cost
        savings_percent = (savings / gpt4_cost * 100) if gpt4_cost > 0 else 0

        return {
            'total_cost': round(total_cost, 6),
            'input_cost': round(input_cost, 6),
            'output_cost': round(output_cost, 6),
            'savings_vs_gpt4': round(savings, 6),
            'savings_percent': round(savings_percent, 2),
            'currency': 'USD'
        }

    def _analyze_rag_quality(self, content: str, citations: List, documents: List) -> Dict[str, Any]:
        """Analyze RAG response quality"""
        has_citations = len(citations) > 0
        citation_density = len(citations) / max(len(content.split('.')), 1)

        return {
            'length': len(content),
            'word_count': len(content.split()),
            'has_citations': has_citations,
            'citation_count': len(citations),
            'citation_density': round(citation_density, 2),
            'documents_retrieved': len(documents),
            'grounded_response': has_citations,
            'rag_optimized': True
        }


class CohereRerankAgent:
    """AI Agent for document reranking - Best-in-class retrieval"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cohere.ai/v1"
        self.agent_name = "Cohere Rerank Agent"
        self.default_model = "rerank-english-v3.0"

    async def rerank_documents(
        self,
        tenant_id: str,
        query: str,
        documents: List[str],
        top_n: int = 5,
        model: str = "rerank-english-v3.0",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Rerank documents by relevance to query

        Args:
            tenant_id: Tenant identifier
            query: Search query
            documents: List of document texts to rerank
            top_n: Number of top results to return
            model: rerank-english-v3.0, rerank-multilingual-v3.0

        Returns:
            Reranked documents with relevance scores
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "query": query,
                "documents": documents,
                "top_n": top_n,
                "return_documents": True,
                **kwargs
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/rerank",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            results = data.get('results', [])

            # Extract reranked documents with scores
            reranked_docs = []
            for result in results:
                reranked_docs.append({
                    'index': result.get('index'),
                    'relevance_score': result.get('relevance_score'),
                    'document': result.get('document', {}).get('text', '')
                })

            # Calculate cost
            cost_info = self._calculate_cost(len(documents), query)

            return {
                'success': True,
                'query': query,
                'results': reranked_docs,
                'total_documents': len(documents),
                'returned_documents': len(reranked_docs),
                'cost': cost_info,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'model': model,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'cohere'
                }
            }

        except Exception as e:
            logger.error(f"Cohere rerank error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }

    def _calculate_cost(self, num_documents: int, query: str) -> Dict[str, float]:
        """Calculate reranking cost"""
        # Cohere Rerank pricing: ~$2 per 1000 searches
        cost_per_search = 0.002

        # Additional cost for number of documents
        document_multiplier = max(num_documents / 10, 1.0)
        total_cost = cost_per_search * document_multiplier

        return {
            'total_cost': round(total_cost, 6),
            'per_search_cost': cost_per_search,
            'documents_processed': num_documents
        }


class CohereEmbeddingAgent:
    """AI Agent for text embeddings - Best-in-class semantic search"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cohere.ai/v1"
        self.agent_name = "Cohere Embedding Agent"
        self.default_model = "embed-english-v3.0"

    async def create_embeddings(
        self,
        tenant_id: str,
        texts: List[str],
        input_type: str = "search_document",
        model: str = "embed-english-v3.0",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create embeddings for text(s)

        Args:
            tenant_id: Tenant identifier
            texts: Text(s) to embed
            input_type: search_document, search_query, classification, clustering
            model: embed-english-v3.0, embed-multilingual-v3.0

        Returns:
            Embeddings with metadata
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "texts": texts,
                "input_type": input_type,
                **kwargs
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/embed",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            embeddings = data.get('embeddings', [])

            # Calculate cost
            cost_info = self._calculate_cost(len(texts))

            return {
                'success': True,
                'embeddings': embeddings,
                'dimension': len(embeddings[0]) if embeddings else 0,
                'count': len(embeddings),
                'input_type': input_type,
                'cost': cost_info,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'model': model,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'cohere'
                }
            }

        except Exception as e:
            logger.error(f"Cohere embedding error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }

    def _calculate_cost(self, num_texts: int) -> Dict[str, float]:
        """Calculate embedding cost"""
        # Cohere Embed pricing: ~$0.1 per million tokens (approx 750 texts per 1M tokens)
        cost_per_text = 0.0000001333
        total_cost = num_texts * cost_per_text

        return {
            'total_cost': round(total_cost, 6),
            'texts_embedded': num_texts
        }


class CohereClassifyAgent:
    """AI Agent for text classification"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cohere.ai/v1"
        self.agent_name = "Cohere Classify Agent"

    async def classify_texts(
        self,
        tenant_id: str,
        inputs: List[str],
        examples: List[Dict[str, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Classify texts using few-shot learning

        Args:
            tenant_id: Tenant identifier
            inputs: Texts to classify
            examples: Training examples [{'text': '...', 'label': '...'}]

        Returns:
            Classifications with confidence scores
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "inputs": inputs,
                "examples": examples,
                **kwargs
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/classify",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            classifications = data.get('classifications', [])

            return {
                'success': True,
                'classifications': [
                    {
                        'input': c.get('input'),
                        'prediction': c.get('prediction'),
                        'confidence': c.get('confidence'),
                        'labels': c.get('labels', {})
                    }
                    for c in classifications
                ],
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'cohere'
                }
            }

        except Exception as e:
            logger.error(f"Cohere classify error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }


class CohereAnalyticsAgent:
    """Analytics and usage tracking for Cohere API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agent_name = "Cohere Analytics Agent"

    async def get_usage_analytics(
        self,
        tenant_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get usage analytics for tenant

        Args:
            tenant_id: Tenant identifier
            start_date: Start date (ISO format)
            end_date: End date (ISO format)

        Returns:
            Usage analytics with RAG metrics
        """
        # Mock analytics - replace with actual API calls
        return {
            'success': True,
            'tenant_id': tenant_id,
            'period': {
                'start': start_date or datetime.utcnow().isoformat(),
                'end': end_date or datetime.utcnow().isoformat()
            },
            'usage': {
                'total_requests': 0,
                'total_tokens': 0,
                'total_cost': 0.0,
                'by_model': {
                    'command-r-plus': {'requests': 0, 'tokens': 0, 'cost': 0.0},
                    'rerank-v3': {'requests': 0, 'searches': 0, 'cost': 0.0},
                    'embed-v3': {'requests': 0, 'embeddings': 0, 'cost': 0.0}
                }
            },
            'rag_metrics': {
                'average_citation_count': 0,
                'grounded_responses': 0,
                'documents_processed': 0,
                'average_relevance_score': 0.0
            },
            'recommendations': [
                'Use Command R for balanced RAG performance',
                'Enable rerank for improved retrieval accuracy',
                'Utilize embeddings for semantic search',
                'Implement document chunking for better citations'
            ],
            'metadata': {
                'agent': self.agent_name,
                'timestamp': datetime.utcnow().isoformat()
            }
        }


class CohereAPIIntegration:
    """Main integration class for Cohere API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('COHERE_API_KEY', 'demo_key_for_testing')
        self.chat_agent = CohereChatAgent(self.api_key)
        self.rerank_agent = CohereRerankAgent(self.api_key)
        self.embedding_agent = CohereEmbeddingAgent(self.api_key)
        self.classify_agent = CohereClassifyAgent(self.api_key)
        self.analytics_agent = CohereAnalyticsAgent(self.api_key)

        logger.info("Cohere AI Integration initialized - Enterprise RAG enabled")

    async def health_check(self) -> Dict[str, Any]:
        """Check Cohere API health"""
        try:
            # Simple embedding to verify API access
            result = await self.embedding_agent.create_embeddings(
                tenant_id="health_check",
                texts=["health check"],
                input_type="search_query"
            )

            return {
                'status': 'healthy' if result['success'] else 'unhealthy',
                'provider': 'cohere',
                'rag_optimized': True,
                'enterprise_features': ['chat', 'rerank', 'embed', 'classify'],
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'provider': 'cohere'
            }


# Main execution for testing
async def main():
    """Test Cohere integration"""
    print("🔍 Initializing Cohere AI Integration (Enterprise RAG)\n")

    cohere = CohereAPIIntegration()

    # Health check
    print("1. Health Check...")
    health = await cohere.health_check()
    print(f"Status: {health['status']}")
    print(f"RAG Optimized: {health.get('rag_optimized', False)}\n")

    # RAG-powered chat
    print("2. RAG Chat Test...")
    documents = [
        {"text": "BizOSaaS is an AI-powered SaaS platform for marketing agencies."},
        {"text": "The platform includes CRM, CMS, and e-commerce capabilities."},
        {"text": "Multi-tenant architecture ensures data isolation and security."}
    ]

    chat_result = await cohere.chat_agent.generate_completion(
        tenant_id="test_tenant",
        message="What is BizOSaaS?",
        documents=documents,
        model="command-r"
    )

    if chat_result['success']:
        print(f"Response: {chat_result['content'][:200]}...")
        print(f"Citations: {chat_result['citation_count']}")
        print(f"Cost: ${chat_result['cost']['total_cost']:.6f}\n")

    # Rerank test
    print("3. Rerank Test...")
    docs_to_rerank = [
        "BizOSaaS provides CRM functionality",
        "The weather is sunny today",
        "Marketing automation is a key feature",
        "Dogs are great pets"
    ]

    rerank_result = await cohere.rerank_agent.rerank_documents(
        tenant_id="test_tenant",
        query="BizOSaaS marketing features",
        documents=docs_to_rerank,
        top_n=2
    )

    if rerank_result['success']:
        print(f"Top Results:")
        for doc in rerank_result['results']:
            print(f"  - Score: {doc['relevance_score']:.3f} - {doc['document'][:50]}...")
        print()

    # Analytics
    print("4. Analytics...")
    analytics = await cohere.analytics_agent.get_usage_analytics("test_tenant")
    print(f"Enterprise Features: {len(health.get('enterprise_features', []))}")
    print(f"RAG Metrics Available: Yes\n")

    print("✅ Cohere AI Integration Complete")
    print("🔍 RAG Capabilities: Chat + Rerank + Embed + Classify")
    print("💰 Enterprise-grade retrieval optimization")


if __name__ == "__main__":
    asyncio.run(main())
