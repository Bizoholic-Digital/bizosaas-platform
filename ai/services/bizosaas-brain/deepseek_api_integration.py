#!/usr/bin/env python3
"""
DeepSeek API Integration for BizOSaaS Brain - Cost-Optimized AI at Scale
DeepSeek-V3 (671B parameters, MoE architecture) with R1 reasoning model

Key Features:
- OpenAI-compatible API format (drop-in replacement)
- ~$0.55 per million tokens (40-60% cost savings vs GPT-4)
- 671B total parameters, 37B active per request (MoE efficiency)
- Competitive performance with GPT-4 Turbo
- Complex reasoning with DeepSeek-R1

Models:
- deepseek-chat: General chat and text generation (V3)
- deepseek-reasoner: Advanced reasoning tasks (R1)
- deepseek-coder: Code generation and analysis
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import os
from typing import Dict, List, Any, Optional
import traceback
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekChatAgent:
    """AI Agent for chat completions using DeepSeek models"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.agent_name = "DeepSeek Chat Agent"

    async def generate_completion(
        self,
        tenant_id: str,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate chat completion using DeepSeek models

        Args:
            tenant_id: Tenant identifier
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (deepseek-chat, deepseek-reasoner, deepseek-coder)
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            request_data = {
                "model": model,
                "messages": messages,
                "max_tokens": kwargs.get('max_tokens', 2048),
                "temperature": kwargs.get('temperature', 0.7),
                "top_p": kwargs.get('top_p', 1.0),
                "frequency_penalty": kwargs.get('frequency_penalty', 0),
                "presence_penalty": kwargs.get('presence_penalty', 0),
                "stream": kwargs.get('stream', False)
            }

            # Add optional parameters
            if 'stop' in kwargs:
                request_data['stop'] = kwargs['stop']

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

                        # Calculate cost (DeepSeek pricing)
                        cost_estimate = self._calculate_cost(model, usage)

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
                            'cost_estimate': cost_estimate,
                            'agent': self.agent_name,
                            'provider': 'DeepSeek'
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'DeepSeek completion failed: {response.status} - {error_text}',
                            'agent': self.agent_name,
                            'provider': 'DeepSeek'
                        }

        except Exception as e:
            logger.error(f"DeepSeek completion error: {str(e)}")
            return {
                'success': False,
                'error': f'DeepSeek error: {str(e)}',
                'traceback': traceback.format_exc(),
                'agent': self.agent_name,
                'provider': 'DeepSeek'
            }

    def _analyze_response_quality(self, content: str, model: str) -> Dict[str, Any]:
        """Analyze the quality of DeepSeek response"""
        quality_metrics = {
            'coherence_score': self._assess_coherence(content),
            'informativeness': self._measure_informativeness(content),
            'reasoning_depth': self._evaluate_reasoning(content, model),
            'efficiency_score': self._calculate_efficiency(content, model)
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

    def _evaluate_reasoning(self, content: str, model: str) -> float:
        """Evaluate reasoning capabilities (higher for R1 model)"""
        reasoning_indicators = {
            'step_by_step': 'step' in content.lower() or 'first' in content.lower(),
            'cause_effect': 'because' in content.lower() or 'therefore' in content.lower(),
            'analysis': any(word in content.lower() for word in ['analyze', 'consider', 'evaluate']),
            'conclusion': 'conclusion' in content.lower() or 'summary' in content.lower()
        }

        base_score = sum(reasoning_indicators.values()) / len(reasoning_indicators) * 10

        # Bonus for R1 model (specialized reasoning)
        if 'reasoner' in model:
            base_score = min(base_score + 1.0, 10.0)

        return base_score

    def _calculate_efficiency(self, content: str, model: str) -> float:
        """Calculate efficiency score (MoE architecture benefit)"""
        # DeepSeek uses 37B active params out of 671B total (efficient)
        word_count = len(content.split())

        # Efficient if provides good content without excessive tokens
        if 100 <= word_count <= 400:
            return 9.5
        elif 50 <= word_count <= 600:
            return 8.5
        else:
            return 7.0

    def _get_model_strengths(self, model: str) -> List[str]:
        """Get known strengths of specific DeepSeek models"""
        strengths_map = {
            'deepseek-chat': ['Cost efficiency', 'General knowledge', 'Fast responses', 'MoE architecture'],
            'deepseek-reasoner': ['Advanced reasoning', 'Complex problem solving', 'Step-by-step analysis', 'Logic chains'],
            'deepseek-coder': ['Code generation', 'Code analysis', 'Bug detection', 'Refactoring']
        }

        return strengths_map.get(model, ['Text generation', 'Q&A', 'Cost optimization'])

    def _calculate_cost(self, model: str, usage: Dict) -> Dict[str, float]:
        """
        Calculate cost estimate for DeepSeek completion

        DeepSeek Pricing (as of 2025):
        - deepseek-chat: $0.27 input / $1.10 output per 1M tokens
        - deepseek-reasoner: $0.55 input / $2.19 output per 1M tokens
        - deepseek-coder: $0.27 input / $1.10 output per 1M tokens
        """
        pricing = {
            'deepseek-chat': {'input': 0.00000027, 'output': 0.0000011},
            'deepseek-reasoner': {'input': 0.00000055, 'output': 0.00000219},
            'deepseek-coder': {'input': 0.00000027, 'output': 0.0000011}
        }.get(model, {'input': 0.00000027, 'output': 0.0000011})

        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)

        input_cost = prompt_tokens * pricing['input']
        output_cost = completion_tokens * pricing['output']
        total_cost = input_cost + output_cost

        # Calculate savings vs GPT-4 ($0.03 input / $0.06 output)
        gpt4_cost = (prompt_tokens * 0.00003) + (completion_tokens * 0.00006)
        savings = gpt4_cost - total_cost
        savings_percent = (savings / gpt4_cost * 100) if gpt4_cost > 0 else 0

        return {
            'input_cost': round(input_cost, 6),
            'output_cost': round(output_cost, 6),
            'total_cost': round(total_cost, 6),
            'cost_per_token': round(total_cost / (prompt_tokens + completion_tokens), 8) if (prompt_tokens + completion_tokens) > 0 else 0,
            'savings_vs_gpt4': round(savings, 6),
            'savings_percent': round(savings_percent, 1)
        }


class DeepSeekReasoningAgent:
    """AI Agent for advanced reasoning using DeepSeek R1 model"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.agent_name = "DeepSeek Reasoning Agent (R1)"
        self.chat_agent = DeepSeekChatAgent(api_key)

    async def solve_complex_problem(
        self,
        tenant_id: str,
        problem: str,
        context: str = "",
        reasoning_steps: int = 5
    ) -> Dict[str, Any]:
        """
        Solve complex problems using DeepSeek R1 reasoning model

        Args:
            tenant_id: Tenant identifier
            problem: Problem to solve
            context: Additional context
            reasoning_steps: Number of reasoning steps to use
        """

        # Construct reasoning prompt
        reasoning_prompt = f"""You are an advanced reasoning AI. Solve this problem step-by-step using {reasoning_steps} clear reasoning steps.

Problem: {problem}

Context: {context}

Please provide:
1. Problem analysis and understanding
2. Step-by-step reasoning process
3. Multiple approaches if applicable
4. Verification of solution
5. Final answer with confidence level

Use clear, logical reasoning at each step."""

        messages = [
            {"role": "user", "content": reasoning_prompt}
        ]

        # Use DeepSeek-Reasoner model
        result = await self.chat_agent.generate_completion(
            tenant_id=tenant_id,
            messages=messages,
            model="deepseek-reasoner",
            temperature=0.2,  # Lower temperature for reasoning
            max_tokens=3000   # More tokens for detailed reasoning
        )

        if result['success']:
            result['reasoning_type'] = 'advanced'
            result['reasoning_steps_requested'] = reasoning_steps

        return result


class DeepSeekCoderAgent:
    """AI Agent for code generation and analysis using DeepSeek Coder"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.agent_name = "DeepSeek Coder Agent"
        self.chat_agent = DeepSeekChatAgent(api_key)

    async def generate_code(
        self,
        tenant_id: str,
        task: str,
        language: str = "python",
        include_tests: bool = True
    ) -> Dict[str, Any]:
        """
        Generate code using DeepSeek Coder model

        Args:
            tenant_id: Tenant identifier
            task: Code generation task
            language: Programming language
            include_tests: Whether to include unit tests
        """

        code_prompt = f"""Generate {language} code for the following task:

Task: {task}

Requirements:
- Write clean, efficient, well-documented code
- Follow {language} best practices and conventions
- Include type hints and docstrings
{'- Include unit tests' if include_tests else ''}

Please provide the complete implementation."""

        messages = [
            {"role": "user", "content": code_prompt}
        ]

        result = await self.chat_agent.generate_completion(
            tenant_id=tenant_id,
            messages=messages,
            model="deepseek-coder",
            temperature=0.3,
            max_tokens=2048
        )

        if result['success']:
            result['code_language'] = language
            result['includes_tests'] = include_tests

        return result


class DeepSeekAnalyticsAgent:
    """AI Agent for DeepSeek API usage analytics and cost optimization"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agent_name = "DeepSeek Analytics Agent"

    async def get_usage_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get comprehensive DeepSeek API usage analytics with cost comparison"""
        try:
            # Simulate analytics data (in production, integrate with usage tracking)
            analytics_data = {
                'usage_summary': {
                    'total_requests': 15234,
                    'total_tokens': 4823947,
                    'total_cost': 68.45,
                    'average_cost_per_request': 0.00449,
                    'most_used_model': 'deepseek-chat',
                    'success_rate': 99.1
                },
                'model_usage': [
                    {
                        'model': 'deepseek-chat',
                        'requests': 11234,
                        'tokens': 3456789,
                        'cost': 45.23,
                        'avg_response_quality': 8.4,
                        'use_cases': ['general chat', 'content generation', 'Q&A']
                    },
                    {
                        'model': 'deepseek-reasoner',
                        'requests': 2890,
                        'tokens': 987654,
                        'cost': 18.67,
                        'avg_response_quality': 9.1,
                        'use_cases': ['complex reasoning', 'problem solving', 'analysis']
                    },
                    {
                        'model': 'deepseek-coder',
                        'requests': 1110,
                        'tokens': 379504,
                        'cost': 4.55,
                        'avg_response_quality': 8.8,
                        'use_cases': ['code generation', 'debugging', 'refactoring']
                    }
                ],
                'performance_insights': {
                    'avg_response_time': '1.1s',
                    'avg_quality_score': 8.6,
                    'cost_efficiency': 'A+',
                    'moe_efficiency': '94.3%'  # MoE architecture efficiency
                },
                'cost_comparison': {
                    'deepseek_cost': 68.45,
                    'gpt4_equivalent_cost': 287.43,
                    'claude_equivalent_cost': 234.56,
                    'total_savings': 218.98,
                    'savings_percent': 76.2,
                    'roi': 'Excellent'
                },
                'cost_optimization': {
                    'current_efficiency': 94.3,
                    'potential_additional_savings': 8.45,
                    'recommendations': [
                        'Already using most cost-effective model selection',
                        'Consider batching requests for better efficiency',
                        'Current usage pattern is optimized for DeepSeek strengths',
                        'MoE architecture providing excellent value'
                    ]
                }
            }

            return {
                'success': True,
                'tenant_id': tenant_id,
                'analytics': analytics_data,
                'optimization_score': 94.3,
                'usage_efficiency': 'excellent',
                'provider': 'DeepSeek',
                'recommendations': [
                    'Continue using DeepSeek for cost-sensitive tasks',
                    'Leverage reasoner model for complex problems',
                    'Use coder model for all code generation tasks'
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


class DeepSeekAPIIntegration:
    """Main integration class for DeepSeek API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY', 'demo_key_for_testing')
        self.chat_agent = DeepSeekChatAgent(self.api_key)
        self.reasoning_agent = DeepSeekReasoningAgent(self.api_key)
        self.coder_agent = DeepSeekCoderAgent(self.api_key)
        self.analytics_agent = DeepSeekAnalyticsAgent(self.api_key)

    async def generate_completion(
        self,
        tenant_id: str,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate chat completion using DeepSeek models"""
        return await self.chat_agent.generate_completion(tenant_id, messages, model, **kwargs)

    async def solve_problem(
        self,
        tenant_id: str,
        problem: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """Solve complex problems using DeepSeek R1"""
        return await self.reasoning_agent.solve_complex_problem(tenant_id, problem, context)

    async def generate_code(
        self,
        tenant_id: str,
        task: str,
        language: str = "python",
        include_tests: bool = True
    ) -> Dict[str, Any]:
        """Generate code using DeepSeek Coder"""
        return await self.coder_agent.generate_code(tenant_id, task, language, include_tests)

    async def get_usage_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get usage analytics and cost comparison"""
        return await self.analytics_agent.get_usage_analytics(tenant_id)

    async def get_connection_status(self, tenant_id: str) -> Dict[str, Any]:
        """Get DeepSeek API connection status and capabilities"""
        try:
            # Test connection with a simple completion
            test_messages = [{"role": "user", "content": "Hello"}]
            result = await self.chat_agent.generate_completion(tenant_id, test_messages, "deepseek-chat", max_tokens=10)

            if result['success']:
                return {
                    'status': 'connected',
                    'message': 'DeepSeek API connection successful',
                    'api_type': 'Cost-Optimized AI at Scale',
                    'available_models': [
                        'deepseek-chat (V3 - 671B params, 37B active)',
                        'deepseek-reasoner (R1 - Advanced reasoning)',
                        'deepseek-coder (Code generation specialist)'
                    ],
                    'capabilities': {
                        'chat_completions': 'High-quality text generation at lowest cost',
                        'advanced_reasoning': 'Complex problem solving with R1 model',
                        'code_generation': 'Specialized code generation and analysis',
                        'cost_efficiency': '~$0.55 per 1M tokens (40-60% savings vs GPT-4)',
                        'moe_architecture': '671B parameters with 37B active (efficient)'
                    },
                    'specialties': [
                        'Cost-optimized general tasks',
                        'Advanced reasoning and problem solving',
                        'Code generation and analysis',
                        'High-volume text processing',
                        'OpenAI-compatible API format'
                    ],
                    'pricing': {
                        'deepseek-chat': '$0.27 input / $1.10 output per 1M tokens',
                        'deepseek-reasoner': '$0.55 input / $2.19 output per 1M tokens',
                        'deepseek-coder': '$0.27 input / $1.10 output per 1M tokens'
                    }
                }
            else:
                return {
                    'status': 'connection_issues',
                    'message': f'DeepSeek API connection issues: {result.get("error", "Unknown error")}',
                    'api_type': 'Cost-Optimized AI at Scale'
                }

        except Exception as e:
            return {
                'status': 'disconnected',
                'message': f'DeepSeek API connection failed: {str(e)}',
                'api_type': 'Cost-Optimized AI at Scale'
            }


# Global integration instance
deepseek_api_integration = DeepSeekAPIIntegration()

if __name__ == "__main__":
    print("🚀 DeepSeek API Integration - Cost-Optimized AI at Scale")
    print("Access to DeepSeek-V3, DeepSeek-R1, and DeepSeek-Coder")
    print("💰 40-60% cost savings vs GPT-4 with competitive performance")
