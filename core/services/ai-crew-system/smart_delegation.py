"""
Smart Delegation Engine for BizOSaaS AI Crew System

This module implements intelligent task delegation logic that determines when to use
direct database/API calls vs AI agents vs full crew orchestration.
"""

from typing import Dict, Any, List, Optional, Tuple, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging
import re
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class TaskComplexity(Enum):
    """Task complexity levels"""
    SIMPLE = "simple"           # Direct DB/API calls
    MODERATE = "moderate"       # Single AI agent
    COMPLEX = "complex"         # Multi-agent coordination
    EXPERT = "expert"           # Full crew orchestration

class ExecutionStrategy(Enum):
    """Task execution strategies"""
    DIRECT_DB = "direct_db"           # Direct database operations
    DIRECT_API = "direct_api"         # Direct API calls
    SINGLE_AGENT = "single_agent"     # Single AI agent
    MULTI_AGENT = "multi_agent"       # Multiple AI agents
    CREW_WORKFLOW = "crew_workflow"   # Full crew orchestration

class TaskCategory(Enum):
    """Task categories for routing"""
    CRUD_OPERATION = "crud_operation"
    DATA_ANALYSIS = "data_analysis"
    CONTENT_GENERATION = "content_generation"
    DECISION_MAKING = "decision_making"
    WORKFLOW_AUTOMATION = "workflow_automation"
    INTEGRATION_TASK = "integration_task"
    REPORTING = "reporting"
    OPTIMIZATION = "optimization"

@dataclass
class TaskAnalysis:
    """Analysis result for task complexity and routing"""
    complexity: TaskComplexity
    strategy: ExecutionStrategy
    category: TaskCategory
    confidence: float
    reasoning: str
    estimated_cost: float
    estimated_time: int  # seconds
    required_capabilities: List[str]
    risk_level: str

@dataclass
class DelegationRule:
    """Rule for task delegation decisions"""
    name: str
    conditions: Dict[str, Any]
    action: ExecutionStrategy
    priority: int
    description: str

class TaskAnalyzer:
    """Analyzes tasks to determine complexity and execution strategy"""
    
    def __init__(self):
        self.complexity_indicators = {
            TaskComplexity.SIMPLE: {
                'keywords': ['get', 'list', 'read', 'fetch', 'retrieve', 'show'],
                'patterns': [r'^get_\w+', r'^list_\w+', r'^fetch_\w+'],
                'max_data_volume': 1000,
                'max_params': 5
            },
            TaskComplexity.MODERATE: {
                'keywords': ['create', 'update', 'delete', 'validate', 'process'],
                'patterns': [r'^create_\w+', r'^update_\w+', r'^process_\w+'],
                'max_data_volume': 10000,
                'max_params': 10
            },
            TaskComplexity.COMPLEX: {
                'keywords': ['analyze', 'optimize', 'recommend', 'generate', 'predict'],
                'patterns': [r'^analyze_\w+', r'^optimize_\w+', r'^generate_\w+'],
                'max_data_volume': 100000,
                'max_params': 20
            },
            TaskComplexity.EXPERT: {
                'keywords': ['orchestrate', 'workflow', 'coordinate', 'integrate'],
                'patterns': [r'^orchestrate_\w+', r'^workflow_\w+'],
                'max_data_volume': float('inf'),
                'max_params': float('inf')
            }
        }
        
        self.category_indicators = {
            TaskCategory.CRUD_OPERATION: {
                'keywords': ['create', 'read', 'update', 'delete', 'insert', 'select'],
                'patterns': [r'^(get|set|add|remove|delete)_\w+']
            },
            TaskCategory.DATA_ANALYSIS: {
                'keywords': ['analyze', 'calculate', 'aggregate', 'summarize', 'trend'],
                'patterns': [r'^(analyze|calc|summarize)_\w+']
            },
            TaskCategory.CONTENT_GENERATION: {
                'keywords': ['generate', 'create', 'write', 'compose', 'draft'],
                'patterns': [r'^(generate|create|write)_\w+_content']
            },
            TaskCategory.DECISION_MAKING: {
                'keywords': ['decide', 'choose', 'select', 'recommend', 'suggest'],
                'patterns': [r'^(recommend|suggest|decide)_\w+']
            },
            TaskCategory.WORKFLOW_AUTOMATION: {
                'keywords': ['automate', 'workflow', 'process', 'orchestrate'],
                'patterns': [r'^(automate|workflow)_\w+']
            },
            TaskCategory.INTEGRATION_TASK: {
                'keywords': ['sync', 'integrate', 'connect', 'import', 'export'],
                'patterns': [r'^(sync|integrate|import|export)_\w+']
            },
            TaskCategory.REPORTING: {
                'keywords': ['report', 'dashboard', 'metrics', 'analytics', 'insights'],
                'patterns': [r'^(report|dashboard)_\w+']
            },
            TaskCategory.OPTIMIZATION: {
                'keywords': ['optimize', 'improve', 'enhance', 'tune', 'refine'],
                'patterns': [r'^(optimize|improve|enhance)_\w+']
            }
        }
    
    def analyze_task(self, task_data: Dict[str, Any]) -> TaskAnalysis:
        """Analyze task to determine complexity and execution strategy"""
        
        task_type = task_data.get('type', '').lower()
        description = task_data.get('description', '').lower()
        data_volume = task_data.get('data_volume', 0)
        param_count = len(task_data.get('parameters', {}))
        requires_ai = task_data.get('requires_ai', False)
        multi_domain = task_data.get('multi_domain', False)
        
        # Analyze complexity
        complexity = self._analyze_complexity(
            task_type, description, data_volume, param_count, requires_ai, multi_domain
        )
        
        # Analyze category
        category = self._analyze_category(task_type, description)
        
        # Determine execution strategy
        strategy = self._determine_strategy(complexity, category, task_data)
        
        # Calculate confidence and other metrics
        confidence = self._calculate_confidence(task_data, complexity, category)
        estimated_cost = self._estimate_cost(strategy, complexity, data_volume)
        estimated_time = self._estimate_time(strategy, complexity, data_volume)
        required_capabilities = self._identify_capabilities(category, complexity)
        risk_level = self._assess_risk(strategy, complexity, data_volume)
        
        reasoning = self._generate_reasoning(
            complexity, strategy, category, task_data
        )
        
        return TaskAnalysis(
            complexity=complexity,
            strategy=strategy,
            category=category,
            confidence=confidence,
            reasoning=reasoning,
            estimated_cost=estimated_cost,
            estimated_time=estimated_time,
            required_capabilities=required_capabilities,
            risk_level=risk_level
        )
    
    def _analyze_complexity(
        self, 
        task_type: str, 
        description: str, 
        data_volume: int,
        param_count: int,
        requires_ai: bool,
        multi_domain: bool
    ) -> TaskComplexity:
        """Analyze task complexity based on various indicators"""
        
        # Force expert complexity for multi-domain tasks
        if multi_domain:
            return TaskComplexity.EXPERT
        
        # Force complex/expert for AI-required tasks
        if requires_ai:
            return TaskComplexity.COMPLEX if data_volume < 100000 else TaskComplexity.EXPERT
        
        # Analyze based on indicators
        text_to_analyze = f"{task_type} {description}"
        
        complexity_scores = {}
        
        for complexity, indicators in self.complexity_indicators.items():
            score = 0
            
            # Keyword matching
            for keyword in indicators['keywords']:
                if keyword in text_to_analyze:
                    score += 1
            
            # Pattern matching
            for pattern in indicators['patterns']:
                if re.search(pattern, text_to_analyze):
                    score += 2
            
            # Data volume check
            if data_volume <= indicators['max_data_volume']:
                score += 1
            
            # Parameter count check
            if param_count <= indicators['max_params']:
                score += 1
            
            complexity_scores[complexity] = score
        
        # Return complexity with highest score
        return max(complexity_scores.items(), key=lambda x: x[1])[0]
    
    def _analyze_category(self, task_type: str, description: str) -> TaskCategory:
        """Analyze task category based on type and description"""
        
        text_to_analyze = f"{task_type} {description}"
        
        category_scores = {}
        
        for category, indicators in self.category_indicators.items():
            score = 0
            
            # Keyword matching
            for keyword in indicators['keywords']:
                if keyword in text_to_analyze:
                    score += 1
            
            # Pattern matching
            for pattern in indicators['patterns']:
                if re.search(pattern, text_to_analyze):
                    score += 2
            
            category_scores[category] = score
        
        # Return category with highest score, default to CRUD_OPERATION
        if not category_scores or max(category_scores.values()) == 0:
            return TaskCategory.CRUD_OPERATION
        
        return max(category_scores.items(), key=lambda x: x[1])[0]
    
    def _determine_strategy(
        self, 
        complexity: TaskComplexity, 
        category: TaskCategory, 
        task_data: Dict[str, Any]
    ) -> ExecutionStrategy:
        """Determine execution strategy based on complexity and category"""
        
        # Strategy mapping based on complexity
        complexity_strategy_map = {
            TaskComplexity.SIMPLE: ExecutionStrategy.DIRECT_DB,
            TaskComplexity.MODERATE: ExecutionStrategy.SINGLE_AGENT,
            TaskComplexity.COMPLEX: ExecutionStrategy.MULTI_AGENT,
            TaskComplexity.EXPERT: ExecutionStrategy.CREW_WORKFLOW
        }
        
        # Category-specific overrides
        category_overrides = {
            TaskCategory.CRUD_OPERATION: ExecutionStrategy.DIRECT_DB,
            TaskCategory.INTEGRATION_TASK: ExecutionStrategy.DIRECT_API,
        }
        
        # Check for category override
        if category in category_overrides and complexity in [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]:
            return category_overrides[category]
        
        # Check for explicit strategy request
        requested_strategy = task_data.get('preferred_strategy')
        if requested_strategy and requested_strategy in [s.value for s in ExecutionStrategy]:
            return ExecutionStrategy(requested_strategy)
        
        return complexity_strategy_map[complexity]
    
    def _calculate_confidence(
        self, 
        task_data: Dict[str, Any], 
        complexity: TaskComplexity, 
        category: TaskCategory
    ) -> float:
        """Calculate confidence in the analysis"""
        
        confidence = 0.5  # Base confidence
        
        # Increase confidence for well-defined tasks
        if task_data.get('type'):
            confidence += 0.2
        
        if task_data.get('description'):
            confidence += 0.2
        
        # Increase confidence for explicit indicators
        if task_data.get('requires_ai') is not None:
            confidence += 0.1
        
        if task_data.get('multi_domain') is not None:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _estimate_cost(
        self, 
        strategy: ExecutionStrategy, 
        complexity: TaskComplexity, 
        data_volume: int
    ) -> float:
        """Estimate task execution cost"""
        
        base_costs = {
            ExecutionStrategy.DIRECT_DB: 0.001,
            ExecutionStrategy.DIRECT_API: 0.005,
            ExecutionStrategy.SINGLE_AGENT: 0.05,
            ExecutionStrategy.MULTI_AGENT: 0.15,
            ExecutionStrategy.CREW_WORKFLOW: 0.50
        }
        
        complexity_multiplier = {
            TaskComplexity.SIMPLE: 1.0,
            TaskComplexity.MODERATE: 2.0,
            TaskComplexity.COMPLEX: 4.0,
            TaskComplexity.EXPERT: 8.0
        }
        
        volume_multiplier = 1.0 + (data_volume / 10000)  # Increase cost with data volume
        
        return (
            base_costs[strategy] * 
            complexity_multiplier[complexity] * 
            volume_multiplier
        )
    
    def _estimate_time(
        self, 
        strategy: ExecutionStrategy, 
        complexity: TaskComplexity, 
        data_volume: int
    ) -> int:
        """Estimate task execution time in seconds"""
        
        base_times = {
            ExecutionStrategy.DIRECT_DB: 1,
            ExecutionStrategy.DIRECT_API: 5,
            ExecutionStrategy.SINGLE_AGENT: 30,
            ExecutionStrategy.MULTI_AGENT: 120,
            ExecutionStrategy.CREW_WORKFLOW: 300
        }
        
        complexity_multiplier = {
            TaskComplexity.SIMPLE: 1.0,
            TaskComplexity.MODERATE: 2.0,
            TaskComplexity.COMPLEX: 4.0,
            TaskComplexity.EXPERT: 8.0
        }
        
        volume_multiplier = 1.0 + (data_volume / 100000)  # Increase time with data volume
        
        return int(
            base_times[strategy] * 
            complexity_multiplier[complexity] * 
            volume_multiplier
        )
    
    def _identify_capabilities(
        self, 
        category: TaskCategory, 
        complexity: TaskComplexity
    ) -> List[str]:
        """Identify required capabilities for task execution"""
        
        category_capabilities = {
            TaskCategory.CRUD_OPERATION: ['database_access', 'data_validation'],
            TaskCategory.DATA_ANALYSIS: ['data_processing', 'statistical_analysis'],
            TaskCategory.CONTENT_GENERATION: ['nlp', 'content_creation'],
            TaskCategory.DECISION_MAKING: ['reasoning', 'pattern_recognition'],
            TaskCategory.WORKFLOW_AUTOMATION: ['process_orchestration', 'task_coordination'],
            TaskCategory.INTEGRATION_TASK: ['api_integration', 'data_transformation'],
            TaskCategory.REPORTING: ['data_visualization', 'report_generation'],
            TaskCategory.OPTIMIZATION: ['algorithm_optimization', 'performance_tuning']
        }
        
        complexity_capabilities = {
            TaskComplexity.SIMPLE: [],
            TaskComplexity.MODERATE: ['ai_reasoning'],
            TaskComplexity.COMPLEX: ['ai_reasoning', 'multi_step_planning'],
            TaskComplexity.EXPERT: ['ai_reasoning', 'multi_step_planning', 'coordination']
        }
        
        capabilities = category_capabilities.get(category, [])
        capabilities.extend(complexity_capabilities.get(complexity, []))
        
        return list(set(capabilities))  # Remove duplicates
    
    def _assess_risk(
        self, 
        strategy: ExecutionStrategy, 
        complexity: TaskComplexity, 
        data_volume: int
    ) -> str:
        """Assess risk level for task execution"""
        
        risk_score = 0
        
        # Strategy risk
        strategy_risk = {
            ExecutionStrategy.DIRECT_DB: 1,
            ExecutionStrategy.DIRECT_API: 2,
            ExecutionStrategy.SINGLE_AGENT: 3,
            ExecutionStrategy.MULTI_AGENT: 4,
            ExecutionStrategy.CREW_WORKFLOW: 5
        }
        risk_score += strategy_risk[strategy]
        
        # Complexity risk
        complexity_risk = {
            TaskComplexity.SIMPLE: 1,
            TaskComplexity.MODERATE: 2,
            TaskComplexity.COMPLEX: 3,
            TaskComplexity.EXPERT: 4
        }
        risk_score += complexity_risk[complexity]
        
        # Data volume risk
        if data_volume > 100000:
            risk_score += 2
        elif data_volume > 10000:
            risk_score += 1
        
        # Determine risk level
        if risk_score <= 3:
            return "low"
        elif risk_score <= 6:
            return "medium"
        else:
            return "high"
    
    def _generate_reasoning(
        self, 
        complexity: TaskComplexity, 
        strategy: ExecutionStrategy, 
        category: TaskCategory,
        task_data: Dict[str, Any]
    ) -> str:
        """Generate reasoning for the delegation decision"""
        
        reasoning_parts = []
        
        # Complexity reasoning
        reasoning_parts.append(f"Task complexity: {complexity.value}")
        
        # Category reasoning
        reasoning_parts.append(f"Task category: {category.value}")
        
        # Strategy reasoning
        strategy_reasons = {
            ExecutionStrategy.DIRECT_DB: "Simple database operation, no AI needed",
            ExecutionStrategy.DIRECT_API: "Straightforward API call, no AI processing required",
            ExecutionStrategy.SINGLE_AGENT: "Moderate complexity requires AI reasoning",
            ExecutionStrategy.MULTI_AGENT: "Complex task needs multiple AI agents",
            ExecutionStrategy.CREW_WORKFLOW: "Expert-level task requires full crew orchestration"
        }
        reasoning_parts.append(strategy_reasons[strategy])
        
        # Additional factors
        if task_data.get('multi_domain'):
            reasoning_parts.append("Multi-domain task requires coordination")
        
        if task_data.get('data_volume', 0) > 10000:
            reasoning_parts.append("Large data volume increases complexity")
        
        return "; ".join(reasoning_parts)

class SmartDelegationEngine:
    """Main engine for smart task delegation decisions"""
    
    def __init__(self):
        self.task_analyzer = TaskAnalyzer()
        self.delegation_rules = self._initialize_delegation_rules()
        self.execution_history: List[Dict[str, Any]] = []
        self.performance_cache: Dict[str, Dict[str, Any]] = {}
    
    def _initialize_delegation_rules(self) -> List[DelegationRule]:
        """Initialize delegation rules"""
        
        return [
            DelegationRule(
                name="simple_crud_rule",
                conditions={
                    "category": TaskCategory.CRUD_OPERATION,
                    "complexity": TaskComplexity.SIMPLE,
                    "data_volume": {"max": 1000}
                },
                action=ExecutionStrategy.DIRECT_DB,
                priority=10,
                description="Route simple CRUD operations directly to database"
            ),
            DelegationRule(
                name="api_integration_rule",
                conditions={
                    "category": TaskCategory.INTEGRATION_TASK,
                    "type_contains": ["sync", "import", "export"]
                },
                action=ExecutionStrategy.DIRECT_API,
                priority=9,
                description="Route API integration tasks to direct API calls"
            ),
            DelegationRule(
                name="ai_required_rule",
                conditions={
                    "requires_ai": True
                },
                action=ExecutionStrategy.SINGLE_AGENT,
                priority=8,
                description="Use AI agent when explicitly required"
            ),
            DelegationRule(
                name="multi_domain_rule",
                conditions={
                    "multi_domain": True
                },
                action=ExecutionStrategy.CREW_WORKFLOW,
                priority=7,
                description="Use crew workflow for multi-domain tasks"
            ),
            DelegationRule(
                name="high_volume_rule",
                conditions={
                    "data_volume": {"min": 100000}
                },
                action=ExecutionStrategy.MULTI_AGENT,
                priority=6,
                description="Use multi-agent for high volume processing"
            ),
            DelegationRule(
                name="content_generation_rule",
                conditions={
                    "category": TaskCategory.CONTENT_GENERATION
                },
                action=ExecutionStrategy.SINGLE_AGENT,
                priority=5,
                description="Use AI agent for content generation tasks"
            ),
            DelegationRule(
                name="decision_making_rule",
                conditions={
                    "category": TaskCategory.DECISION_MAKING,
                    "complexity": [TaskComplexity.COMPLEX, TaskComplexity.EXPERT]
                },
                action=ExecutionStrategy.MULTI_AGENT,
                priority=4,
                description="Use multi-agent for complex decision making"
            )
        ]
    
    async def delegate_task(self, task_data: Dict[str, Any]) -> Tuple[ExecutionStrategy, TaskAnalysis]:
        """Main delegation method that determines how to execute a task"""
        
        # Analyze the task
        analysis = self.task_analyzer.analyze_task(task_data)
        
        # Apply delegation rules
        strategy = self._apply_delegation_rules(task_data, analysis)
        
        # Override with rule-based strategy if found
        if strategy:
            analysis.strategy = strategy
        
        # Log delegation decision
        await self._log_delegation_decision(task_data, analysis)
        
        return analysis.strategy, analysis
    
    def _apply_delegation_rules(
        self, 
        task_data: Dict[str, Any], 
        analysis: TaskAnalysis
    ) -> Optional[ExecutionStrategy]:
        """Apply delegation rules to determine strategy"""
        
        # Sort rules by priority (highest first)
        sorted_rules = sorted(self.delegation_rules, key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            if self._rule_matches(rule, task_data, analysis):
                logger.info(f"Applied delegation rule: {rule.name}")
                return rule.action
        
        return None
    
    def _rule_matches(
        self, 
        rule: DelegationRule, 
        task_data: Dict[str, Any], 
        analysis: TaskAnalysis
    ) -> bool:
        """Check if a delegation rule matches the task"""
        
        conditions = rule.conditions
        
        # Check category condition
        if "category" in conditions:
            if analysis.category != conditions["category"]:
                return False
        
        # Check complexity condition
        if "complexity" in conditions:
            complexity_condition = conditions["complexity"]
            if isinstance(complexity_condition, list):
                if analysis.complexity not in complexity_condition:
                    return False
            else:
                if analysis.complexity != complexity_condition:
                    return False
        
        # Check data volume condition
        if "data_volume" in conditions:
            volume_condition = conditions["data_volume"]
            task_volume = task_data.get("data_volume", 0)
            
            if "min" in volume_condition and task_volume < volume_condition["min"]:
                return False
            if "max" in volume_condition and task_volume > volume_condition["max"]:
                return False
        
        # Check type contains condition
        if "type_contains" in conditions:
            task_type = task_data.get("type", "").lower()
            type_keywords = conditions["type_contains"]
            if not any(keyword in task_type for keyword in type_keywords):
                return False
        
        # Check boolean conditions
        boolean_conditions = ["requires_ai", "multi_domain"]
        for condition in boolean_conditions:
            if condition in conditions:
                if task_data.get(condition) != conditions[condition]:
                    return False
        
        return True
    
    async def _log_delegation_decision(
        self, 
        task_data: Dict[str, Any], 
        analysis: TaskAnalysis
    ):
        """Log delegation decision for monitoring and optimization"""
        
        decision_log = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_data.get("id", "unknown"),
            "task_type": task_data.get("type", "unknown"),
            "strategy": analysis.strategy.value,
            "complexity": analysis.complexity.value,
            "category": analysis.category.value,
            "confidence": analysis.confidence,
            "estimated_cost": analysis.estimated_cost,
            "estimated_time": analysis.estimated_time,
            "reasoning": analysis.reasoning
        }
        
        self.execution_history.append(decision_log)
        
        # Keep only last 1000 decisions
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-1000:]
        
        logger.info(f"Delegation decision: {analysis.strategy.value} for {task_data.get('type', 'unknown')}")
    
    def get_delegation_statistics(self) -> Dict[str, Any]:
        """Get statistics about delegation decisions"""
        
        if not self.execution_history:
            return {"message": "No delegation history available"}
        
        total_decisions = len(self.execution_history)
        
        # Strategy distribution
        strategy_counts = {}
        for decision in self.execution_history:
            strategy = decision["strategy"]
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        # Complexity distribution
        complexity_counts = {}
        for decision in self.execution_history:
            complexity = decision["complexity"]
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
        
        # Average confidence
        avg_confidence = sum(d["confidence"] for d in self.execution_history) / total_decisions
        
        # Average costs and times
        avg_cost = sum(d["estimated_cost"] for d in self.execution_history) / total_decisions
        avg_time = sum(d["estimated_time"] for d in self.execution_history) / total_decisions
        
        return {
            "total_decisions": total_decisions,
            "strategy_distribution": strategy_counts,
            "complexity_distribution": complexity_counts,
            "average_confidence": avg_confidence,
            "average_estimated_cost": avg_cost,
            "average_estimated_time": avg_time,
            "recent_decisions": self.execution_history[-10:]  # Last 10 decisions
        }
    
    def add_delegation_rule(self, rule: DelegationRule):
        """Add a new delegation rule"""
        self.delegation_rules.append(rule)
        # Re-sort by priority
        self.delegation_rules.sort(key=lambda r: r.priority, reverse=True)
    
    def remove_delegation_rule(self, rule_name: str) -> bool:
        """Remove a delegation rule by name"""
        for i, rule in enumerate(self.delegation_rules):
            if rule.name == rule_name:
                del self.delegation_rules[i]
                return True
        return False
    
    def update_rule_priority(self, rule_name: str, new_priority: int) -> bool:
        """Update the priority of a delegation rule"""
        for rule in self.delegation_rules:
            if rule.name == rule_name:
                rule.priority = new_priority
                # Re-sort by priority
                self.delegation_rules.sort(key=lambda r: r.priority, reverse=True)
                return True
        return False

# Global instance
smart_delegation_engine = SmartDelegationEngine()