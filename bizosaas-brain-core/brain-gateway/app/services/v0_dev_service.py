import httpx
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class V0DevService:
    """
    Service for interacting with the V0.dev API (by Vercel).
    Handles screenshot-to-React generation and UI refinement.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("V0_DEV_API_KEY")
        self.base_url = "https://api.v0.dev/v1"

    async def generate_from_screenshot(self, image_url: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generates React code from a screenshot image URL.
        """
        if not self.api_key:
            raise ValueError("V0_DEV_API_KEY not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "image_url": image_url,
            "prompt": prompt or "Generate a high-fidelity React component from this screenshot using Tailwind CSS.",
            "format": "react",
            "styling": "tailwind"
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{self.base_url}/generate", json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"V0.dev generation failed: {e}")
                raise

    async def refine_ui(self, code: str, refinement_prompt: str) -> Dict[str, Any]:
        """
        Refines existing UI code based on a prompt.
        """
        if not self.api_key:
            raise ValueError("V0_DEV_API_KEY not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "code": code,
            "prompt": refinement_prompt
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{self.base_url}/refine", json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"V0.dev refinement failed: {e}")
                raise
