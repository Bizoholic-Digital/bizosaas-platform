"""
BizOSaaS CrewAI Agent Workers
Distributed agent workers for task processing with RabbitMQ and Kafka
"""

from .base_worker import CrewAIWorker

__all__ = ['CrewAIWorker']
