"""
Smart LLM Router for BizOSaaS Platform
Intelligent provider selection based on task type, budget, context size, and performance

Features:
- Cost-optimized routing based on budget constraints
- Task-specific provider selection (RAG, vision, code, reasoning)
- Automatic fallback chain on provider failures
- Performance tracking and optimization
- Geographic compliance routing (EU vs US)
- Real-time provider health monitoring
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of AI tasks for routing decisions"""
    CHAT = "chat"
    REASONING = "reasoning"
    CODE_GENERATION = "code_generation"
    RAG = "rag"  # Retrieval-Augmented Generation
    VISION = "vision"
    EMBEDDING = "embedding"
    IMAGE_GENERATION = "image_generation"
    WEB_SEARCH = "web_search"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"


class BudgetTier(Enum):
    """Budget constraints for cost optimization"""
    FREE = "free"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNLIMITED = "unlimited"


class Region(Enum):
    """Geographic regions for compliance"""
    EU = "eu"
    US = "us"
    GLOBAL = "global"


class ProviderHealth:
    """Track provider health and performance"""

    def __init__(self):
        self.provider_stats: Dict[str, Dict] = {}

    def record_success(self, provider: str, response_time: float, cost: float):
        """Record successful provider response"""
        if provider not in self.provider_stats:
            self.provider_stats[provider] = {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'total_response_time': 0.0,
                'total_cost': 0.0,
                'last_success': None,
                'last_failure': None,
                'consecutive_failures': 0
            }

        stats = self.provider_stats[provider]
        stats['total_requests'] += 1
        stats['successful_requests'] += 1
        stats['total_response_time'] += response_time
        stats['total_cost'] += cost
        stats['last_success'] = datetime.utcnow().isoformat()
        stats['consecutive_failures'] = 0  # Reset failure counter

    def record_failure(self, provider: str, error: str):
        """Record provider failure"""
        if provider not in self.provider_stats:
            self.provider_stats[provider] = {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'total_response_time': 0.0,
                'total_cost': 0.0,
                'last_success': None,
                'last_failure': None,
                'consecutive_failures': 0
            }

        stats = self.provider_stats[provider]
        stats['total_requests'] += 1
        stats['failed_requests'] += 1
        stats['last_failure'] = datetime.utcnow().isoformat()
        stats['consecutive_failures'] += 1

    def get_success_rate(self, provider: str) -> float:
        """Calculate provider success rate"""
        if provider not in self.provider_stats:
            return 1.0  # Assume healthy if no data

        stats = self.provider_stats[provider]
        total = stats['total_requests']
        if total == 0:
            return 1.0

        return stats['successful_requests'] / total

    def is_healthy(self, provider: str, min_success_rate: float = 0.9) -> bool:
        """Check if provider is healthy"""
        success_rate = self.get_success_rate(provider)

        # Check consecutive failures
        if provider in self.provider_stats:
            if self.provider_stats[provider]['consecutive_failures'] >= 3:
                return False

        return success_rate >= min_success_rate

    def get_avg_response_time(self, provider: str) -> float:
        """Get average response time for provider"""
        if provider not in self.provider_stats:
            return 1.0  # Default estimate

        stats = self.provider_stats[provider]
        if stats['successful_requests'] == 0:
            return 1.0

        return stats['total_response_time'] / stats['successful_requests']


class SmartLLMRouter:
    """Intelligent LLM provider routing engine"""

    def __init__(self):
        self.health_monitor = ProviderHealth()
        self.routing_rules = self._initialize_routing_rules()

    def _initialize_routing_rules(self) -> Dict[str, Any]:
        """Initialize provider routing rules"""
        return {
            # Cost optimization rules (per million tokens)
            'cost_tiers': {
                BudgetTier.FREE: ['huggingface'],
                BudgetTier.LOW: ['deepseek', 'mistral-small', 'huggingface'],
                BudgetTier.MEDIUM: ['mistral-medium', 'cohere', 'gemini', 'openrouter'],
                BudgetTier.HIGH: ['gpt-4', 'claude-opus', 'mistral-large'],
                BudgetTier.UNLIMITED: ['gpt-4', 'claude-opus', 'azure-openai']
            },

            # Task-specific provider recommendations
            'task_providers': {
                TaskType.CHAT: {
                    'primary': ['openrouter', 'deepseek', 'mistral-medium'],
                    'fallback': ['gpt-3.5', 'claude-sonnet', 'gemini']
                },
                TaskType.REASONING: {
                    'primary': ['claude-opus', 'deepseek-r1', 'gpt-4'],
                    'fallback': ['mistral-large', 'openrouter']
                },
                TaskType.CODE_GENERATION: {
                    'primary': ['vertex-codey', 'huggingface-starcoder', 'gpt-4'],
                    'fallback': ['deepseek-coder', 'claude-sonnet']
                },
                TaskType.RAG: {
                    'primary': ['cohere', 'openrouter'],
                    'fallback': ['claude-sonnet', 'gpt-4']
                },
                TaskType.VISION: {
                    'primary': ['gpt-4v', 'gemini-vision', 'vertex-vision'],
                    'fallback': ['huggingface-llava', 'azure-openai-vision']
                },
                TaskType.EMBEDDING: {
                    'primary': ['cohere-embed', 'huggingface-bge', 'openai-ada'],
                    'fallback': ['mistral-embed', 'vertex-embed']
                },
                TaskType.IMAGE_GENERATION: {
                    'primary': ['huggingface-sdxl', 'azure-dalle3', 'bedrock-stable-diffusion'],
                    'fallback': ['openai-dalle3']
                },
                TaskType.WEB_SEARCH: {
                    'primary': ['perplexity'],
                    'fallback': ['openrouter', 'gpt-4']
                },
                TaskType.SUMMARIZATION: {
                    'primary': ['claude-sonnet', 'perplexity', 'cohere'],
                    'fallback': ['mistral-medium', 'gpt-3.5']
                },
                TaskType.TRANSLATION: {
                    'primary': ['gemini', 'gpt-4', 'mistral-large'],
                    'fallback': ['openrouter', 'deepseek']
                }
            },

            # Geographic compliance rules
            'region_providers': {
                Region.EU: ['mistral', 'azure-openai-eu', 'vertex-eu'],
                Region.US: ['openai', 'anthropic', 'bedrock-us'],
                Region.GLOBAL: ['openrouter', 'gemini', 'deepseek']
            },

            # Context window requirements
            'context_windows': {
                'small': {'max': 8192, 'providers': ['gpt-3.5', 'deepseek', 'mistral-small']},
                'medium': {'max': 32768, 'providers': ['gpt-4', 'claude-sonnet', 'mistral-medium']},
                'large': {'max': 200000, 'providers': ['claude-opus', 'claude-sonnet']},
                'xlarge': {'max': 1000000, 'providers': ['gemini', 'vertex-gemini']}
            },

            # Enterprise features
            'enterprise_providers': {
                'sla_required': ['azure-openai', 'bedrock', 'vertex'],
                'compliance_required': ['azure-openai', 'mistral-eu', 'bedrock'],
                'self_hosting': ['mistral', 'huggingface', 'vertex']
            }
        }

    async def route_request(
        self,
        task_type: TaskType,
        budget: BudgetTier = BudgetTier.MEDIUM,
        context_size: int = 0,
        region: Region = Region.GLOBAL,
        requires_sla: bool = False,
        requires_compliance: bool = False,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Route request to optimal LLM provider

        Args:
            task_type: Type of AI task
            budget: Budget constraint
            context_size: Number of tokens in context
            region: Geographic region requirement
            requires_sla: Whether enterprise SLA is required
            requires_compliance: Whether compliance (GDPR, SOC2) is required
            max_retries: Maximum number of provider retries

        Returns:
            Routing decision with primary and fallback providers
        """

        # Step 1: Get task-specific providers
        task_providers = self.routing_rules['task_providers'].get(
            task_type,
            {'primary': ['openrouter'], 'fallback': ['gpt-4']}
        )

        # Step 2: Filter by budget
        budget_providers = self.routing_rules['cost_tiers'].get(budget, [])

        # Step 3: Filter by region
        region_providers = self.routing_rules['region_providers'].get(region, [])

        # Step 4: Filter by context window size
        context_providers = self._get_providers_for_context(context_size)

        # Step 5: Apply enterprise requirements
        if requires_sla:
            sla_providers = self.routing_rules['enterprise_providers']['sla_required']
        else:
            sla_providers = None

        if requires_compliance:
            compliance_providers = self.routing_rules['enterprise_providers']['compliance_required']
        else:
            compliance_providers = None

        # Step 6: Find optimal provider with all constraints
        primary_candidates = self._filter_providers(
            task_providers['primary'],
            budget_providers,
            region_providers,
            context_providers,
            sla_providers,
            compliance_providers
        )

        fallback_candidates = self._filter_providers(
            task_providers['fallback'],
            budget_providers,
            region_providers,
            context_providers,
            sla_providers,
            compliance_providers
        )

        # Step 7: Sort by health and performance
        primary_providers = self._sort_by_health(primary_candidates)
        fallback_providers = self._sort_by_health(fallback_candidates)

        # Step 8: Build routing decision
        routing_decision = {
            'task_type': task_type.value,
            'budget': budget.value,
            'region': region.value,
            'primary_provider': primary_providers[0] if primary_providers else 'openrouter',
            'fallback_providers': fallback_providers[:3],  # Top 3 fallbacks
            'routing_strategy': self._get_routing_strategy(task_type, budget),
            'estimated_cost': self._estimate_cost(primary_providers[0] if primary_providers else 'openrouter'),
            'expected_quality': self._estimate_quality(task_type, primary_providers[0] if primary_providers else 'openrouter'),
            'context_window_supported': context_size <= self._get_max_context(primary_providers[0] if primary_providers else 'openrouter'),
            'timestamp': datetime.utcnow().isoformat()
        }

        return routing_decision

    def _filter_providers(
        self,
        candidates: List[str],
        budget_filter: List[str] = None,
        region_filter: List[str] = None,
        context_filter: List[str] = None,
        sla_filter: List[str] = None,
        compliance_filter: List[str] = None
    ) -> List[str]:
        """Filter providers by multiple constraints"""

        filtered = set(candidates)

        # Apply budget filter
        if budget_filter:
            budget_set = set(budget_filter)
            filtered = filtered.intersection(budget_set) if filtered.intersection(budget_set) else filtered

        # Apply region filter
        if region_filter:
            region_set = set(region_filter)
            filtered = filtered.intersection(region_set) if filtered.intersection(region_set) else filtered

        # Apply context window filter
        if context_filter:
            context_set = set(context_filter)
            filtered = filtered.intersection(context_set) if filtered.intersection(context_set) else filtered

        # Apply SLA filter
        if sla_filter:
            sla_set = set(sla_filter)
            filtered = filtered.intersection(sla_set) if filtered.intersection(sla_set) else filtered

        # Apply compliance filter
        if compliance_filter:
            compliance_set = set(compliance_filter)
            filtered = filtered.intersection(compliance_set) if filtered.intersection(compliance_set) else filtered

        return list(filtered) if filtered else candidates  # Return original if no matches

    def _get_providers_for_context(self, context_size: int) -> List[str]:
        """Get providers that support the required context window"""
        if context_size == 0:
            return []  # No filter if context not specified

        providers = []
        for category, info in self.routing_rules['context_windows'].items():
            if context_size <= info['max']:
                providers.extend(info['providers'])

        return providers

    def _sort_by_health(self, providers: List[str]) -> List[str]:
        """Sort providers by health and performance"""
        if not providers:
            return []

        # Score each provider
        scored_providers = []
        for provider in providers:
            success_rate = self.health_monitor.get_success_rate(provider)
            avg_response_time = self.health_monitor.get_avg_response_time(provider)

            # Calculate score (higher is better)
            # Success rate weighted 70%, speed weighted 30%
            speed_score = max(0, 1 - (avg_response_time / 10.0))  # Normalize to 0-1
            score = (success_rate * 0.7) + (speed_score * 0.3)

            scored_providers.append((provider, score))

        # Sort by score descending
        scored_providers.sort(key=lambda x: x[1], reverse=True)

        return [p[0] for p in scored_providers]

    def _get_routing_strategy(self, task_type: TaskType, budget: BudgetTier) -> str:
        """Determine routing strategy description"""
        if budget == BudgetTier.FREE:
            return "cost_minimization"
        elif budget == BudgetTier.LOW:
            return "cost_optimized"
        elif task_type == TaskType.REASONING:
            return "quality_optimized"
        elif task_type == TaskType.RAG:
            return "rag_optimized"
        else:
            return "balanced"

    def _estimate_cost(self, provider: str) -> Dict[str, float]:
        """Estimate cost for provider"""
        # Cost estimates per million tokens (input/output average)
        cost_estimates = {
            'deepseek': 0.69,
            'mistral-small': 0.40,
            'mistral-medium': 1.35,
            'mistral-large': 4.00,
            'cohere': 1.50,
            'huggingface': 0.00,
            'gpt-3.5': 1.00,
            'gpt-4': 20.00,
            'claude-sonnet': 9.00,
            'claude-opus': 45.00,
            'gemini': 2.00,
            'openrouter': 5.00,  # Average across models
            'azure-openai': 20.00,
            'bedrock': 15.00,
            'vertex': 2.50,
            'perplexity': 2.00
        }

        estimated_cost = cost_estimates.get(provider, 5.00)

        return {
            'estimated_cost_per_million_tokens': estimated_cost,
            'savings_vs_gpt4': round(((20.00 - estimated_cost) / 20.00) * 100, 1),
            'tier': 'free' if estimated_cost == 0 else 'low' if estimated_cost < 1 else 'medium' if estimated_cost < 10 else 'high'
        }

    def _estimate_quality(self, task_type: TaskType, provider: str) -> Dict[str, Any]:
        """Estimate quality for task/provider combination"""

        # Quality ratings (1-10 scale)
        quality_matrix = {
            TaskType.REASONING: {
                'claude-opus': 10, 'gpt-4': 9, 'deepseek-r1': 8,
                'mistral-large': 8, 'claude-sonnet': 7
            },
            TaskType.RAG: {
                'cohere': 10, 'claude-sonnet': 8, 'gpt-4': 8,
                'openrouter': 7, 'gemini': 7
            },
            TaskType.CODE_GENERATION: {
                'vertex-codey': 9, 'gpt-4': 9, 'claude-sonnet': 8,
                'deepseek-coder': 7, 'huggingface-starcoder': 7
            },
            TaskType.WEB_SEARCH: {
                'perplexity': 10, 'openrouter': 6, 'gpt-4': 5
            }
        }

        task_quality = quality_matrix.get(task_type, {})
        quality_score = task_quality.get(provider, 7)  # Default to 7/10

        return {
            'quality_score': quality_score,
            'quality_tier': 'excellent' if quality_score >= 9 else 'good' if quality_score >= 7 else 'acceptable',
            'confidence': 'high' if quality_score >= 8 else 'medium'
        }

    def _get_max_context(self, provider: str) -> int:
        """Get maximum context window for provider"""
        context_limits = {
            'gpt-3.5': 16384,
            'gpt-4': 8192,
            'gpt-4-turbo': 128000,
            'claude-opus': 200000,
            'claude-sonnet': 200000,
            'claude-haiku': 200000,
            'gemini': 1000000,
            'deepseek': 64000,
            'mistral-small': 32000,
            'mistral-medium': 32000,
            'mistral-large': 32000,
            'cohere': 128000,
            'huggingface': 8192,
            'openrouter': 32000,
            'perplexity': 128000
        }

        return context_limits.get(provider, 8192)

    async def execute_with_fallback(
        self,
        routing_decision: Dict[str, Any],
        execution_func: callable,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute request with automatic fallback on failure

        Args:
            routing_decision: Routing decision from route_request()
            execution_func: Async function to execute (must accept provider param)
            **kwargs: Additional arguments for execution_func

        Returns:
            Execution result with provider metadata
        """

        primary_provider = routing_decision['primary_provider']
        fallback_providers = routing_decision['fallback_providers']

        # Try primary provider
        start_time = datetime.utcnow()
        try:
            result = await execution_func(provider=primary_provider, **kwargs)

            # Record success
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            cost = result.get('cost', {}).get('total_cost', 0.0)
            self.health_monitor.record_success(primary_provider, elapsed, cost)

            result['routing_info'] = {
                'provider_used': primary_provider,
                'fallback_attempted': False,
                'response_time': elapsed,
                'routing_decision': routing_decision
            }

            return result

        except Exception as e:
            logger.error(f"Primary provider {primary_provider} failed: {str(e)}")
            self.health_monitor.record_failure(primary_provider, str(e))

            # Try fallback providers
            for fallback_provider in fallback_providers:
                try:
                    logger.info(f"Attempting fallback to {fallback_provider}")
                    start_time = datetime.utcnow()

                    result = await execution_func(provider=fallback_provider, **kwargs)

                    # Record success
                    elapsed = (datetime.utcnow() - start_time).total_seconds()
                    cost = result.get('cost', {}).get('total_cost', 0.0)
                    self.health_monitor.record_success(fallback_provider, elapsed, cost)

                    result['routing_info'] = {
                        'provider_used': fallback_provider,
                        'fallback_attempted': True,
                        'primary_provider_failed': primary_provider,
                        'response_time': elapsed,
                        'routing_decision': routing_decision
                    }

                    return result

                except Exception as fallback_error:
                    logger.error(f"Fallback provider {fallback_provider} failed: {str(fallback_error)}")
                    self.health_monitor.record_failure(fallback_provider, str(fallback_error))
                    continue

            # All providers failed
            return {
                'success': False,
                'error': 'All providers failed',
                'primary_provider': primary_provider,
                'fallback_providers_attempted': fallback_providers,
                'routing_decision': routing_decision
            }

    def get_routing_analytics(self) -> Dict[str, Any]:
        """Get routing analytics and recommendations"""

        analytics = {
            'provider_stats': {},
            'top_performers': [],
            'problematic_providers': [],
            'cost_analysis': {},
            'recommendations': []
        }

        # Analyze each provider
        for provider, stats in self.health_monitor.provider_stats.items():
            success_rate = self.health_monitor.get_success_rate(provider)
            avg_response_time = self.health_monitor.get_avg_response_time(provider)

            analytics['provider_stats'][provider] = {
                'success_rate': round(success_rate * 100, 2),
                'total_requests': stats['total_requests'],
                'avg_response_time': round(avg_response_time, 2),
                'total_cost': round(stats['total_cost'], 2),
                'is_healthy': self.health_monitor.is_healthy(provider)
            }

        # Identify top performers (success rate > 95%, response time < 3s)
        for provider, stats in analytics['provider_stats'].items():
            if stats['success_rate'] > 95 and stats['avg_response_time'] < 3.0:
                analytics['top_performers'].append(provider)

        # Identify problematic providers (success rate < 90% or response time > 5s)
        for provider, stats in analytics['provider_stats'].items():
            if stats['success_rate'] < 90 or stats['avg_response_time'] > 5.0:
                analytics['problematic_providers'].append(provider)

        # Generate recommendations
        if analytics['problematic_providers']:
            analytics['recommendations'].append(
                f"Consider reducing traffic to: {', '.join(analytics['problematic_providers'])}"
            )

        if analytics['top_performers']:
            analytics['recommendations'].append(
                f"Route more traffic to top performers: {', '.join(analytics['top_performers'])}"
            )

        return analytics


# Example usage and testing
async def main():
    """Test smart router"""
    print("🧠 Initializing Smart LLM Router\n")

    router = SmartLLMRouter()

    # Test 1: Simple chat with low budget
    print("1. Simple Chat (Low Budget):")
    decision1 = await router.route_request(
        task_type=TaskType.CHAT,
        budget=BudgetTier.LOW
    )
    print(f"   Primary: {decision1['primary_provider']}")
    print(f"   Fallback: {decision1['fallback_providers']}")
    print(f"   Strategy: {decision1['routing_strategy']}")
    print(f"   Est. Cost: ${decision1['estimated_cost']['estimated_cost_per_million_tokens']:.2f}/M tokens\n")

    # Test 2: Advanced reasoning with high budget
    print("2. Advanced Reasoning (High Budget):")
    decision2 = await router.route_request(
        task_type=TaskType.REASONING,
        budget=BudgetTier.HIGH
    )
    print(f"   Primary: {decision2['primary_provider']}")
    print(f"   Quality: {decision2['expected_quality']['quality_tier']}\n")

    # Test 3: RAG task
    print("3. RAG Task (Medium Budget):")
    decision3 = await router.route_request(
        task_type=TaskType.RAG,
        budget=BudgetTier.MEDIUM
    )
    print(f"   Primary: {decision3['primary_provider']}")
    print(f"   Strategy: {decision3['routing_strategy']}\n")

    # Test 4: EU compliance requirement
    print("4. EU Compliance Requirement:")
    decision4 = await router.route_request(
        task_type=TaskType.CHAT,
        budget=BudgetTier.MEDIUM,
        region=Region.EU,
        requires_compliance=True
    )
    print(f"   Primary: {decision4['primary_provider']}")
    print(f"   Region: {decision4['region']}\n")

    # Test 5: Large context window
    print("5. Large Context (500K tokens):")
    decision5 = await router.route_request(
        task_type=TaskType.CHAT,
        budget=BudgetTier.MEDIUM,
        context_size=500000
    )
    print(f"   Primary: {decision5['primary_provider']}")
    print(f"   Context Supported: {decision5['context_window_supported']}\n")

    print("✅ Smart LLM Router initialized successfully")
    print("📊 Ready for intelligent provider routing")


if __name__ == "__main__":
    asyncio.run(main())
