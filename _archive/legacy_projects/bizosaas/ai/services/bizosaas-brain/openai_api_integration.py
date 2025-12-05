#!/usr/bin/env python3
"""
OpenAI API Integration for BizOSaaS Brain - GPT Models and Advanced AI
Provides access to GPT-4, GPT-3.5, and specialized OpenAI models
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import os
from typing import Dict, List, Any, Optional
import traceback

class OpenAICompletionAgent:
    """AI Agent for GPT completions and chat interactions"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.agent_name = "OpenAI GPT Completion Agent"
        
    async def generate_completion(
        self, 
        tenant_id: str, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-3.5-turbo",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate chat completion using OpenAI GPT models"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            request_data = {
                "model": model,
                "messages": messages,
                "max_tokens": kwargs.get('max_tokens', 1500),
                "temperature": kwargs.get('temperature', 0.7),
                "top_p": kwargs.get('top_p', 1.0),
                "frequency_penalty": kwargs.get('frequency_penalty', 0),
                "presence_penalty": kwargs.get('presence_penalty', 0)
            }
            
            # Add optional parameters
            if 'stop' in kwargs:
                request_data['stop'] = kwargs['stop']
            if 'stream' in kwargs:
                request_data['stream'] = kwargs['stream']
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        choice = response_data['choices'][0] if response_data.get('choices') else {}
                        usage = response_data.get('usage', {})
                        
                        # Analyze response quality
                        quality_analysis = self._analyze_response_quality(
                            choice.get('message', {}).get('content', ''), 
                            model
                        )
                        
                        return {
                            'success': True,
                            'tenant_id': tenant_id,
                            'model': model,
                            'completion': {
                                'content': choice.get('message', {}).get('content', ''),
                                'role': choice.get('message', {}).get('role', 'assistant'),
                                'finish_reason': choice.get('finish_reason', 'stop')
                            },
                            'usage': usage,
                            'quality_analysis': quality_analysis,
                            'cost_estimate': self._calculate_cost(model, usage),
                            'agent': self.agent_name
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Completion failed: {response.status} - {error_text}',
                            'agent': self.agent_name
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': f'Completion error: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name
            }
    
    def _analyze_response_quality(self, content: str, model: str) -> Dict[str, Any]:
        """Analyze the quality of GPT response"""
        quality_metrics = {
            'coherence_score': self._assess_coherence(content),
            'informativeness': self._measure_informativeness(content),
            'creativity_level': self._evaluate_creativity(content),
            'accuracy_confidence': self._estimate_accuracy(content, model)
        }
        
        overall_quality = sum(quality_metrics.values()) / len(quality_metrics)
        
        return {
            'overall_score': round(overall_quality, 1),
            'metrics': quality_metrics,
            'quality_grade': 'A' if overall_quality >= 8.5 else 'B' if overall_quality >= 7 else 'C',
            'model_strengths': self._get_model_strengths(model)
        }
    
    def _assess_coherence(self, content: str) -> float:
        """Assess logical coherence of response"""
        coherence_indicators = {
            'logical_flow': any(word in content.lower() for word in ['therefore', 'because', 'since', 'thus']),
            'structured_thinking': any(word in content.lower() for word in ['first', 'second', 'finally', 'additionally']),
            'consistent_tone': len(set(content.lower().count(word) for word in ['i', 'you', 'we'])) <= 2,
            'appropriate_length': 50 <= len(content.split()) <= 500
        }
        
        return sum(coherence_indicators.values()) / len(coherence_indicators) * 10
    
    def _measure_informativeness(self, content: str) -> float:
        """Measure how informative the content is"""
        info_indicators = {
            'specific_details': any(char.isdigit() for char in content),
            'examples_provided': 'example' in content.lower() or 'instance' in content.lower(),
            'actionable_advice': any(word in content.lower() for word in ['should', 'can', 'might', 'consider']),
            'comprehensive': len(content.split()) >= 100
        }
        
        return sum(info_indicators.values()) / len(info_indicators) * 10
    
    def _evaluate_creativity(self, content: str) -> float:
        """Evaluate creativity level of response"""
        creativity_indicators = {
            'metaphors_analogies': any(word in content.lower() for word in ['like', 'similar to', 'imagine', 'think of']),
            'varied_vocabulary': len(set(content.lower().split())) / len(content.split()) > 0.7,
            'novel_perspectives': any(phrase in content.lower() for phrase in ['interestingly', 'surprisingly', 'uniquely']),
            'creative_solutions': any(word in content.lower() for word in ['innovative', 'creative', 'novel', 'unique'])
        }
        
        return sum(creativity_indicators.values()) / len(creativity_indicators) * 10
    
    def _estimate_accuracy(self, content: str, model: str) -> float:
        """Estimate accuracy confidence based on model and content"""
        base_confidence = {
            'gpt-4': 9.0,
            'gpt-3.5-turbo': 8.5,
            'gpt-3.5-turbo-16k': 8.5
        }.get(model, 8.0)
        
        # Adjust based on content characteristics
        if any(phrase in content.lower() for phrase in ['i think', 'possibly', 'might be', 'uncertain']):
            base_confidence -= 0.5  # Lower confidence for uncertain language
        
        if any(phrase in content.lower() for phrase in ['according to', 'research shows', 'studies indicate']):
            base_confidence += 0.3  # Higher confidence for referenced information
        
        return min(base_confidence, 10.0)
    
    def _get_model_strengths(self, model: str) -> List[str]:
        """Get known strengths of specific GPT models"""
        strengths_map = {
            'gpt-4': ['Complex reasoning', 'Code generation', 'Creative writing', 'Analysis'],
            'gpt-3.5-turbo': ['Speed', 'Cost efficiency', 'General knowledge', 'Conversational'],
            'gpt-3.5-turbo-16k': ['Extended context', 'Long documents', 'Detailed analysis']
        }
        
        return strengths_map.get(model, ['Text generation', 'Q&A', 'Summarization'])
    
    def _calculate_cost(self, model: str, usage: Dict) -> Dict[str, float]:
        """Calculate cost estimate for the completion"""
        pricing = {
            'gpt-4': {'input': 0.03, 'output': 0.06},
            'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
            'gpt-3.5-turbo-16k': {'input': 0.003, 'output': 0.004}
        }.get(model, {'input': 0.002, 'output': 0.002})
        
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        
        input_cost = prompt_tokens / 1000 * pricing['input']
        output_cost = completion_tokens / 1000 * pricing['output']
        total_cost = input_cost + output_cost
        
        return {
            'input_cost': round(input_cost, 6),
            'output_cost': round(output_cost, 6),
            'total_cost': round(total_cost, 6),
            'cost_per_token': round(total_cost / (prompt_tokens + completion_tokens), 8) if (prompt_tokens + completion_tokens) > 0 else 0
        }

class OpenAIEmbeddingAgent:
    """AI Agent for text embeddings and semantic search using OpenAI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.agent_name = "OpenAI Embedding Agent"
        
    async def generate_embeddings(
        self, 
        tenant_id: str, 
        texts: List[str], 
        model: str = "text-embedding-ada-002"
    ) -> Dict[str, Any]:
        """Generate embeddings for text using OpenAI embedding models"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            request_data = {
                "model": model,
                "input": texts
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/embeddings",
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        embeddings = [item['embedding'] for item in response_data.get('data', [])]
                        usage = response_data.get('usage', {})
                        
                        # Analyze embedding quality
                        embedding_analysis = self._analyze_embedding_quality(embeddings, texts)
                        
                        return {
                            'success': True,
                            'tenant_id': tenant_id,
                            'model': model,
                            'embeddings': {
                                'vectors': embeddings,
                                'dimensions': len(embeddings[0]) if embeddings else 0,
                                'count': len(embeddings)
                            },
                            'texts_processed': len(texts),
                            'embedding_analysis': embedding_analysis,
                            'usage': usage,
                            'cost_estimate': self._calculate_embedding_cost(model, usage),
                            'agent': self.agent_name
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Embedding generation failed: {response.status} - {error_text}',
                            'agent': self.agent_name
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': f'Embedding error: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name
            }
    
    def _analyze_embedding_quality(self, embeddings: List[List[float]], texts: List[str]) -> Dict[str, Any]:
        """Analyze quality characteristics of generated embeddings"""
        if not embeddings:
            return {'quality_score': 0, 'analysis': 'No embeddings generated'}
        
        # Calculate basic statistics
        import statistics
        
        quality_metrics = {
            'dimensionality': len(embeddings[0]),
            'consistency': self._measure_embedding_consistency(embeddings),
            'text_coverage': len(texts),
            'vector_quality': self._assess_vector_quality(embeddings)
        }
        
        overall_quality = min(quality_metrics['consistency'] * 3 + quality_metrics['vector_quality'] * 2, 10.0)
        
        return {
            'quality_score': round(overall_quality, 1),
            'metrics': quality_metrics,
            'recommendations': self._get_embedding_recommendations(quality_metrics)
        }
    
    def _measure_embedding_consistency(self, embeddings: List[List[float]]) -> float:
        """Measure consistency across embeddings"""
        if len(embeddings) < 2:
            return 8.0
        
        # Calculate average magnitude consistency
        magnitudes = [sum(x**2 for x in emb)**0.5 for emb in embeddings]
        magnitude_std = statistics.stdev(magnitudes) if len(magnitudes) > 1 else 0
        consistency = max(0, 10 - magnitude_std * 10)
        
        return min(consistency, 10.0)
    
    def _assess_vector_quality(self, embeddings: List[List[float]]) -> float:
        """Assess the quality of embedding vectors"""
        if not embeddings:
            return 0.0
        
        # Check for reasonable value ranges and non-zero vectors
        quality_score = 8.0  # Base score
        
        for emb in embeddings[:5]:  # Check first 5 embeddings
            # Check for non-zero vectors
            if all(abs(x) < 1e-6 for x in emb):
                quality_score -= 2.0
            
            # Check for reasonable value ranges (-1 to 1)
            if any(abs(x) > 2.0 for x in emb):
                quality_score -= 0.5
        
        return max(quality_score, 0.0)
    
    def _get_embedding_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations for embedding usage"""
        recommendations = []
        
        if metrics['dimensionality'] < 1000:
            recommendations.append("Consider using higher dimensional embeddings for better semantic capture")
        
        if metrics['consistency'] < 7.0:
            recommendations.append("Text preprocessing may improve embedding consistency")
        
        if metrics['text_coverage'] < 10:
            recommendations.append("Larger text corpus may improve embedding utility")
        
        return recommendations or ["Embeddings are well-suited for semantic search and clustering"]
    
    def _calculate_embedding_cost(self, model: str, usage: Dict) -> float:
        """Calculate cost for embedding generation"""
        pricing = {
            'text-embedding-ada-002': 0.0001,  # per 1K tokens
            'text-embedding-3-small': 0.00002,  # per 1K tokens  
            'text-embedding-3-large': 0.00013   # per 1K tokens
        }.get(model, 0.0001)
        
        tokens = usage.get('total_tokens', 0)
        cost = tokens / 1000 * pricing
        
        return round(cost, 6)

class OpenAIImageAgent:
    """AI Agent for image generation using DALL-E"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.agent_name = "OpenAI DALL-E Image Agent"
        
    async def generate_image(
        self, 
        tenant_id: str, 
        prompt: str, 
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> Dict[str, Any]:
        """Generate images using DALL-E models"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            request_data = {
                "model": model,
                "prompt": prompt,
                "size": size,
                "quality": quality,
                "n": n
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/images/generations",
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        images = response_data.get('data', [])
                        
                        # Analyze prompt and generation
                        generation_analysis = self._analyze_image_generation(prompt, model, images)
                        
                        return {
                            'success': True,
                            'tenant_id': tenant_id,
                            'model': model,
                            'prompt': prompt,
                            'images': {
                                'urls': [img.get('url', '') for img in images],
                                'revised_prompts': [img.get('revised_prompt', prompt) for img in images],
                                'count': len(images)
                            },
                            'generation_analysis': generation_analysis,
                            'cost_estimate': self._calculate_image_cost(model, size, quality, n),
                            'agent': self.agent_name
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Image generation failed: {response.status} - {error_text}',
                            'agent': self.agent_name
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': f'Image generation error: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name
            }
    
    def _analyze_image_generation(self, prompt: str, model: str, images: List[Dict]) -> Dict[str, Any]:
        """Analyze the image generation process and results"""
        prompt_analysis = {
            'prompt_complexity': self._assess_prompt_complexity(prompt),
            'creative_elements': self._identify_creative_elements(prompt),
            'technical_feasibility': self._assess_feasibility(prompt, model)
        }
        
        generation_quality = {
            'success_rate': len(images) > 0,
            'prompt_adherence': self._estimate_prompt_adherence(prompt, images),
            'creative_score': prompt_analysis['creative_elements']
        }
        
        return {
            'prompt_analysis': prompt_analysis,
            'generation_quality': generation_quality,
            'model_capabilities': self._get_model_capabilities(model),
            'recommendations': self._get_generation_recommendations(prompt_analysis)
        }
    
    def _assess_prompt_complexity(self, prompt: str) -> float:
        """Assess complexity of the image prompt"""
        complexity_factors = {
            'word_count': len(prompt.split()),
            'descriptive_words': len([w for w in prompt.split() if len(w) > 6]),
            'style_modifiers': len([w for w in prompt.lower().split() if w in ['photorealistic', 'artistic', 'abstract', 'detailed']]),
            'color_mentions': len([w for w in prompt.lower().split() if w in ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black', 'white']])
        }
        
        complexity_score = min(sum(complexity_factors.values()) / 20 * 10, 10)
        return round(complexity_score, 1)
    
    def _identify_creative_elements(self, prompt: str) -> float:
        """Identify creative elements in the prompt"""
        creative_indicators = {
            'artistic_style': any(word in prompt.lower() for word in ['style', 'artistic', 'painting', 'drawing']),
            'imaginative_content': any(word in prompt.lower() for word in ['fantasy', 'surreal', 'magical', 'dreamlike']),
            'unique_combinations': ',' in prompt or 'and' in prompt,
            'emotional_elements': any(word in prompt.lower() for word in ['beautiful', 'mysterious', 'dramatic', 'peaceful'])
        }
        
        return sum(creative_indicators.values()) / len(creative_indicators) * 10
    
    def _assess_feasibility(self, prompt: str, model: str) -> float:
        """Assess technical feasibility of the prompt"""
        base_feasibility = 8.0
        
        # Check for potentially problematic content
        if any(word in prompt.lower() for word in ['violent', 'explicit', 'copyrighted']):
            base_feasibility -= 3.0
        
        # DALL-E 3 is generally more capable
        if model == "dall-e-3":
            base_feasibility += 1.0
        
        return min(base_feasibility, 10.0)
    
    def _estimate_prompt_adherence(self, prompt: str, images: List[Dict]) -> float:
        """Estimate how well generated images might adhere to prompt"""
        if not images:
            return 0.0
        
        # Check for revised prompts (DALL-E 3 feature)
        has_revisions = any('revised_prompt' in img for img in images)
        adherence_estimate = 8.5 if has_revisions else 7.5
        
        return adherence_estimate
    
    def _get_model_capabilities(self, model: str) -> Dict[str, str]:
        """Get capabilities of specific DALL-E models"""
        capabilities = {
            'dall-e-3': {
                'resolution': 'Up to 1024x1024',
                'quality': 'Standard and HD options',
                'prompt_following': 'Enhanced prompt adherence',
                'safety': 'Advanced content filtering'
            },
            'dall-e-2': {
                'resolution': 'Up to 1024x1024',
                'quality': 'Standard quality',
                'variations': 'Can create variations of images',
                'editing': 'Supports inpainting and outpainting'
            }
        }
        
        return capabilities.get(model, {'capability': 'Image generation'})
    
    def _get_generation_recommendations(self, prompt_analysis: Dict) -> List[str]:
        """Generate recommendations for better image generation"""
        recommendations = []
        
        if prompt_analysis['prompt_complexity'] < 5:
            recommendations.append("Add more descriptive details for better results")
        
        if prompt_analysis['creative_elements'] < 6:
            recommendations.append("Include artistic style or mood descriptors")
        
        if prompt_analysis['technical_feasibility'] < 7:
            recommendations.append("Consider adjusting prompt to align with content policies")
        
        return recommendations or ["Prompt is well-optimized for image generation"]
    
    def _calculate_image_cost(self, model: str, size: str, quality: str, n: int) -> float:
        """Calculate cost for image generation"""
        pricing = {
            'dall-e-3': {
                '1024x1024': {'standard': 0.040, 'hd': 0.080},
                '1792x1024': {'standard': 0.080, 'hd': 0.120},
                '1024x1792': {'standard': 0.080, 'hd': 0.120}
            },
            'dall-e-2': {
                '1024x1024': {'standard': 0.020},
                '512x512': {'standard': 0.018},
                '256x256': {'standard': 0.016}
            }
        }
        
        model_pricing = pricing.get(model, {})
        size_pricing = model_pricing.get(size, {})
        unit_cost = size_pricing.get(quality, 0.040)  # Default to DALL-E 3 standard
        
        return round(unit_cost * n, 4)

class OpenAIAnalyticsAgent:
    """AI Agent for OpenAI API usage analytics and optimization"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agent_name = "OpenAI Analytics Agent"
        
    async def get_usage_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get comprehensive OpenAI API usage analytics"""
        try:
            # Simulate analytics data (in production, integrate with usage tracking)
            analytics_data = {
                'usage_summary': {
                    'total_requests': 12456,
                    'total_tokens': 3847293,
                    'total_cost': 287.43,
                    'average_cost_per_request': 0.0231,
                    'most_used_model': 'gpt-3.5-turbo',
                    'success_rate': 97.8
                },
                'model_usage': [
                    {
                        'model': 'gpt-3.5-turbo',
                        'requests': 8934,
                        'tokens': 2534823,
                        'cost': 178.95,
                        'avg_response_quality': 8.2,
                        'use_cases': ['chat', 'content generation', 'analysis']
                    },
                    {
                        'model': 'gpt-4',
                        'requests': 2156,
                        'tokens': 987462,
                        'cost': 89.67,
                        'avg_response_quality': 9.1,
                        'use_cases': ['complex reasoning', 'code generation', 'research']
                    },
                    {
                        'model': 'text-embedding-ada-002',
                        'requests': 1234,
                        'tokens': 298456,
                        'cost': 14.92,
                        'quality_score': 8.8,
                        'use_cases': ['semantic search', 'clustering', 'recommendations']
                    },
                    {
                        'model': 'dall-e-3',
                        'requests': 132,
                        'images': 156,
                        'cost': 3.89,
                        'success_rate': 94.7,
                        'use_cases': ['marketing visuals', 'product mockups', 'creative content']
                    }
                ],
                'performance_insights': {
                    'avg_response_time': '2.1s',
                    'avg_quality_score': 8.5,
                    'cost_efficiency': 'B+',
                    'optimization_potential': '18.3%'
                },
                'cost_optimization': {
                    'potential_savings': 52.74,
                    'recommendations': [
                        'Use GPT-3.5-turbo for simple tasks instead of GPT-4',
                        'Implement response caching for repeated queries',
                        'Optimize prompt length to reduce token usage',
                        'Use embedding models for semantic tasks instead of completion models'
                    ]
                }
            }
            
            return {
                'success': True,
                'tenant_id': tenant_id,
                'analytics': analytics_data,
                'optimization_score': 81.7,
                'usage_efficiency': 'good',
                'recommendations': [
                    'Current model mix is well-balanced',
                    'Consider more aggressive prompt optimization',
                    'Implement usage monitoring alerts'
                ],
                'agent': self.agent_name
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Analytics retrieval failed: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name
            }

class OpenAIAPIIntegration:
    """Main integration class for OpenAI API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY', 'demo_key_for_testing')
        self.completion_agent = OpenAICompletionAgent(self.api_key)
        self.embedding_agent = OpenAIEmbeddingAgent(self.api_key)
        self.image_agent = OpenAIImageAgent(self.api_key)
        self.analytics_agent = OpenAIAnalyticsAgent(self.api_key)
        
    async def generate_completion(
        self, 
        tenant_id: str, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-3.5-turbo",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate chat completion using GPT models"""
        return await self.completion_agent.generate_completion(tenant_id, messages, model, **kwargs)
    
    async def generate_embeddings(
        self, 
        tenant_id: str, 
        texts: List[str], 
        model: str = "text-embedding-ada-002"
    ) -> Dict[str, Any]:
        """Generate embeddings for semantic search and analysis"""
        return await self.embedding_agent.generate_embeddings(tenant_id, texts, model)
    
    async def generate_image(
        self, 
        tenant_id: str, 
        prompt: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate images using DALL-E models"""
        return await self.image_agent.generate_image(tenant_id, prompt, **kwargs)
    
    async def get_usage_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get usage analytics and optimization recommendations"""
        return await self.analytics_agent.get_usage_analytics(tenant_id)
    
    async def get_connection_status(self, tenant_id: str) -> Dict[str, Any]:
        """Get OpenAI API connection status and capabilities"""
        try:
            # Test connection with a simple completion
            test_messages = [{"role": "user", "content": "Hello"}]
            result = await self.completion_agent.generate_completion(tenant_id, test_messages, "gpt-3.5-turbo", max_tokens=10)
            
            if result['success']:
                return {
                    'status': 'connected',
                    'message': 'OpenAI API connection successful',
                    'api_type': 'GPT Models and Advanced AI',
                    'available_models': {
                        'chat_completions': ['gpt-4', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'],
                        'embeddings': ['text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large'],
                        'image_generation': ['dall-e-3', 'dall-e-2']
                    },
                    'capabilities': {
                        'chat_completions': 'Natural language conversations and text generation',
                        'text_embeddings': 'Semantic search and similarity analysis',
                        'image_generation': 'AI-powered image creation from text prompts',
                        'code_generation': 'Programming assistance and code completion',
                        'fine_tuning': 'Custom model training (available for select models)'
                    },
                    'specialties': [
                        'Natural language understanding',
                        'Creative writing and content generation', 
                        'Code analysis and generation',
                        'Mathematical reasoning',
                        'Image creation and editing',
                        'Semantic search and embeddings'
                    ]
                }
            else:
                return {
                    'status': 'connection_issues',
                    'message': f'OpenAI API connection issues: {result.get("error", "Unknown error")}',
                    'api_type': 'GPT Models and Advanced AI'
                }
                
        except Exception as e:
            return {
                'status': 'disconnected',
                'message': f'OpenAI API connection failed: {str(e)}',
                'api_type': 'GPT Models and Advanced AI'
            }

# Global integration instance
openai_api_integration = OpenAIAPIIntegration()

if __name__ == "__main__":
    print("🤖 OpenAI API Integration - GPT Models and Advanced AI")
    print("Access to GPT-4, GPT-3.5, DALL-E, and Embeddings")