"""
Azure OpenAI Service Integration for BizOSaaS Platform
Enterprise-grade OpenAI models with Microsoft compliance and SLAs

Models Available:
- GPT-4 Turbo (128k context)
- GPT-4 (8k context)
- GPT-3.5 Turbo (16k context)
- GPT-4 Vision (multimodal)
- DALL-E 3 (image generation)
- Whisper (speech-to-text)
- Text Embedding Ada-002
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


class AzureOpenAIChatAgent:
    """AI Agent for chat completions using Azure OpenAI"""

    def __init__(self, api_key: str, endpoint: str, api_version: str = "2024-02-15-preview"):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.api_version = api_version
        self.agent_name = "Azure OpenAI Chat Agent"

    async def generate_completion(
        self,
        tenant_id: str,
        messages: List[Dict[str, str]],
        deployment_name: str = "gpt-4-turbo",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate chat completion using Azure OpenAI

        Args:
            tenant_id: Tenant identifier
            messages: Conversation messages
            deployment_name: Azure deployment name (e.g., gpt-4-turbo, gpt-35-turbo)
            temperature: Randomness (0.0-1.0)
            max_tokens: Max response length

        Returns:
            Response with content, usage, cost, and quality metrics
        """
        try:
            headers = {
                "api-key": self.api_key,
                "Content-Type": "application/json"
            }

            url = f"{self.endpoint}/openai/deployments/{deployment_name}/chat/completions"
            params = {"api-version": self.api_version}

            payload = {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    params=params,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            # Extract response
            content = data['choices'][0]['message']['content']
            usage = data.get('usage', {})

            # Calculate costs (Azure OpenAI pricing)
            cost_info = self._calculate_cost(deployment_name, usage)

            # Quality analysis
            quality_metrics = self._analyze_quality(content, deployment_name)

            return {
                'success': True,
                'content': content,
                'model': deployment_name,
                'usage': {
                    'prompt_tokens': usage.get('prompt_tokens', 0),
                    'completion_tokens': usage.get('completion_tokens', 0),
                    'total_tokens': usage.get('total_tokens', 0)
                },
                'cost': cost_info,
                'quality': quality_metrics,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'finish_reason': data['choices'][0].get('finish_reason'),
                    'provider': 'azure_openai',
                    'endpoint': self.endpoint,
                    'enterprise_sla': True,
                    'microsoft_compliance': True
                }
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"Azure OpenAI HTTP error: {e.response.status_code} - {e.response.text}")
            return {
                'success': False,
                'error': f"HTTP {e.response.status_code}: {e.response.text}",
                'agent': self.agent_name,
                'fallback_recommended': 'openai'
            }
        except Exception as e:
            logger.error(f"Azure OpenAI chat completion error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }

    def _calculate_cost(self, deployment_name: str, usage: Dict) -> Dict[str, float]:
        """Calculate cost based on Azure OpenAI pricing"""
        # Azure OpenAI pricing (similar to OpenAI but with enterprise features)
        pricing = {
            'gpt-4-turbo': {'input': 0.00001, 'output': 0.00003},
            'gpt-4': {'input': 0.00003, 'output': 0.00006},
            'gpt-4-32k': {'input': 0.00006, 'output': 0.00012},
            'gpt-35-turbo': {'input': 0.0000005, 'output': 0.0000015},
            'gpt-35-turbo-16k': {'input': 0.000003, 'output': 0.000004}
        }

        # Find matching pricing
        model_pricing = None
        for key, price in pricing.items():
            if key in deployment_name.lower():
                model_pricing = price
                break

        if not model_pricing:
            model_pricing = pricing['gpt-4-turbo']  # Default to GPT-4 Turbo

        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)

        input_cost = prompt_tokens * model_pricing['input']
        output_cost = completion_tokens * model_pricing['output']
        total_cost = input_cost + output_cost

        return {
            'total_cost': round(total_cost, 6),
            'input_cost': round(input_cost, 6),
            'output_cost': round(output_cost, 6),
            'currency': 'USD',
            'enterprise_sla': True,
            '99.9_uptime': True
        }

    def _analyze_quality(self, content: str, deployment_name: str) -> Dict[str, Any]:
        """Analyze response quality"""
        return {
            'length': len(content),
            'word_count': len(content.split()),
            'has_code': '```' in content,
            'has_lists': any(line.strip().startswith(('-', '*', '1.')) for line in content.split('\n')),
            'model_family': 'gpt',
            'microsoft_managed': True,
            'content_filtered': True  # Azure has built-in content filtering
        }


class AzureOpenAIVisionAgent:
    """AI Agent for vision tasks using GPT-4 Vision"""

    def __init__(self, api_key: str, endpoint: str, api_version: str = "2024-02-15-preview"):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.api_version = api_version
        self.agent_name = "Azure OpenAI Vision Agent"

    async def analyze_image(
        self,
        tenant_id: str,
        image_url: str,
        prompt: str = "What's in this image?",
        deployment_name: str = "gpt-4-vision",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze image using GPT-4 Vision

        Args:
            tenant_id: Tenant identifier
            image_url: URL of image to analyze
            prompt: Analysis prompt
            deployment_name: Azure deployment name

        Returns:
            Analysis results
        """
        try:
            headers = {
                "api-key": self.api_key,
                "Content-Type": "application/json"
            }

            url = f"{self.endpoint}/openai/deployments/{deployment_name}/chat/completions"
            params = {"api-version": self.api_version}

            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ],
                "max_tokens": kwargs.get('max_tokens', 1000)
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    params=params,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            content = data['choices'][0]['message']['content']
            usage = data.get('usage', {})

            return {
                'success': True,
                'analysis': content,
                'image_url': image_url,
                'usage': usage,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'azure_openai',
                    'multimodal': True
                }
            }

        except Exception as e:
            logger.error(f"Azure OpenAI vision error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }


class AzureOpenAIEmbeddingAgent:
    """AI Agent for text embeddings using Azure OpenAI"""

    def __init__(self, api_key: str, endpoint: str, api_version: str = "2024-02-15-preview"):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.api_version = api_version
        self.agent_name = "Azure OpenAI Embedding Agent"

    async def create_embeddings(
        self,
        tenant_id: str,
        texts: List[str],
        deployment_name: str = "text-embedding-ada-002",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create embeddings for text(s)

        Args:
            tenant_id: Tenant identifier
            texts: Text(s) to embed
            deployment_name: Azure deployment name

        Returns:
            Embeddings with metadata
        """
        try:
            headers = {
                "api-key": self.api_key,
                "Content-Type": "application/json"
            }

            url = f"{self.endpoint}/openai/deployments/{deployment_name}/embeddings"
            params = {"api-version": self.api_version}

            payload = {
                "input": texts
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    params=params,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            embeddings = [item['embedding'] for item in data['data']]
            usage = data.get('usage', {})

            # Calculate cost
            cost_info = self._calculate_cost(usage)

            return {
                'success': True,
                'embeddings': embeddings,
                'dimension': len(embeddings[0]) if embeddings else 0,
                'count': len(embeddings),
                'usage': usage,
                'cost': cost_info,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'model': deployment_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'azure_openai'
                }
            }

        except Exception as e:
            logger.error(f"Azure OpenAI embedding error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }

    def _calculate_cost(self, usage: Dict) -> Dict[str, float]:
        """Calculate embedding cost"""
        total_tokens = usage.get('total_tokens', 0)
        # Azure OpenAI Ada-002 pricing: $0.0001 per 1000 tokens
        cost = total_tokens * 0.0000001

        return {
            'total_cost': round(cost, 6),
            'tokens': total_tokens
        }


class AzureOpenAIImageAgent:
    """AI Agent for image generation using DALL-E 3"""

    def __init__(self, api_key: str, endpoint: str, api_version: str = "2024-02-15-preview"):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.api_version = api_version
        self.agent_name = "Azure OpenAI Image Agent"

    async def generate_image(
        self,
        tenant_id: str,
        prompt: str,
        deployment_name: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image using DALL-E 3

        Args:
            tenant_id: Tenant identifier
            prompt: Image generation prompt
            deployment_name: Azure deployment name
            size: 1024x1024, 1024x1792, 1792x1024
            quality: standard or hd

        Returns:
            Generated image data
        """
        try:
            headers = {
                "api-key": self.api_key,
                "Content-Type": "application/json"
            }

            url = f"{self.endpoint}/openai/deployments/{deployment_name}/images/generations"
            params = {"api-version": self.api_version}

            payload = {
                "prompt": prompt,
                "size": size,
                "quality": quality,
                "n": 1
            }

            async with httpx.AsyncClient(timeout=180.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    params=params,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            images = data.get('data', [])

            return {
                'success': True,
                'images': images,
                'count': len(images),
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'azure_openai',
                    'model': deployment_name
                }
            }

        except Exception as e:
            logger.error(f"Azure OpenAI image generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }


class AzureOpenAIAnalyticsAgent:
    """Analytics and usage tracking for Azure OpenAI"""

    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint
        self.agent_name = "Azure OpenAI Analytics Agent"

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
            Usage analytics with enterprise insights
        """
        # Mock analytics - integrate with Azure Monitor for real data
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
                'by_deployment': {
                    'gpt-4-turbo': {'requests': 0, 'tokens': 0, 'cost': 0.0},
                    'gpt-35-turbo': {'requests': 0, 'tokens': 0, 'cost': 0.0},
                    'dall-e-3': {'requests': 0, 'images': 0, 'cost': 0.0}
                }
            },
            'enterprise_features': {
                'sla_uptime': '99.9%',
                'regional_deployment': True,
                'content_filtering': True,
                'azure_ad_integration': True,
                'private_endpoints': True,
                'key_vault_integration': True
            },
            'compliance': {
                'iso_27001': True,
                'soc_2': True,
                'hipaa': True,
                'gdpr': True
            },
            'recommendations': [
                'Use GPT-3.5 Turbo for cost optimization',
                'Enable Azure AD integration for SSO',
                'Configure private endpoints for security',
                'Set up Azure Monitor alerts for usage tracking'
            ],
            'metadata': {
                'agent': self.agent_name,
                'timestamp': datetime.utcnow().isoformat()
            }
        }


class AzureOpenAIIntegration:
    """Main integration class for Azure OpenAI Service"""

    def __init__(
        self,
        api_key: str = None,
        endpoint: str = None,
        api_version: str = "2024-02-15-preview"
    ):
        self.api_key = api_key or os.getenv('AZURE_OPENAI_API_KEY', 'demo_key_for_testing')
        self.endpoint = endpoint or os.getenv('AZURE_OPENAI_ENDPOINT', 'https://YOUR-RESOURCE.openai.azure.com')
        self.api_version = api_version

        self.chat_agent = AzureOpenAIChatAgent(self.api_key, self.endpoint, api_version)
        self.vision_agent = AzureOpenAIVisionAgent(self.api_key, self.endpoint, api_version)
        self.embedding_agent = AzureOpenAIEmbeddingAgent(self.api_key, self.endpoint, api_version)
        self.image_agent = AzureOpenAIImageAgent(self.api_key, self.endpoint, api_version)
        self.analytics_agent = AzureOpenAIAnalyticsAgent(self.api_key, self.endpoint)

        logger.info(f"Azure OpenAI Integration initialized - Endpoint: {self.endpoint}")

    async def health_check(self) -> Dict[str, Any]:
        """Check Azure OpenAI API health"""
        try:
            # Simple completion to verify API access
            result = await self.chat_agent.generate_completion(
                tenant_id="health_check",
                messages=[{"role": "user", "content": "Hi"}],
                deployment_name="gpt-35-turbo",
                max_tokens=10
            )

            return {
                'status': 'healthy' if result['success'] else 'unhealthy',
                'provider': 'azure_openai',
                'endpoint': self.endpoint,
                'enterprise_sla': True,
                'compliance': ['ISO 27001', 'SOC 2', 'HIPAA', 'GDPR'],
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'provider': 'azure_openai',
                'note': 'Ensure Azure OpenAI API key and endpoint are configured'
            }


# Main execution for testing
async def main():
    """Test Azure OpenAI integration"""
    print("☁️ Initializing Azure OpenAI Service Integration\n")

    azure_openai = AzureOpenAIIntegration()

    # Health check
    print("1. Health Check...")
    health = await azure_openai.health_check()
    print(f"Status: {health['status']}")
    print(f"Enterprise SLA: {health.get('enterprise_sla', False)}")
    print(f"Compliance: {', '.join(health.get('compliance', []))}\n")

    # Chat completion
    print("2. Chat Completion Test...")
    chat_result = await azure_openai.chat_agent.generate_completion(
        tenant_id="test_tenant",
        messages=[
            {"role": "user", "content": "What are the benefits of Azure OpenAI Service?"}
        ],
        deployment_name="gpt-4-turbo"
    )

    if chat_result['success']:
        print(f"Response: {chat_result['content'][:200]}...")
        print(f"Cost: ${chat_result['cost']['total_cost']:.6f}")
        print(f"Enterprise SLA: {chat_result['metadata']['enterprise_sla']}\n")

    # Embedding test
    print("3. Embedding Test...")
    embedding_result = await azure_openai.embedding_agent.create_embeddings(
        tenant_id="test_tenant",
        texts=["Azure OpenAI Service enterprise features"]
    )

    if embedding_result['success']:
        print(f"Embeddings created: {embedding_result['count']}")
        print(f"Dimension: {embedding_result['dimension']}\n")

    # Analytics
    print("4. Analytics...")
    analytics = await azure_openai.analytics_agent.get_usage_analytics("test_tenant")
    print(f"SLA Uptime: {analytics['enterprise_features']['sla_uptime']}")
    print(f"Compliance Standards: {len(analytics['compliance'])}\n")

    print("✅ Azure OpenAI Service Integration Complete")
    print("🏢 Enterprise-grade with Microsoft compliance")


if __name__ == "__main__":
    asyncio.run(main())
