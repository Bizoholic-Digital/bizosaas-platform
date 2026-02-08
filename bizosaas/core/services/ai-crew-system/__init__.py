"""
BizOSaaS AI Crew System - Hierarchical Agent Orchestration

This module provides a comprehensive AI agentic system for intelligent task automation
throughout the BizOSaaS platform using CrewAI for sophisticated multi-agent workflows.
"""

from .crew_orchestrator import CrewOrchestrator
from .agent_hierarchy import (
    SupervisorAgent,
    SpecialistAgent, 
    WorkerAgent,
    AgentHierarchy
)
from .smart_delegation import SmartDelegationEngine
from .crew_integration import CrewAIIntegration
from .performance_monitor import CrewPerformanceMonitor

__version__ = "1.0.0"
__author__ = "BizOSaaS Platform"

__all__ = [
    "CrewOrchestrator",
    "SupervisorAgent",
    "SpecialistAgent", 
    "WorkerAgent",
    "AgentHierarchy",
    "SmartDelegationEngine",
    "CrewAIIntegration",
    "CrewPerformanceMonitor"
]