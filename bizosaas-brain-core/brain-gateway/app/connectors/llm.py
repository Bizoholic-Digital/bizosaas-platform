import httpx
import logging
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

class LLMBaseConnector(BaseConnector):
    """Base class for LLM connectors to share common logic"""
    
    async def get_status(self) -> ConnectorStatus:
        try:
            is_valid = await self.validate_credentials()
            return ConnectorStatus.CONNECTED if is_valid else ConnectorStatus.ERROR
        except Exception:
            return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # LLM connectors don't typically "sync" data in the traditional sense
        return {"data": [], "message": "Manual sync not supported for LLM connectors"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # LLM actions are typically chat or completion
        if action == "chat":
            return await self._chat(payload)
        return {"status": "error", "message": f"Action {action} not supported"}

    async def _chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

@ConnectorRegistry.register
class OpenAIConnector(LLMBaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="openai",
            name="OpenAI",
            type=ConnectorType.OTHER,
            description="OpenAI LLM services (GPT-4, GPT-3.5)",
            icon="openai",
            auth_schema={
                "api_key": {"type": "string", "description": "OpenAI API Key (sk-...)"},
                "organization": {"type": "string", "description": "Optional Organization ID", "required": False}
            }
        )

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        if not api_key:
            return False
            
        async with httpx.AsyncClient() as client:
            try:
                # Lightweight call to list models to validate key
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"OpenAI validation failed: {e}")
                return False

@ConnectorRegistry.register
class AnthropicConnector(LLMBaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="anthropic",
            name="Anthropic Claude",
            type=ConnectorType.OTHER,
            description="Anthropic Claude LLM services",
            icon="anthropic",
            auth_schema={
                "api_key": {"type": "string", "description": "Anthropic API Key (sk-ant-...)"}
            }
        )

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        if not api_key:
            return False
            
        async with httpx.AsyncClient() as client:
            try:
                # Anthropic doesn't have a simple "list models" like OpenAI for validation
                # We'll try a minimal completion or check headers
                # For now, let's use their messages API with a tiny prompt
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 1,
                        "messages": [{"role": "user", "content": "Hello"}]
                    },
                    timeout=10.0
                )
                # 400 Bad Request might happen if model is wrong, but 401 is auth failure
                return response.status_code != 401
            except Exception as e:
                logger.error(f"Anthropic validation failed: {e}")
                return False

@ConnectorRegistry.register
class OpenRouterConnector(LLMBaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="openrouter",
            name="OpenRouter",
            type=ConnectorType.OTHER,
            description="Unified API for multiple LLMs via OpenRouter",
            icon="openrouter",
            auth_schema={
                "api_key": {"type": "string", "description": "OpenRouter API Key (sk-or-...)"}
            }
        )

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        if not api_key:
            return False
            
        async with httpx.AsyncClient() as client:
            try:
                # OpenRouter has an endpoint to check key info
                response = await client.get(
                    "https://openrouter.ai/api/v1/auth/key",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"OpenRouter validation failed: {e}")
                return False

@ConnectorRegistry.register
class GoogleAIConnector(LLMBaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google_ai",
            name="Google AI (Gemini)",
            type=ConnectorType.OTHER,
            description="Google Gemini LLM services",
            icon="google",
            auth_schema={
                "api_key": {"type": "string", "description": "Google AI API Key"}
            }
        )

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        if not api_key:
            return False
            
        async with httpx.AsyncClient() as client:
            try:
                # Check models for Gemini
                response = await client.get(
                    f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
                    timeout=10.0
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Google AI validation failed: {e}")
                return False
