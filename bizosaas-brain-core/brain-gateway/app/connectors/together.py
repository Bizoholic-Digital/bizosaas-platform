import httpx
import logging
from typing import Dict, Any
from .base import ConnectorConfig, ConnectorType
from .llm import LLMBaseConnector
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class TogetherAIConnector(LLMBaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="together_ai",
            name="Together AI",
            type=ConnectorType.OTHER,
            description="Inference & Fine-tuning for open models (Llama 3, Mistral)",
            icon="together",
            auth_schema={
                "api_key": {"type": "string", "description": "Together AI API Key"}
            }
        )

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        if not api_key:
            return False
            
        async with httpx.AsyncClient() as client:
            try:
                # Together AI has an account endpoint or models endpoint
                response = await client.get(
                    "https://api.together.xyz/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Together AI validation failed: {e}")
                return False

    async def _chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        api_key = self.credentials.get("api_key")
        messages = payload.get("messages", [])
        # Default to Llama 3.1 8B 
        model = payload.get("model", "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")
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
                    "https://api.together.xyz/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json=data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Together AI chat failed: {e}")
                return {"error": str(e)}

    # Fine-tuning methods (to be used by fine_tuning_pipeline.py)
    async def create_fine_tune_job(self, training_file_id: str, model: str, n_epochs: int = 3) -> Dict[str, Any]:
        """Start a fine-tuning job via Together AI API"""
        api_key = self.credentials.get("api_key")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.together.xyz/v1/fine-tunes",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "training_file": training_file_id,
                        "model": model,
                        "n_epochs": n_epochs,
                        "wandb_api_key": None # Optional integration
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Together AI fine-tune create failed: {e}")
                raise

    async def upload_file(self, file_path: str) -> Dict[str, Any]:
        """Upload a JSONL file for training"""
        api_key = self.credentials.get("api_key")
        async with httpx.AsyncClient() as client:
            try:
                with open(file_path, "rb") as f:
                    files = {"file": ("training_data.jsonl", f, "application/jsonl")}
                    response = await client.post(
                        "https://api.together.xyz/v1/files",
                        headers={"Authorization": f"Bearer {api_key}"},
                        data={"purpose": "fine-tune"},
                        files=files,
                        timeout=120.0
                    )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Together AI file upload failed: {e}")
                raise
