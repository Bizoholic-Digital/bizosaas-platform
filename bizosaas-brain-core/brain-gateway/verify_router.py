import asyncio
import json
import logging
import sys
import os

# Mock dependencies to test logic without full environment
class MockAgentTaskRequest:
    def __init__(self, agent_name, task_type, config):
        self.agent_name = agent_name
        self.task_type = task_type
        self.config = config
        self.task_id = "test-id"
        self.tenant_id = "test-tenant"

def _select_llm_config(agent_type: str, task_description: str):
    """Router logic from intelligence.py"""
    speed_optimized_tasks = [
        "content_creator", "seo_specialist", "social_media_specialist",
        "quality_scorer", "meta_tag_generator"
    ]
    reasoning_heavy_tasks = [
        "marketing_strategist", "competitive_analysis_specialist",
        "brand_positioning_specialist", "master_orchestrator"
    ]
    
    if agent_type in speed_optimized_tasks:
        return {"model_provider": "groq", "model_name": "llama-3.1-70b-versatile"}
    elif agent_type in reasoning_heavy_tasks:
        return {"model_provider": "openrouter", "model_name": "openai/gpt-4o"}
    return {"model_provider": "openrouter", "model_name": "openai/gpt-4o-mini"}

def test_router():
    print("--- Testing Router Logic ---")
    test_cases = [
        ("content_creator", "Generate blog post"),
        ("marketing_strategist", "Develop Q3 strategy"),
        ("unknown_agent", "Just a test")
    ]
    
    for agent, desc in test_cases:
        config = _select_llm_config(agent, desc)
        print(f"Agent: {agent} -> Provider: {config['model_provider']}, Model: {config['model_name']}")

if __name__ == "__main__":
    test_router()
