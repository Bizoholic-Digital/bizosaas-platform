"""
Hugging Face Inference API Integration for BizOSaaS Platform
Access to 1000+ open-source models for experimentation and specialized tasks

Model Categories:
- Text Generation (Llama, Mistral, Falcon, BLOOM, Zephyr)
- Code Generation (StarCoder, CodeLlama, WizardCoder)
- Embeddings (BGE, E5, Instructor)
- Image Generation (Stable Diffusion, SDXL)
- Multimodal (LLaVA, CLIP, BLIP)
- Audio (Whisper, Bark, MusicGen)
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


class HuggingFaceTextAgent:
    """AI Agent for text generation using Hugging Face models"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/models"
        self.agent_name = "Hugging Face Text Agent"

    async def generate_text(
        self,
        tenant_id: str,
        prompt: str,
        model: str = "meta-llama/Llama-2-7b-chat-hf",
        max_tokens: int = 512,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text using Hugging Face models

        Args:
            tenant_id: Tenant identifier
            prompt: Text generation prompt
            model: HF model ID (e.g., meta-llama/Llama-2-7b-chat-hf)
            max_tokens: Max response length
            temperature: Randomness (0.0-1.0)

        Returns:
            Generated text with metadata
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": kwargs.get('top_p', 0.9),
                    "do_sample": True,
                    "return_full_text": False
                }
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/{model}",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            # Extract generated text
            if isinstance(data, list) and len(data) > 0:
                generated_text = data[0].get('generated_text', '')
            else:
                generated_text = str(data)

            # Calculate costs (Hugging Face Inference API is free for basic usage)
            cost_info = self._calculate_cost(model, len(prompt), len(generated_text))

            return {
                'success': True,
                'generated_text': generated_text,
                'prompt': prompt,
                'model': model,
                'cost': cost_info,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'huggingface',
                    'open_source': True
                }
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"HuggingFace HTTP error: {e.response.status_code} - {e.response.text}")
            return {
                'success': False,
                'error': f"HTTP {e.response.status_code}: Model may be loading. Try again in 20 seconds.",
                'agent': self.agent_name,
                'fallback_recommended': 'openai'
            }
        except Exception as e:
            logger.error(f"HuggingFace text generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }

    def _calculate_cost(self, model: str, input_length: int, output_length: int) -> Dict[str, float]:
        """Calculate cost (HF Inference API has tiered pricing)"""
        # Free tier: 1000 requests/day, then rate-limited
        # Pro tier: $9/month for 5000 requests/day
        # Enterprise: Custom pricing

        return {
            'total_cost': 0.0,  # Free tier
            'tier': 'free',
            'note': 'Upgrade to Pro ($9/mo) for higher limits',
            'model_type': 'open_source',
            'self_hosting_option': True
        }


class HuggingFaceCodeAgent:
    """AI Agent for code generation using StarCoder and CodeLlama"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/models"
        self.agent_name = "Hugging Face Code Agent"

    async def generate_code(
        self,
        tenant_id: str,
        prompt: str,
        model: str = "bigcode/starcoder",
        language: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate code using specialized code models

        Args:
            tenant_id: Tenant identifier
            prompt: Code generation prompt
            model: bigcode/starcoder, codellama/CodeLlama-7b-hf, WizardLM/WizardCoder-15B-V1.0
            language: Programming language hint

        Returns:
            Generated code
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # Enhance prompt with language if specified
            enhanced_prompt = prompt
            if language:
                enhanced_prompt = f"# Language: {language}\n{prompt}"

            payload = {
                "inputs": enhanced_prompt,
                "parameters": {
                    "max_new_tokens": kwargs.get('max_tokens', 512),
                    "temperature": kwargs.get('temperature', 0.2),  # Lower temp for code
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/{model}",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            # Extract code
            if isinstance(data, list) and len(data) > 0:
                code = data[0].get('generated_text', '')
            else:
                code = str(data)

            return {
                'success': True,
                'code': code,
                'prompt': prompt,
                'language': language,
                'model': model,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'huggingface',
                    'specialized': 'code_generation'
                }
            }

        except Exception as e:
            logger.error(f"HuggingFace code generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }


class HuggingFaceEmbeddingAgent:
    """AI Agent for embeddings using BGE, E5, and other models"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/pipeline/feature-extraction"
        self.agent_name = "Hugging Face Embedding Agent"

    async def create_embeddings(
        self,
        tenant_id: str,
        texts: List[str],
        model: str = "BAAI/bge-base-en-v1.5",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create embeddings using open-source models

        Args:
            tenant_id: Tenant identifier
            texts: Text(s) to embed
            model: BAAI/bge-base-en-v1.5, intfloat/e5-base-v2, hkunlp/instructor-base

        Returns:
            Embeddings with metadata
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            embeddings = []

            for text in texts:
                payload = {
                    "inputs": text,
                    "options": {
                        "wait_for_model": True
                    }
                }

                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        f"{self.base_url}/{model}",
                        headers=headers,
                        json=payload
                    )
                    response.raise_for_status()
                    embedding = response.json()
                    embeddings.append(embedding)

            return {
                'success': True,
                'embeddings': embeddings,
                'dimension': len(embeddings[0]) if embeddings else 0,
                'count': len(embeddings),
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'model': model,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'huggingface',
                    'open_source': True
                }
            }

        except Exception as e:
            logger.error(f"HuggingFace embedding error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }


class HuggingFaceImageAgent:
    """AI Agent for image generation using Stable Diffusion"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/models"
        self.agent_name = "Hugging Face Image Agent"

    async def generate_image(
        self,
        tenant_id: str,
        prompt: str,
        model: str = "stabilityai/stable-diffusion-xl-base-1.0",
        negative_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image using Stable Diffusion models

        Args:
            tenant_id: Tenant identifier
            prompt: Image generation prompt
            model: stabilityai/stable-diffusion-xl-base-1.0, runwayml/stable-diffusion-v1-5
            negative_prompt: Things to avoid

        Returns:
            Generated image data
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }

            payload = {
                "inputs": prompt,
            }

            if negative_prompt:
                payload["negative_prompt"] = negative_prompt

            async with httpx.AsyncClient(timeout=180.0) as client:
                response = await client.post(
                    f"{self.base_url}/{model}",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()

                # Response is binary image data
                image_bytes = response.content

            return {
                'success': True,
                'image_data': image_bytes,
                'image_size': len(image_bytes),
                'prompt': prompt,
                'model': model,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'huggingface',
                    'format': 'png'
                }
            }

        except Exception as e:
            logger.error(f"HuggingFace image generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }


class HuggingFaceMultimodalAgent:
    """AI Agent for multimodal tasks (vision-language models)"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/models"
        self.agent_name = "Hugging Face Multimodal Agent"

    async def analyze_image(
        self,
        tenant_id: str,
        image_url: str,
        question: str,
        model: str = "llava-hf/llava-1.5-7b-hf",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze image with vision-language model

        Args:
            tenant_id: Tenant identifier
            image_url: URL of image to analyze
            question: Question about the image
            model: llava-hf/llava-1.5-7b-hf, Salesforce/blip-image-captioning-large

        Returns:
            Image analysis results
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "inputs": {
                    "image": image_url,
                    "question": question
                }
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/{model}",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            # Extract answer
            if isinstance(data, list) and len(data) > 0:
                answer = data[0].get('answer', '') or data[0].get('generated_text', '')
            else:
                answer = str(data)

            return {
                'success': True,
                'answer': answer,
                'question': question,
                'image_url': image_url,
                'model': model,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'huggingface',
                    'multimodal': True
                }
            }

        except Exception as e:
            logger.error(f"HuggingFace multimodal error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }


class HuggingFaceModelExplorerAgent:
    """AI Agent for discovering and exploring available models"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://huggingface.co/api"
        self.agent_name = "Hugging Face Model Explorer Agent"

    async def search_models(
        self,
        tenant_id: str,
        task: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 10,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Search for models on Hugging Face Hub

        Args:
            tenant_id: Tenant identifier
            task: Task type (text-generation, text-classification, etc.)
            search_query: Search keywords
            limit: Max results

        Returns:
            List of available models
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }

            params = {
                "limit": limit,
                "full": True
            }

            if task:
                params["filter"] = task
            if search_query:
                params["search"] = search_query

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                models = response.json()

            # Extract key information
            model_list = []
            for model in models:
                model_list.append({
                    'id': model.get('id', ''),
                    'task': model.get('pipeline_tag', 'unknown'),
                    'downloads': model.get('downloads', 0),
                    'likes': model.get('likes', 0),
                    'tags': model.get('tags', [])
                })

            return {
                'success': True,
                'models': model_list,
                'count': len(model_list),
                'task_filter': task,
                'metadata': {
                    'tenant_id': tenant_id,
                    'agent': self.agent_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'provider': 'huggingface'
                }
            }

        except Exception as e:
            logger.error(f"HuggingFace model search error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.agent_name
            }

    async def get_recommended_models(
        self,
        tenant_id: str,
        use_case: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get recommended models for specific use case

        Args:
            tenant_id: Tenant identifier
            use_case: Use case description

        Returns:
            Recommended models with explanations
        """
        # Pre-curated recommendations for common use cases
        recommendations = {
            'chat': [
                {'model': 'meta-llama/Llama-2-7b-chat-hf', 'reason': 'Balanced chat performance'},
                {'model': 'mistralai/Mistral-7B-Instruct-v0.2', 'reason': 'Fast and efficient'},
                {'model': 'tiiuae/falcon-7b-instruct', 'reason': 'Good for general tasks'}
            ],
            'code': [
                {'model': 'bigcode/starcoder', 'reason': 'Best for code generation'},
                {'model': 'codellama/CodeLlama-7b-hf', 'reason': 'Code-focused Llama'},
                {'model': 'WizardLM/WizardCoder-15B-V1.0', 'reason': 'Advanced code tasks'}
            ],
            'embeddings': [
                {'model': 'BAAI/bge-base-en-v1.5', 'reason': 'Top semantic search'},
                {'model': 'intfloat/e5-base-v2', 'reason': 'Multilingual support'},
                {'model': 'sentence-transformers/all-MiniLM-L6-v2', 'reason': 'Fast and compact'}
            ],
            'images': [
                {'model': 'stabilityai/stable-diffusion-xl-base-1.0', 'reason': 'Highest quality'},
                {'model': 'runwayml/stable-diffusion-v1-5', 'reason': 'Fast generation'},
                {'model': 'prompthero/openjourney', 'reason': 'Artistic style'}
            ]
        }

        # Find matching use case
        use_case_lower = use_case.lower()
        matched_recommendations = []

        for key, models in recommendations.items():
            if key in use_case_lower:
                matched_recommendations = models
                break

        if not matched_recommendations:
            matched_recommendations = [
                {'model': 'meta-llama/Llama-2-7b-chat-hf', 'reason': 'General purpose model'}
            ]

        return {
            'success': True,
            'use_case': use_case,
            'recommendations': matched_recommendations,
            'count': len(matched_recommendations),
            'metadata': {
                'tenant_id': tenant_id,
                'agent': self.agent_name,
                'timestamp': datetime.utcnow().isoformat()
            }
        }


class HuggingFaceAnalyticsAgent:
    """Analytics and usage tracking for Hugging Face API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agent_name = "Hugging Face Analytics Agent"

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
            Usage analytics with model insights
        """
        # Mock analytics - HF doesn't provide detailed usage API
        return {
            'success': True,
            'tenant_id': tenant_id,
            'period': {
                'start': start_date or datetime.utcnow().isoformat(),
                'end': end_date or datetime.utcnow().isoformat()
            },
            'usage': {
                'total_requests': 0,
                'total_cost': 0.0,
                'by_model_category': {
                    'text_generation': {'requests': 0, 'cost': 0.0},
                    'code_generation': {'requests': 0, 'cost': 0.0},
                    'embeddings': {'requests': 0, 'cost': 0.0},
                    'image_generation': {'requests': 0, 'cost': 0.0}
                }
            },
            'open_source_benefits': {
                'available_models': '1000+',
                'cost_savings': 'Free tier available',
                'self_hosting': True,
                'customization': True,
                'no_vendor_lock_in': True
            },
            'recommendations': [
                'Use HuggingFace for experimentation and prototyping',
                'Self-host popular models for production scale',
                'Combine with commercial APIs for fallback',
                'Upgrade to Pro tier for higher rate limits'
            ],
            'metadata': {
                'agent': self.agent_name,
                'timestamp': datetime.utcnow().isoformat()
            }
        }


class HuggingFaceInferenceIntegration:
    """Main integration class for Hugging Face Inference API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY', 'demo_key_for_testing')
        self.text_agent = HuggingFaceTextAgent(self.api_key)
        self.code_agent = HuggingFaceCodeAgent(self.api_key)
        self.embedding_agent = HuggingFaceEmbeddingAgent(self.api_key)
        self.image_agent = HuggingFaceImageAgent(self.api_key)
        self.multimodal_agent = HuggingFaceMultimodalAgent(self.api_key)
        self.model_explorer_agent = HuggingFaceModelExplorerAgent(self.api_key)
        self.analytics_agent = HuggingFaceAnalyticsAgent(self.api_key)

        logger.info("Hugging Face Inference Integration initialized - 1000+ models available")

    async def health_check(self) -> Dict[str, Any]:
        """Check Hugging Face API health"""
        try:
            # Simple model search to verify API access
            result = await self.model_explorer_agent.search_models(
                tenant_id="health_check",
                limit=1
            )

            return {
                'status': 'healthy' if result['success'] else 'unhealthy',
                'provider': 'huggingface',
                'available_models': '1000+',
                'open_source': True,
                'self_hosting': True,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'provider': 'huggingface'
            }


# Main execution for testing
async def main():
    """Test Hugging Face integration"""
    print("🤗 Initializing Hugging Face Inference API Integration\n")

    hf = HuggingFaceInferenceIntegration()

    # Health check
    print("1. Health Check...")
    health = await hf.health_check()
    print(f"Status: {health['status']}")
    print(f"Available Models: {health.get('available_models', 'N/A')}")
    print(f"Open Source: {health.get('open_source', False)}\n")

    # Model recommendations
    print("2. Model Recommendations Test...")
    recommendations = await hf.model_explorer_agent.get_recommended_models(
        tenant_id="test_tenant",
        use_case="code generation"
    )

    if recommendations['success']:
        print(f"Use Case: {recommendations['use_case']}")
        print(f"Recommendations: {recommendations['count']}")
        for rec in recommendations['recommendations'][:2]:
            print(f"  - {rec['model']}: {rec['reason']}")
        print()

    # Analytics
    print("3. Analytics...")
    analytics = await hf.analytics_agent.get_usage_analytics("test_tenant")
    print(f"Available Models: {analytics['open_source_benefits']['available_models']}")
    print(f"Self-Hosting: {analytics['open_source_benefits']['self_hosting']}")
    print(f"Cost Savings: {analytics['open_source_benefits']['cost_savings']}\n")

    print("✅ Hugging Face Inference API Integration Complete")
    print("🤗 1000+ open-source models for experimentation")
    print("💰 Free tier + self-hosting options available")


if __name__ == "__main__":
    asyncio.run(main())
