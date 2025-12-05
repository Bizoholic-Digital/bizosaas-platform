"""
BizOSaaS Autonomous AI Workflow Monitoring and Continuous Improvement System

This module implements AI agents that continuously monitor platform changes,
analyze performance metrics, and generate automated improvement suggestions.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import asyncpg
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"

class TaskCategory(str, Enum):
    PERFORMANCE = "performance"
    SECURITY = "security"
    USER_EXPERIENCE = "user_experience"
    INFRASTRUCTURE = "infrastructure"
    FEATURES = "features"
    OPTIMIZATION = "optimization"
    MONITORING = "monitoring"
    DOCUMENTATION = "documentation"

@dataclass
class ImprovementTask:
    """Represents an AI-generated improvement task"""
    id: str
    title: str
    description: str
    category: TaskCategory
    priority: TaskPriority
    estimated_effort: str  # "1-2 hours", "1-3 days", "1-2 weeks"
    impact_score: float  # 0-10 scale
    confidence: float  # 0-1 scale
    data_source: str
    metrics: Dict[str, Any]
    suggested_solution: str
    dependencies: List[str]
    tenant_specific: Optional[str] = None
    created_at: datetime = None
    status: str = "pending"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

class MetricsCollector:
    """Collects metrics from various platform sources"""
    
    def __init__(self, db_url: str, brain_api_url: str):
        self.db_url = db_url
        self.brain_api_url = brain_api_url
        
    async def collect_performance_metrics(self) -> Dict[str, Any]:
        """Collect performance metrics from Brain API and database"""
        async with aiohttp.ClientSession() as session:
            try:
                # Get API response times
                async with session.get(f"{self.brain_api_url}/api/health/detailed") as resp:
                    api_health = await resp.json()
                
                # Get database performance
                async with session.get(f"{self.brain_api_url}/api/analytics/performance") as resp:
                    db_performance = await resp.json()
                
                # Get AI agent execution metrics
                async with session.get(f"{self.brain_api_url}/api/agents/metrics") as resp:
                    agent_metrics = await resp.json()
                
                return {
                    "api_health": api_health,
                    "database_performance": db_performance,
                    "agent_metrics": agent_metrics,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.error(f"Error collecting performance metrics: {e}")
                return {}
    
    async def collect_usage_metrics(self) -> Dict[str, Any]:
        """Collect usage patterns and user behavior metrics"""
        async with aiohttp.ClientSession() as session:
            try:
                # Get user activity patterns
                async with session.get(f"{self.brain_api_url}/api/analytics/users/activity") as resp:
                    user_activity = await resp.json()
                
                # Get feature usage statistics
                async with session.get(f"{self.brain_api_url}/api/analytics/features/usage") as resp:
                    feature_usage = await resp.json()
                
                # Get integration usage
                async with session.get(f"{self.brain_api_url}/api/integrations/usage-stats") as resp:
                    integration_usage = await resp.json()
                
                return {
                    "user_activity": user_activity,
                    "feature_usage": feature_usage,
                    "integration_usage": integration_usage,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.error(f"Error collecting usage metrics: {e}")
                return {}
    
    async def collect_error_metrics(self) -> Dict[str, Any]:
        """Collect error rates and failure patterns"""
        async with aiohttp.ClientSession() as session:
            try:
                # Get error rates by endpoint
                async with session.get(f"{self.brain_api_url}/api/monitoring/errors") as resp:
                    error_stats = await resp.json()
                
                # Get failed AI agent executions
                async with session.get(f"{self.brain_api_url}/api/agents/failures") as resp:
                    agent_failures = await resp.json()
                
                return {
                    "error_stats": error_stats,
                    "agent_failures": agent_failures,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.error(f"Error collecting error metrics: {e}")
                return {}

class WorkflowAnalyzer:
    """Analyzes collected metrics and identifies improvement opportunities"""
    
    def __init__(self):
        self.improvement_patterns = self._load_improvement_patterns()
    
    def _load_improvement_patterns(self) -> Dict[str, Any]:
        """Load predefined patterns for identifying improvements"""
        return {
            "performance_thresholds": {
                "api_response_time_ms": 500,
                "database_query_time_ms": 100,
                "agent_execution_time_s": 30,
                "memory_usage_percent": 80,
                "cpu_usage_percent": 70
            },
            "usage_patterns": {
                "low_feature_adoption_threshold": 0.1,  # 10%
                "high_error_rate_threshold": 0.05,  # 5%
                "user_drop_off_threshold": 0.3  # 30%
            },
            "optimization_opportunities": {
                "cache_hit_ratio_threshold": 0.8,  # 80%
                "database_index_efficiency": 0.9,  # 90%
                "ai_agent_success_rate": 0.95  # 95%
            }
        }
    
    async def analyze_performance_issues(self, metrics: Dict[str, Any]) -> List[ImprovementTask]:
        """Analyze performance metrics and generate improvement tasks"""
        tasks = []
        
        try:
            api_health = metrics.get("api_health", {})
            db_performance = metrics.get("database_performance", {})
            agent_metrics = metrics.get("agent_metrics", {})
            
            # Check API response times
            avg_response_time = api_health.get("average_response_time_ms", 0)
            if avg_response_time > self.improvement_patterns["performance_thresholds"]["api_response_time_ms"]:
                tasks.append(ImprovementTask(
                    id=f"perf-api-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    title="Optimize API Response Times",
                    description=f"API average response time is {avg_response_time}ms, exceeding threshold of {self.improvement_patterns['performance_thresholds']['api_response_time_ms']}ms",
                    category=TaskCategory.PERFORMANCE,
                    priority=TaskPriority.HIGH,
                    estimated_effort="2-3 days",
                    impact_score=8.5,
                    confidence=0.9,
                    data_source="api_health_metrics",
                    metrics={"current_response_time": avg_response_time, "threshold": 500},
                    suggested_solution="Implement response caching, optimize database queries, add CDN for static assets",
                    dependencies=["database_optimization", "caching_layer"]
                ))
            
            # Check database performance
            slow_queries = db_performance.get("slow_queries_count", 0)
            if slow_queries > 10:
                tasks.append(ImprovementTask(
                    id=f"perf-db-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    title="Optimize Database Query Performance",
                    description=f"Detected {slow_queries} slow database queries in the last hour",
                    category=TaskCategory.PERFORMANCE,
                    priority=TaskPriority.MEDIUM,
                    estimated_effort="1-2 days",
                    impact_score=7.0,
                    confidence=0.85,
                    data_source="database_metrics",
                    metrics={"slow_queries_count": slow_queries},
                    suggested_solution="Add database indexes, optimize complex queries, implement query result caching",
                    dependencies=["database_analysis"]
                ))
            
            # Check AI agent performance
            agent_success_rate = agent_metrics.get("success_rate", 1.0)
            if agent_success_rate < self.improvement_patterns["optimization_opportunities"]["ai_agent_success_rate"]:
                tasks.append(ImprovementTask(
                    id=f"perf-agents-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    title="Improve AI Agent Reliability",
                    description=f"AI agent success rate is {agent_success_rate:.2%}, below target of 95%",
                    category=TaskCategory.PERFORMANCE,
                    priority=TaskPriority.HIGH,
                    estimated_effort="3-5 days",
                    impact_score=9.0,
                    confidence=0.95,
                    data_source="agent_metrics",
                    metrics={"success_rate": agent_success_rate, "target": 0.95},
                    suggested_solution="Add error handling, implement retry logic, optimize agent prompts",
                    dependencies=["agent_error_analysis", "prompt_optimization"]
                ))
                
        except Exception as e:
            logger.error(f"Error analyzing performance issues: {e}")
        
        return tasks
    
    async def analyze_usage_patterns(self, metrics: Dict[str, Any]) -> List[ImprovementTask]:
        """Analyze usage patterns and suggest UX improvements"""
        tasks = []
        
        try:
            user_activity = metrics.get("user_activity", {})
            feature_usage = metrics.get("feature_usage", {})
            
            # Check for underutilized features
            for feature, usage_rate in feature_usage.get("feature_adoption_rates", {}).items():
                if usage_rate < self.improvement_patterns["usage_patterns"]["low_feature_adoption_threshold"]:
                    tasks.append(ImprovementTask(
                        id=f"ux-feature-{feature}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                        title=f"Improve {feature.replace('_', ' ').title()} Feature Adoption",
                        description=f"Feature '{feature}' has low adoption rate of {usage_rate:.1%}",
                        category=TaskCategory.USER_EXPERIENCE,
                        priority=TaskPriority.MEDIUM,
                        estimated_effort="1-2 weeks",
                        impact_score=6.5,
                        confidence=0.8,
                        data_source="feature_usage_metrics",
                        metrics={"adoption_rate": usage_rate, "feature": feature},
                        suggested_solution="Improve feature discoverability, add onboarding tutorial, enhance UI/UX",
                        dependencies=["user_research", "ui_design"]
                    ))
            
            # Check user drop-off rates
            drop_off_rate = user_activity.get("session_drop_off_rate", 0)
            if drop_off_rate > self.improvement_patterns["usage_patterns"]["user_drop_off_threshold"]:
                tasks.append(ImprovementTask(
                    id=f"ux-retention-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    title="Reduce User Session Drop-off Rate",
                    description=f"User session drop-off rate is {drop_off_rate:.1%}, above threshold",
                    category=TaskCategory.USER_EXPERIENCE,
                    priority=TaskPriority.HIGH,
                    estimated_effort="2-3 weeks",
                    impact_score=8.0,
                    confidence=0.75,
                    data_source="user_activity_metrics", 
                    metrics={"drop_off_rate": drop_off_rate},
                    suggested_solution="Analyze user journey, improve onboarding, add engagement features",
                    dependencies=["user_journey_analysis", "engagement_features"]
                ))
                
        except Exception as e:
            logger.error(f"Error analyzing usage patterns: {e}")
        
        return tasks
    
    async def analyze_security_issues(self, metrics: Dict[str, Any]) -> List[ImprovementTask]:
        """Analyze security metrics and identify vulnerabilities"""
        tasks = []
        
        try:
            error_stats = metrics.get("error_stats", {})
            
            # Check for authentication failures
            auth_failures = error_stats.get("authentication_failures", 0)
            if auth_failures > 50:  # per hour
                tasks.append(ImprovementTask(
                    id=f"sec-auth-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    title="Investigate Authentication Failures",
                    description=f"High number of authentication failures: {auth_failures} in the last hour",
                    category=TaskCategory.SECURITY,
                    priority=TaskPriority.CRITICAL,
                    estimated_effort="1-2 days",
                    impact_score=9.5,
                    confidence=0.9,
                    data_source="security_metrics",
                    metrics={"auth_failures": auth_failures},
                    suggested_solution="Implement rate limiting, add CAPTCHA, investigate potential attacks",
                    dependencies=["security_analysis", "rate_limiting"]
                ))
            
            # Check for API abuse patterns
            rate_limit_hits = error_stats.get("rate_limit_violations", 0)
            if rate_limit_hits > 100:
                tasks.append(ImprovementTask(
                    id=f"sec-rate-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    title="Optimize Rate Limiting Strategy",
                    description=f"High rate limit violations: {rate_limit_hits} instances",
                    category=TaskCategory.SECURITY,
                    priority=TaskPriority.MEDIUM,
                    estimated_effort="1-2 days",
                    impact_score=6.0,
                    confidence=0.8,
                    data_source="api_security_metrics",
                    metrics={"rate_limit_hits": rate_limit_hits},
                    suggested_solution="Adjust rate limits, implement tiered limits, add user education",
                    dependencies=["rate_limit_analysis"]
                ))
                
        except Exception as e:
            logger.error(f"Error analyzing security issues: {e}")
        
        return tasks

class TaskPrioritizer:
    """Prioritizes and ranks improvement tasks"""
    
    def prioritize_tasks(self, tasks: List[ImprovementTask]) -> List[ImprovementTask]:
        """Prioritize tasks based on impact, priority, and confidence"""
        
        def priority_score(task: ImprovementTask) -> float:
            # Priority weights
            priority_weights = {
                TaskPriority.CRITICAL: 1.0,
                TaskPriority.HIGH: 0.8,
                TaskPriority.MEDIUM: 0.6,
                TaskPriority.LOW: 0.4
            }
            
            # Calculate composite score
            priority_weight = priority_weights.get(task.priority, 0.5)
            confidence_factor = task.confidence
            impact_factor = task.impact_score / 10.0
            
            return (priority_weight * 0.4 + impact_factor * 0.4 + confidence_factor * 0.2)
        
        return sorted(tasks, key=priority_score, reverse=True)

class WorkflowMonitor:
    """Main class orchestrating the workflow monitoring system"""
    
    def __init__(self, db_url: str, brain_api_url: str):
        self.db_url = db_url
        self.brain_api_url = brain_api_url
        self.metrics_collector = MetricsCollector(db_url, brain_api_url)
        self.workflow_analyzer = WorkflowAnalyzer()
        self.task_prioritizer = TaskPrioritizer()
        self.tasks_storage = []
        
    async def run_monitoring_cycle(self) -> List[ImprovementTask]:
        """Run a complete monitoring and analysis cycle"""
        logger.info("Starting workflow monitoring cycle...")
        
        try:
            # Collect metrics from all sources
            performance_metrics = await self.metrics_collector.collect_performance_metrics()
            usage_metrics = await self.metrics_collector.collect_usage_metrics()  
            error_metrics = await self.metrics_collector.collect_error_metrics()
            
            # Analyze metrics and generate tasks
            performance_tasks = await self.workflow_analyzer.analyze_performance_issues(performance_metrics)
            usage_tasks = await self.workflow_analyzer.analyze_usage_patterns(usage_metrics)
            security_tasks = await self.workflow_analyzer.analyze_security_issues(error_metrics)
            
            # Combine and prioritize all tasks
            all_tasks = performance_tasks + usage_tasks + security_tasks
            prioritized_tasks = self.task_prioritizer.prioritize_tasks(all_tasks)
            
            # Store tasks
            self.tasks_storage.extend(prioritized_tasks)
            
            logger.info(f"Generated {len(prioritized_tasks)} improvement tasks")
            return prioritized_tasks
            
        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}")
            return []
    
    async def get_pending_tasks(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get pending improvement tasks"""
        pending_tasks = [task for task in self.tasks_storage if task.status == "pending"]
        return [asdict(task) for task in pending_tasks[:limit]]
    
    async def update_task_status(self, task_id: str, status: str) -> bool:
        """Update the status of a specific task"""
        for task in self.tasks_storage:
            if task.id == task_id:
                task.status = status
                return True
        return False
    
    async def get_task_summary(self) -> Dict[str, Any]:
        """Get summary of all tasks by category and priority"""
        summary = {
            "total_tasks": len(self.tasks_storage),
            "by_priority": {},
            "by_category": {},
            "by_status": {}
        }
        
        for task in self.tasks_storage:
            # Count by priority
            priority = task.priority.value
            summary["by_priority"][priority] = summary["by_priority"].get(priority, 0) + 1
            
            # Count by category
            category = task.category.value
            summary["by_category"][category] = summary["by_category"].get(category, 0) + 1
            
            # Count by status
            status = task.status
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        
        return summary

# Global monitor instance
workflow_monitor = None

async def initialize_workflow_monitor(db_url: str, brain_api_url: str) -> WorkflowMonitor:
    """Initialize the global workflow monitor"""
    global workflow_monitor
    workflow_monitor = WorkflowMonitor(db_url, brain_api_url)
    return workflow_monitor

async def run_continuous_monitoring(interval_minutes: int = 30):
    """Run continuous monitoring in background"""
    global workflow_monitor
    
    if not workflow_monitor:
        logger.error("Workflow monitor not initialized")
        return
    
    while True:
        try:
            await workflow_monitor.run_monitoring_cycle()
            logger.info(f"Completed monitoring cycle, sleeping for {interval_minutes} minutes")
            await asyncio.sleep(interval_minutes * 60)
        except Exception as e:
            logger.error(f"Error in continuous monitoring: {e}")
            await asyncio.sleep(300)  # Wait 5 minutes before retry

if __name__ == "__main__":
    # Example usage
    import os
    
    db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/bizosaas")
    brain_api_url = os.getenv("BRAIN_API_URL", "http://localhost:8001")
    
    async def main():
        monitor = await initialize_workflow_monitor(db_url, brain_api_url)
        tasks = await monitor.run_monitoring_cycle()
        
        print(f"\nGenerated {len(tasks)} improvement tasks:")
        for i, task in enumerate(tasks[:5], 1):
            print(f"\n{i}. {task.title}")
            print(f"   Priority: {task.priority.value}")
            print(f"   Impact: {task.impact_score}/10")
            print(f"   Effort: {task.estimated_effort}")
            print(f"   Description: {task.description}")
    
    asyncio.run(main())