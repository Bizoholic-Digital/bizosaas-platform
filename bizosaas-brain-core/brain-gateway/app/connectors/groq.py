import httpx
import logging
from typing import Dict, Any
from .base import ConnectorConfig, ConnectorType
from .llm import LLMBaseConnector
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class GroqConnector(LLMBaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="groq",
            name="Groq",
            type=ConnectorType.OTHER,
            description="Ultra-fast inference for Llama 3.1 & Mixtral via Groq",
            icon="groq",
            auth_schema={
                "api_key": {"type": "string", "description": "Groq API Key (gsk_...)"}
            }
        )

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        if not api_key:
            return False
            
        async with httpx.AsyncClient() as client:
            try:
                # Groq is OpenAI-compatible, check models
                response = await client.get(
                    "https://api.groq.com/openai/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Groq validation failed: {e}")
                return False

    async def _chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        api_key = self.credentials.get("api_key")
        messages = payload.get("messages", [])
        # Default to Llama 3.1 70B if not specified
        model = payload.get("model", "llama-3.1-70b-versatile")
        temperature = payload.get("temperature", 0.7)
        max_tokens = payload.get("max_tokens", 1024)
        response_format = payload.get("response_format", None)
        
        async with httpx.AsyncClient() as client:
            try:
                data = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                if response_format:
                    data["response_format"] = response_format
                    
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json=data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Groq chat failed: {e}")
                return {"error": str(e)}
