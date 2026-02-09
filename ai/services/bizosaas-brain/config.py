"""
Configuration management for BizOSaaS Brain
Handles API keys, Elasticsearch, and provider configuration
"""

import os
from typing import Optional
from elasticsearch_rag_setup import ElasticsearchRAGManager
import logging

logger = logging.getLogger(__name__)

# ==================== ELASTICSEARCH ====================

_elasticsearch_manager = None


def get_elasticsearch_manager() -> ElasticsearchRAGManager:
    """Get or create Elasticsearch manager singleton"""
    global _elasticsearch_manager

    if _elasticsearch_manager is None:
        elasticsearch_url = os.getenv(
            "ELASTICSEARCH_URL",
            "http://elasticsearch:9200"
        )

        _elasticsearch_manager = ElasticsearchRAGManager(
            elasticsearch_url=elasticsearch_url,
            index_prefix="bizosaas"
        )

        logger.info(f"Elasticsearch manager initialized: {elasticsearch_url}")

    return _elasticsearch_manager


# ==================== API KEYS ====================

from vault_client import get_vault_client

def get_provider_api_key(provider: str) -> str:
    """Get API key for specific provider from Vault or environment"""

    key_map = {
        "deepseek": "DEEPSEEK_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "cohere": "COHERE_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "gemini": "GOOGLE_API_KEY",
        "bedrock": "AWS_ACCESS_KEY_ID",  # Also needs AWS_SECRET_ACCESS_KEY
        "azure-openai": "AZURE_OPENAI_API_KEY",
        "vertex-ai": "GOOGLE_CLOUD_PROJECT",  # Uses service account
        "perplexity": "PERPLEXITY_API_KEY",
        "huggingface": "HUGGINGFACE_API_KEY"
    }

    env_var = key_map.get(provider)
    if not env_var:
        raise ValueError(f"Unknown provider: {provider}")

    # Try Vault first
    try:
        vault = get_vault_client()
        ai_secrets = vault.get_ai_config()
        if ai_secrets and env_var in ai_secrets:
            return ai_secrets[env_var]
    except Exception as e:
        logger.warning(f"Failed to fetch from Vault for {provider}: {e}")

    # Fallback to environment
    api_key = os.getenv(env_var)
    if not api_key:
        logger.warning(f"API key not found for {provider}: {env_var}")
        return ""

    return api_key


def get_cohere_api_key() -> str:
    """Get Cohere API key for RAG reranking"""
    return get_provider_api_key("cohere")


# ==================== CONFIGURATION ====================

class Config:
    """Application configuration"""

    # Elasticsearch
    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
    ELASTICSEARCH_INDEX_PREFIX = os.getenv("ELASTICSEARCH_INDEX_PREFIX", "bizosaas")

    # Monitoring
    PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9090"))
    GRAFANA_PORT = int(os.getenv("GRAFANA_PORT", "3030"))
    KIBANA_PORT = int(os.getenv("KIBANA_PORT", "5601"))

    # Brain API
    BRAIN_API_URL = os.getenv("BRAIN_API_URL", "http://localhost:8001")

    # Vault
    VAULT_ADDR = os.getenv("VAULT_ADDR", "http://vault:8200")
    VAULT_TOKEN = os.getenv("VAULT_TOKEN", "")

    # Feature flags
    ENABLE_MONITORING = os.getenv("ENABLE_MONITORING", "true").lower() == "true"
    ENABLE_RAG = os.getenv("ENABLE_RAG", "true").lower() == "true"
    ENABLE_SMART_ROUTING = os.getenv("ENABLE_SMART_ROUTING", "true").lower() == "true"

    # Cost limits
    DAILY_COST_LIMIT = float(os.getenv("DAILY_COST_LIMIT", "100.0"))
    MONTHLY_COST_LIMIT = float(os.getenv("MONTHLY_COST_LIMIT", "3000.0"))


config = Config()
