"""
Routing Analytics for Smart LLM Router
Tracks performance, costs, and optimization opportunities

Features:
- Real-time provider performance tracking
- Cost analysis and savings calculations
- Quality metrics per provider/task combination
- Routing effectiveness analysis
- Recommendations engine
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RoutingAnalytics:
    """Analytics engine for LLM routing decisions"""

    def __init__(self):
        self.routing_history: List[Dict] = []
        self.provider_performance: Dict[str, Dict] = defaultdict(lambda: {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_cost': 0.0,
            'total_response_time': 0.0,
            'fallback_count': 0,
            'quality_scores': [],
            'tasks_handled': defaultdict(int)
        })

    def record_routing_decision(
        self,
        routing_decision: Dict[str, Any],
        execution_result: Dict[str, Any]
    ):
        """Record a routing decision and its outcome"""

        record = {
            'timestamp': datetime.utcnow().isoformat(),
            'routing_decision': routing_decision,
            'execution_result': execution_result,
            'success': execution_result.get('success', False),
            'provider_used': execution_result.get('routing_info', {}).get('provider_used'),
            'fallback_attempted': execution_result.get('routing_info', {}).get('fallback_attempted', False),
            'response_time': execution_result.get('routing_info', {}).get('response_time', 0.0),
            'cost': execution_result.get('cost', {}).get('total_cost', 0.0),
            'quality_score': self._calculate_quality_score(execution_result)
        }

        self.routing_history.append(record)

        # Update provider performance stats
        provider = record['provider_used']
        if provider:
            stats = self.provider_performance[provider]
            stats['total_requests'] += 1

            if record['success']:
                stats['successful_requests'] += 1
                stats['total_cost'] += record['cost']
                stats['total_response_time'] += record['response_time']
                stats['quality_scores'].append(record['quality_score'])

                # Track task distribution
                task_type = routing_decision.get('task_type', 'unknown')
                stats['tasks_handled'][task_type] += 1
            else:
                stats['failed_requests'] += 1

            if record['fallback_attempted']:
                stats['fallback_count'] += 1

    def _calculate_quality_score(self, execution_result: Dict[str, Any]) -> float:
        """Calculate quality score for response (0-10 scale)"""

        if not execution_result.get('success'):
            return 0.0

        quality = execution_result.get('quality', {})

        # Factors contributing to quality
        length_score = min(10, quality.get('word_count', 0) / 100)  # Normalize
        has_code = 10 if quality.get('has_code') else 5
        has_lists = 10 if quality.get('has_lists') else 5
        has_citations = 10 if quality.get('citation_count', 0) > 0 else 5

        # Weighted average
        score = (length_score * 0.2 + has_code * 0.2 + has_lists * 0.3 + has_citations * 0.3)

        return min(10.0, score)

    def get_provider_analytics(
        self,
        provider: Optional[str] = None,
        time_window_hours: int = 24
    ) -> Dict[str, Any]:
        """Get detailed analytics for provider(s)"""

        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)

        if provider:
            # Single provider analytics
            stats = self.provider_performance[provider]

            return {
                'provider': provider,
                'time_window_hours': time_window_hours,
                'total_requests': stats['total_requests'],
                'success_rate': self._calculate_success_rate(provider),
                'avg_response_time': self._calculate_avg_response_time(provider),
                'total_cost': round(stats['total_cost'], 2),
                'avg_cost_per_request': round(stats['total_cost'] / max(stats['total_requests'], 1), 4),
                'avg_quality_score': round(sum(stats['quality_scores']) / max(len(stats['quality_scores']), 1), 2),
                'fallback_rate': round(stats['fallback_count'] / max(stats['total_requests'], 1) * 100, 2),
                'tasks_handled': dict(stats['tasks_handled']),
                'health_status': self._get_health_status(provider)
            }
        else:
            # All providers analytics
            all_stats = {}
            for prov in self.provider_performance.keys():
                all_stats[prov] = self.get_provider_analytics(prov, time_window_hours)

            return {
                'time_window_hours': time_window_hours,
                'providers': all_stats,
                'total_providers': len(all_stats),
                'top_performer': self._get_top_performer(),
                'most_cost_effective': self._get_most_cost_effective(),
                'recommendations': self.generate_recommendations()
            }

    def _calculate_success_rate(self, provider: str) -> float:
        """Calculate success rate for provider"""
        stats = self.provider_performance[provider]
        total = stats['total_requests']
        if total == 0:
            return 100.0

        return round((stats['successful_requests'] / total) * 100, 2)

    def _calculate_avg_response_time(self, provider: str) -> float:
        """Calculate average response time for provider"""
        stats = self.provider_performance[provider]
        if stats['successful_requests'] == 0:
            return 0.0

        return round(stats['total_response_time'] / stats['successful_requests'], 2)

    def _get_health_status(self, provider: str) -> str:
        """Determine health status of provider"""
        success_rate = self._calculate_success_rate(provider)
        avg_response_time = self._calculate_avg_response_time(provider)

        if success_rate >= 95 and avg_response_time < 3.0:
            return "excellent"
        elif success_rate >= 90 and avg_response_time < 5.0:
            return "good"
        elif success_rate >= 80:
            return "acceptable"
        else:
            return "poor"

    def _get_top_performer(self) -> Dict[str, Any]:
        """Identify top performing provider"""
        if not self.provider_performance:
            return {'provider': 'none', 'reason': 'No data available'}

        # Score providers by success rate and speed
        best_provider = None
        best_score = 0.0

        for provider, stats in self.provider_performance.items():
            if stats['total_requests'] < 5:  # Need minimum data
                continue

            success_rate = self._calculate_success_rate(provider) / 100
            avg_response_time = self._calculate_avg_response_time(provider)
            speed_score = max(0, 1 - (avg_response_time / 10))

            # Weighted score (70% success, 30% speed)
            score = (success_rate * 0.7) + (speed_score * 0.3)

            if score > best_score:
                best_score = score
                best_provider = provider

        if best_provider:
            return {
                'provider': best_provider,
                'score': round(best_score * 100, 2),
                'success_rate': self._calculate_success_rate(best_provider),
                'avg_response_time': self._calculate_avg_response_time(best_provider)
            }

        return {'provider': 'none', 'reason': 'Insufficient data'}

    def _get_most_cost_effective(self) -> Dict[str, Any]:
        """Identify most cost-effective provider"""
        if not self.provider_performance:
            return {'provider': 'none', 'reason': 'No data available'}

        best_provider = None
        best_value = 0.0  # Quality per dollar

        for provider, stats in self.provider_performance.items():
            if stats['total_requests'] < 5 or stats['total_cost'] == 0:
                continue

            avg_quality = sum(stats['quality_scores']) / max(len(stats['quality_scores']), 1)
            avg_cost = stats['total_cost'] / stats['total_requests']

            # Value = quality / cost (higher is better)
            value = avg_quality / max(avg_cost, 0.000001)

            if value > best_value:
                best_value = value
                best_provider = provider

        if best_provider:
            stats = self.provider_performance[best_provider]
            return {
                'provider': best_provider,
                'avg_cost_per_request': round(stats['total_cost'] / stats['total_requests'], 4),
                'avg_quality_score': round(sum(stats['quality_scores']) / len(stats['quality_scores']), 2),
                'value_score': round(best_value, 2)
            }

        return {'provider': 'none', 'reason': 'Insufficient data'}

    def generate_recommendations(self) -> List[str]:
        """Generate routing optimization recommendations"""
        recommendations = []

        # Analyze provider performance
        for provider, stats in self.provider_performance.items():
            if stats['total_requests'] < 10:
                continue

            success_rate = self._calculate_success_rate(provider)
            avg_response_time = self._calculate_avg_response_time(provider)
            fallback_rate = (stats['fallback_count'] / stats['total_requests']) * 100

            # High failure rate
            if success_rate < 85:
                recommendations.append(
                    f"⚠️ {provider}: Low success rate ({success_rate:.1f}%). Consider removing from primary routing."
                )

            # Slow response
            if avg_response_time > 5.0:
                recommendations.append(
                    f"🐌 {provider}: Slow response time ({avg_response_time:.1f}s). Consider routing fast tasks elsewhere."
                )

            # High fallback rate
            if fallback_rate > 20:
                recommendations.append(
                    f"🔄 {provider}: High fallback rate ({fallback_rate:.1f}%). Investigate reliability issues."
                )

            # Excellent performance
            if success_rate > 98 and avg_response_time < 2.0:
                recommendations.append(
                    f"⭐ {provider}: Excellent performance ({success_rate:.1f}% success, {avg_response_time:.1f}s). Increase routing priority."
                )

        # Cost optimization recommendations
        top_performer = self._get_top_performer()
        most_cost_effective = self._get_most_cost_effective()

        if top_performer.get('provider') != 'none':
            recommendations.append(
                f"🏆 Top performer: {top_performer['provider']} ({top_performer['success_rate']:.1f}% success rate)"
            )

        if most_cost_effective.get('provider') != 'none':
            recommendations.append(
                f"💰 Most cost-effective: {most_cost_effective['provider']} (${most_cost_effective['avg_cost_per_request']:.4f} per request)"
            )

        if not recommendations:
            recommendations.append("✅ All providers performing within acceptable ranges")

        return recommendations

    def get_cost_analysis(
        self,
        time_window_hours: int = 24
    ) -> Dict[str, Any]:
        """Analyze costs and savings"""

        total_cost = 0.0
        provider_costs = {}

        for provider, stats in self.provider_performance.items():
            provider_costs[provider] = round(stats['total_cost'], 2)
            total_cost += stats['total_cost']

        # Calculate what it would have cost with GPT-4 only
        total_requests = sum(stats['total_requests'] for stats in self.provider_performance.values())
        estimated_gpt4_cost = total_requests * 0.00002  # Rough estimate

        savings = estimated_gpt4_cost - total_cost
        savings_percent = (savings / max(estimated_gpt4_cost, 0.000001)) * 100

        return {
            'time_window_hours': time_window_hours,
            'total_cost': round(total_cost, 2),
            'estimated_gpt4_cost': round(estimated_gpt4_cost, 2),
            'actual_savings': round(savings, 2),
            'savings_percent': round(savings_percent, 1),
            'provider_breakdown': provider_costs,
            'total_requests': total_requests,
            'avg_cost_per_request': round(total_cost / max(total_requests, 1), 4)
        }

    def get_task_distribution(self) -> Dict[str, Any]:
        """Analyze task distribution across providers"""

        task_totals = defaultdict(int)
        task_by_provider = defaultdict(lambda: defaultdict(int))

        for provider, stats in self.provider_performance.items():
            for task, count in stats['tasks_handled'].items():
                task_totals[task] += count
                task_by_provider[provider][task] = count

        return {
            'total_tasks_by_type': dict(task_totals),
            'tasks_by_provider': {
                provider: dict(tasks)
                for provider, tasks in task_by_provider.items()
            },
            'recommendations': self._get_task_routing_recommendations(task_by_provider)
        }

    def _get_task_routing_recommendations(
        self,
        task_by_provider: Dict[str, Dict[str, int]]
    ) -> List[str]:
        """Generate task-specific routing recommendations"""

        recommendations = []

        # Find best provider for each task type
        task_best_providers = defaultdict(lambda: {'provider': None, 'score': 0})

        for provider, tasks in task_by_provider.items():
            provider_success_rate = self._calculate_success_rate(provider) / 100
            provider_response_time = self._calculate_avg_response_time(provider)
            speed_score = max(0, 1 - (provider_response_time / 10))

            for task, count in tasks.items():
                if count < 5:  # Need minimum data
                    continue

                # Score = success * 0.7 + speed * 0.3
                score = (provider_success_rate * 0.7) + (speed_score * 0.3)

                if score > task_best_providers[task]['score']:
                    task_best_providers[task] = {
                        'provider': provider,
                        'score': score
                    }

        for task, best in task_best_providers.items():
            if best['provider']:
                recommendations.append(
                    f"📋 {task}: Best performance with {best['provider']} (score: {best['score']*100:.1f})"
                )

        return recommendations

    def export_analytics(
        self,
        format: str = 'json',
        include_raw_data: bool = False
    ) -> str:
        """Export analytics data"""

        analytics_data = {
            'export_timestamp': datetime.utcnow().isoformat(),
            'summary': {
                'total_routing_decisions': len(self.routing_history),
                'active_providers': len(self.provider_performance),
                'time_range': self._get_time_range()
            },
            'provider_analytics': self.get_provider_analytics(),
            'cost_analysis': self.get_cost_analysis(),
            'task_distribution': self.get_task_distribution(),
            'recommendations': self.generate_recommendations()
        }

        if include_raw_data:
            analytics_data['raw_routing_history'] = self.routing_history[-100:]  # Last 100 records

        if format == 'json':
            return json.dumps(analytics_data, indent=2)
        else:
            # CSV format for simple tabular data
            csv_lines = ["Provider,Success Rate,Avg Response Time,Total Cost,Health Status"]
            for provider, stats in analytics_data['provider_analytics']['providers'].items():
                csv_lines.append(
                    f"{provider},{stats['success_rate']},{stats['avg_response_time']},"
                    f"{stats['total_cost']},{stats['health_status']}"
                )
            return "\n".join(csv_lines)

    def _get_time_range(self) -> Dict[str, str]:
        """Get time range of recorded data"""
        if not self.routing_history:
            return {'start': 'N/A', 'end': 'N/A'}

        timestamps = [record['timestamp'] for record in self.routing_history]
        return {
            'start': min(timestamps),
            'end': max(timestamps)
        }


# Example usage
async def main():
    """Test routing analytics"""
    print("📊 Initializing Routing Analytics\n")

    analytics = RoutingAnalytics()

    # Simulate some routing decisions and results
    test_data = [
        {
            'routing_decision': {'task_type': 'chat', 'budget': 'low', 'primary_provider': 'deepseek'},
            'execution_result': {
                'success': True,
                'routing_info': {'provider_used': 'deepseek', 'response_time': 1.2},
                'cost': {'total_cost': 0.0005},
                'quality': {'word_count': 150, 'has_code': False, 'has_lists': True}
            }
        },
        {
            'routing_decision': {'task_type': 'reasoning', 'budget': 'high', 'primary_provider': 'claude-opus'},
            'execution_result': {
                'success': True,
                'routing_info': {'provider_used': 'claude-opus', 'response_time': 2.3},
                'cost': {'total_cost': 0.025},
                'quality': {'word_count': 300, 'has_code': False, 'has_lists': True, 'citation_count': 3}
            }
        },
        {
            'routing_decision': {'task_type': 'rag', 'budget': 'medium', 'primary_provider': 'cohere'},
            'execution_result': {
                'success': True,
                'routing_info': {'provider_used': 'cohere', 'response_time': 1.8},
                'cost': {'total_cost': 0.012},
                'quality': {'word_count': 200, 'citation_count': 5}
            }
        }
    ]

    for data in test_data:
        analytics.record_routing_decision(data['routing_decision'], data['execution_result'])

    # Get analytics
    print("1. Provider Analytics:")
    provider_analytics = analytics.get_provider_analytics()
    print(f"   Total Providers: {provider_analytics['total_providers']}")
    print(f"   Top Performer: {provider_analytics['top_performer']['provider']}\n")

    print("2. Cost Analysis:")
    cost_analysis = analytics.get_cost_analysis()
    print(f"   Total Cost: ${cost_analysis['total_cost']:.4f}")
    print(f"   Savings: {cost_analysis['savings_percent']:.1f}%\n")

    print("3. Recommendations:")
    for rec in analytics.generate_recommendations():
        print(f"   {rec}")

    print("\n✅ Routing Analytics initialized successfully")


if __name__ == "__main__":
    asyncio.run(main())
