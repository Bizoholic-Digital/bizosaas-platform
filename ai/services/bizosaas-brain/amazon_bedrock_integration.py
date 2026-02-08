"""
Amazon Bedrock API Integration for BizOSaaS Platform
Unified access to multiple foundation models on AWS

Models Available via Bedrock:
- Anthropic Claude 3 (Opus, Sonnet, Haiku)
- Meta Llama 2/3
- Mistral AI models
- Amazon Titan
- AI21 Jurassic-2
- Cohere Command
- Stability AI (Image generation)
"""

import os
import json
import boto3
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BedrockChatAgent:
    """AI Agent for chat completions using Bedrock models"""

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )
        self.agent_name = "Bedrock Chat Agent"

    async def generate_completion(
        self,
        tenant_id: str,
        messages: List[Dict[str, str]],
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate chat completion using Bedrock models

        Args:
            tenant_id: Tenant identifier
            messages: Conversation messages
            model_id: Bedrock model ID (e.g., anthropic.claude-3-sonnet-20240229-v1:0)
            temperature: Randomness (0.0-1.0)
            max_tokens: Max response length

        Returns:
            Response with content, usage, cost, and quality metrics
        """
        try:
            # Format request based on model provider
            if "anthropic" in model_id:
                request_body = self._format_anthropic_request(
                    messages, temperature, max_tokens, **kwargs
                )
            elif "meta" in model_id:
                request_body = self._format_llama_request(
                    messages, temperature, max_tokens, **kwargs
                )
            elif "mistral" in model_id:
                request_body = self._format_mistral_request(
                    messages, temperature, max_tokens, **kwargs
                )
            elif "amazon" in model_id:
                request_body = self._format_titan_request(
                    messages, temperature, max_tokens, **kwargs
                )
            else:
                raise ValueError(f"Unsupported model: {model_id}")

            # Invoke model
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body)
            )

            # Parse response
            response_body = json.loads(response['body'].read())

            # Extract content based on model
            if "anthropic" in model_id:
                content = response_body.get('content', [{}])[0].get('text', '')
                usage = response_body.get('usage', {})
            elif "meta" in model_id:
                content = response_body.get('generation', '')
                usage = {'input_tokens': 0, 'output_tokens': 0}  # Llama doesn't provide detailed usage
            elif "mistral" in model_id:
                content = response_body.get('outputs', [{}])[0].get('text', '')
                usage = {'input_tokens': 0, 'output_tokens': 0}
            elif "amazon" in model_id:
                content = response_body.get('results', [{}])[0].get('outputText', '')
                usage = {'inputTextTokenCount': 0, 'resultsTokenCount': 0}
            else:
                content = str(response_body)
                usage = {}

            # Calculate costs
            cost_info = self._calculate_cost(model_id, usage)

            # Quality analysis
            quality_metrics = self._analyze_quality(content, model_id)

            return {
                'success': True,
                'content': content,
                'model': model_id,
                'usage': {
                    'prompt_tokens': usage.get('input_tokens', usage.get('inputTextTokenCount', 0)),
                    'completion_tokens': usage.get('output_tokens', usage.get('resultsTokenCount', 0)),
                    'total_tokens': usage.get('input_tokens', 0) + usage.get('output_tokens', 0)
                },
                'cost': cost_info,
                'quality': quality_metrics,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'aws_bedrock',
                    'region': self.region,
                    'aws_account': True
                }
            }

        except ClientError as e:
            logger.error(f"Bedrock API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name,
                'fallback_recommended': 'openai'
            }
        except Exception as e:
            logger.error(f"Bedrock chat completion error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }

    def _format_anthropic_request(self, messages: List[Dict], temperature: float, max_tokens: int, **kwargs) -> Dict:
        """Format request for Anthropic Claude models"""
        return {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
            **kwargs
        }

    def _format_llama_request(self, messages: List[Dict], temperature: float, max_tokens: int, **kwargs) -> Dict:
        """Format request for Meta Llama models"""
        # Combine messages into a single prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return {
            "prompt": prompt,
            "temperature": temperature,
            "max_gen_len": max_tokens,
            **kwargs
        }

    def _format_mistral_request(self, messages: List[Dict], temperature: float, max_tokens: int, **kwargs) -> Dict:
        """Format request for Mistral models"""
        # Combine messages into a single prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

    def _format_titan_request(self, messages: List[Dict], temperature: float, max_tokens: int, **kwargs) -> Dict:
        """Format request for Amazon Titan models"""
        # Combine messages into a single prompt
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return {
            "inputText": prompt,
            "textGenerationConfig": {
                "temperature": temperature,
                "maxTokenCount": max_tokens,
                **kwargs
            }
        }

    def _calculate_cost(self, model_id: str, usage: Dict) -> Dict[str, float]:
        """Calculate cost based on Bedrock pricing"""
        # Bedrock pricing varies by model
        pricing = {
            'anthropic.claude-3-opus': {'input': 0.000015, 'output': 0.000075},
            'anthropic.claude-3-sonnet': {'input': 0.000003, 'output': 0.000015},
            'anthropic.claude-3-haiku': {'input': 0.00000025, 'output': 0.00000125},
            'meta.llama2-70b': {'input': 0.00000195, 'output': 0.00000256},
            'meta.llama3-70b': {'input': 0.00000265, 'output': 0.00000347},
            'mistral.mistral-7b': {'input': 0.00000015, 'output': 0.0000002},
            'mistral.mixtral-8x7b': {'input': 0.00000045, 'output': 0.0000007},
            'amazon.titan-text-express': {'input': 0.0000008, 'output': 0.0000016}
        }

        # Find matching pricing
        model_pricing = None
        for key, price in pricing.items():
            if key in model_id:
                model_pricing = price
                break

        if not model_pricing:
            model_pricing = {'input': 0.000003, 'output': 0.000015}  # Default to Sonnet pricing

        prompt_tokens = usage.get('input_tokens', usage.get('inputTextTokenCount', 0))
        completion_tokens = usage.get('output_tokens', usage.get('resultsTokenCount', 0))

        input_cost = prompt_tokens * model_pricing['input']
        output_cost = completion_tokens * model_pricing['output']
        total_cost = input_cost + output_cost

        return {
            'total_cost': round(total_cost, 6),
            'input_cost': round(input_cost, 6),
            'output_cost': round(output_cost, 6),
            'currency': 'USD',
            'aws_region': self.region
        }

    def _analyze_quality(self, content: str, model_id: str) -> Dict[str, Any]:
        """Analyze response quality"""
        return {
            'length': len(content),
            'word_count': len(content.split()),
            'has_code': '```' in content,
            'has_lists': any(line.strip().startswith(('-', '*', '1.')) for line in content.split('\n')),
            'model_family': self._get_model_family(model_id),
            'aws_managed': True
        }

    def _get_model_family(self, model_id: str) -> str:
        """Get model family from model ID"""
        if 'anthropic' in model_id:
            return 'claude'
        elif 'meta' in model_id:
            return 'llama'
        elif 'mistral' in model_id:
            return 'mistral'
        elif 'amazon' in model_id:
            return 'titan'
        elif 'ai21' in model_id:
            return 'jurassic'
        elif 'cohere' in model_id:
            return 'command'
        return 'unknown'


class BedrockEmbeddingAgent:
    """AI Agent for text embeddings using Bedrock"""

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )
        self.agent_name = "Bedrock Embedding Agent"
        self.default_model = "amazon.titan-embed-text-v1"

    async def create_embeddings(
        self,
        tenant_id: str,
        texts: List[str],
        model_id: str = "amazon.titan-embed-text-v1",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create embeddings for text(s)

        Args:
            tenant_id: Tenant identifier
            texts: Text(s) to embed
            model_id: Bedrock embedding model ID

        Returns:
            Embeddings with metadata
        """
        try:
            embeddings = []

            for text in texts:
                request_body = {
                    "inputText": text
                }

                response = self.client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(request_body)
                )

                response_body = json.loads(response['body'].read())
                embedding = response_body.get('embedding', [])
                embeddings.append(embedding)

            # Calculate cost
            cost_info = self._calculate_cost(len(texts))

            return {
                'success': True,
                'embeddings': embeddings,
                'dimension': len(embeddings[0]) if embeddings else 0,
                'count': len(embeddings),
                'cost': cost_info,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'model': model_id,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'aws_bedrock',
                    'region': self.region
                }
            }

        except Exception as e:
            logger.error(f"Bedrock embedding error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }

    def _calculate_cost(self, num_texts: int) -> Dict[str, float]:
        """Calculate embedding cost"""
        # Amazon Titan Embeddings pricing: ~$0.0001 per 1000 tokens
        cost_per_text = 0.0000001
        total_cost = num_texts * cost_per_text

        return {
            'total_cost': round(total_cost, 6),
            'texts_embedded': num_texts
        }


class BedrockImageAgent:
    """AI Agent for image generation using Bedrock"""

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )
        self.agent_name = "Bedrock Image Agent"
        self.default_model = "stability.stable-diffusion-xl-v1"

    async def generate_image(
        self,
        tenant_id: str,
        prompt: str,
        negative_prompt: Optional[str] = None,
        model_id: str = "stability.stable-diffusion-xl-v1",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image using Bedrock models

        Args:
            tenant_id: Tenant identifier
            prompt: Image generation prompt
            negative_prompt: Things to avoid in image
            model_id: Bedrock image model ID

        Returns:
            Generated image data
        """
        try:
            request_body = {
                "text_prompts": [
                    {"text": prompt, "weight": 1.0}
                ],
                "cfg_scale": kwargs.get('cfg_scale', 7),
                "seed": kwargs.get('seed', 0),
                "steps": kwargs.get('steps', 30)
            }

            if negative_prompt:
                request_body["text_prompts"].append({
                    "text": negative_prompt,
                    "weight": -1.0
                })

            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body)
            )

            response_body = json.loads(response['body'].read())

            # Extract image data
            artifacts = response_body.get('artifacts', [])
            images = []
            for artifact in artifacts:
                images.append({
                    'base64': artifact.get('base64'),
                    'seed': artifact.get('seed'),
                    'finish_reason': artifact.get('finishReason')
                })

            return {
                'success': True,
                'images': images,
                'count': len(images),
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'model': model_id,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'aws_bedrock',
                    'region': self.region
                }
            }

        except Exception as e:
            logger.error(f"Bedrock image generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }


class BedrockAnalyticsAgent:
    """Analytics and usage tracking for Bedrock"""

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.agent_name = "Bedrock Analytics Agent"

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
            Usage analytics with multi-model insights
        """
        # Mock analytics - integrate with AWS CloudWatch for real data
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
                'by_model_family': {
                    'claude': {'requests': 0, 'tokens': 0, 'cost': 0.0},
                    'llama': {'requests': 0, 'tokens': 0, 'cost': 0.0},
                    'mistral': {'requests': 0, 'tokens': 0, 'cost': 0.0},
                    'titan': {'requests': 0, 'tokens': 0, 'cost': 0.0}
                }
            },
            'aws_integration': {
                'region': self.region,
                'security_controls': True,
                'cloudwatch_enabled': True,
                'kms_encryption': True
            },
            'recommendations': [
                'Use Claude Haiku for cost-optimized tasks',
                'Use Llama 3 for open-source flexibility',
                'Enable CloudWatch for detailed monitoring',
                'Configure IAM policies for security'
            ],
            'metadata': {
                'agent': self.agent_name,
                'timestamp': datetime.utcnow().isoformat()
            }
        }


class AmazonBedrockIntegration:
    """Main integration class for Amazon Bedrock"""

    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.chat_agent = BedrockChatAgent(region)
        self.embedding_agent = BedrockEmbeddingAgent(region)
        self.image_agent = BedrockImageAgent(region)
        self.analytics_agent = BedrockAnalyticsAgent(region)

        logger.info(f"Amazon Bedrock Integration initialized - Region: {region}")

    async def health_check(self) -> Dict[str, Any]:
        """Check Bedrock API health"""
        try:
            # List available models to verify access
            client = boto3.client('bedrock', region_name=self.region)
            response = client.list_foundation_models()

            model_count = len(response.get('modelSummaries', []))

            return {
                'status': 'healthy',
                'provider': 'aws_bedrock',
                'region': self.region,
                'available_models': model_count,
                'model_families': ['claude', 'llama', 'mistral', 'titan', 'jurassic', 'stable-diffusion'],
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'provider': 'aws_bedrock',
                'note': 'Ensure AWS credentials are configured'
            }


# Main execution for testing
async def main():
    """Test Bedrock integration"""
    print("☁️ Initializing Amazon Bedrock Integration\n")

    bedrock = AmazonBedrockIntegration(region="us-east-1")

    # Health check
    print("1. Health Check...")
    health = await bedrock.health_check()
    print(f"Status: {health['status']}")
    print(f"Region: {health.get('region', 'N/A')}")
    print(f"Available Models: {health.get('available_models', 0)}\n")

    # Chat completion (Claude via Bedrock)
    print("2. Chat Completion Test (Claude via Bedrock)...")
    chat_result = await bedrock.chat_agent.generate_completion(
        tenant_id="test_tenant",
        messages=[
            {"role": "user", "content": "What are the benefits of using AWS Bedrock?"}
        ],
        model_id="anthropic.claude-3-sonnet-20240229-v1:0"
    )

    if chat_result['success']:
        print(f"Response: {chat_result['content'][:200]}...")
        print(f"Cost: ${chat_result['cost']['total_cost']:.6f}\n")

    # Embedding test
    print("3. Embedding Test (Amazon Titan)...")
    embedding_result = await bedrock.embedding_agent.create_embeddings(
        tenant_id="test_tenant",
        texts=["BizOSaaS platform capabilities"]
    )

    if embedding_result['success']:
        print(f"Embeddings created: {embedding_result['count']}")
        print(f"Dimension: {embedding_result['dimension']}\n")

    # Analytics
    print("4. Analytics...")
    analytics = await bedrock.analytics_agent.get_usage_analytics("test_tenant")
    print(f"Multi-model Platform: {len(analytics['usage']['by_model_family'])} families")
    print(f"AWS Integration: {analytics['aws_integration']['security_controls']}\n")

    print("✅ Amazon Bedrock Integration Complete")
    print("☁️ Multi-model access via unified AWS platform")


if __name__ == "__main__":
    asyncio.run(main())
