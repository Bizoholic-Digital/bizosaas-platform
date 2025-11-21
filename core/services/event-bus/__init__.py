"""
BizOSaaS Event Bus Package

Domain Event Bus for BizOSaaS Platform - AI Agent Coordination & Event-Driven Architecture
"""

from domain_events import BaseEvent, EventStatus, EventPriority, EventCategory, create_event
from event_bus import EventBus, EventBusConfig
from client_sdk import EventBusClient, EventBusClientConfig
from tenant_isolation import TenantContext

__version__ = "1.0.0"
__author__ = "BizOSaaS Platform Team"
__description__ = "Domain Event Bus for AI Agent Coordination"

__all__ = [
    "BaseEvent",
    "EventStatus", 
    "EventPriority",
    "EventCategory",
    "create_event",
    "EventBus",
    "EventBusConfig",
    "EventBusClient",
    "EventBusClientConfig",
    "TenantContext"
]