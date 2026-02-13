import httpx
import base64
import logging
from typing import Dict, Any, List, Optional
from app.core.vault import get_config_val

logger = logging.getLogger(__name__)

class DataforSEOClient:
    """
    Client for DataforSEO API.
    Provides methods for keyword research, backlink analysis, and on-page audits.
    """
    BASE_URL = "https://api.dataforseo.com/v3"

    def __init__(self):
        self.username = get_config_val("DATAFORSEO_USERNAME")
        self.password = get_config_val("DATAFORSEO_PASSWORD")
        self._auth_header = None
        if self.username and self.password:
            auth_bytes = f"{self.username}:{self.password}".encode("ascii")
            self._auth_header = f"Basic {base64.b64encode(auth_bytes).decode('ascii')}"

    async def _post(self, endpoint: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self._auth_header:
            logger.error("DataforSEO credentials missing")
            return {"status_code": 401, "status_message": "Missing credentials", "tasks": []}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.BASE_URL}/{endpoint}",
                    headers={"Authorization": self._auth_header, "Content-Type": "application/json"},
                    json=data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"DataforSEO API error at {endpoint}: {e}")
                return {"status_code": 500, "status_message": str(e), "tasks": []}

    async def get_keyword_data(self, keywords: List[str], location_code: int = 2840, language_code: str = "en") -> List[Dict[str, Any]]:
        """Get search volume and CPC data for keywords."""
        tasks = []
        for kw in keywords:
            tasks.append({
                "keywords": [kw],
                "location_code": location_code,
                "language_code": language_code
            })
        
        response = await self._post("keywords_data/google/search_volume/live", tasks)
        results = []
        if response.get("status_code") == 20000:
            for task in response.get("tasks", []):
                if task.get("result"):
                    results.extend(task["result"])
        return results

    async def get_backlinks_summary(self, target: str) -> Dict[str, Any]:
        """Get summary of backlinks for a domain or page."""
        task = [{"target": target}]
        response = await self._post("backlinks/summary/live", task)
        if response.get("status_code") == 20000 and response.get("tasks"):
            result = response["tasks"][0].get("result")
            if result and len(result) > 0:
                return result[0]
        return {}

    async def get_serp_data(self, keyword: str, location_code: int = 2840, language_code: str = "en") -> List[Dict[str, Any]]:
        """Get Google SERP results for a keyword."""
        task = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "device": "desktop",
            "os": "windows"
        }]
        response = await self._post("serp/google/organic/live/regular", task)
        if response.get("status_code") == 20000 and response.get("tasks"):
            result = response["tasks"][0].get("result")
            if result and len(result) > 0:
                return result[0].get("items", [])
        return []

    async def post_on_page_task(self, target_url: str, max_pages: int = 1) -> Optional[str]:
        """Initiate an on-page audit task."""
        task = [{
            "target": target_url,
            "max_pages": max_pages,
            "enable_javascript": True
        }]
        response = await self._post("on_page/task_post", task)
        if response.get("status_code") == 20000 and response.get("tasks"):
            return response["tasks"][0].get("id")
        return None

    async def get_on_page_results(self, task_id: str) -> Dict[str, Any]:
        """Get results of an on-page audit task."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/on_page/summary/{task_id}",
                    headers={"Authorization": self._auth_header}
                )
                response.raise_for_status()
                data = response.json()
                if data.get("status_code") == 20000 and data.get("tasks"):
                    result = data["tasks"][0].get("result")
                    if result and len(result) > 0:
                        return result[0]
                return {}
            except Exception as e:
                logger.error(f"DataforSEO On-Page results error: {e}")
                return {}

    async def get_keywords_suggestions(self, keywords: List[str], location_code: int = 2840, language_code: str = "en") -> List[Dict[str, Any]]:
        """Get keyword suggestions based on seed keywords."""
        tasks = []
        for kw in keywords:
            tasks.append({
                "keywords": [kw],
                "location_code": location_code,
                "language_code": language_code
            })
        
        response = await self._post("keywords_data/google/keywords_for_keywords/live", tasks)
        results = []
        if response.get("status_code") == 20000:
            for task in response.get("tasks", []):
                if task.get("result"):
                    results.extend(task["result"])
        return results

# Singleton instance
dataforseo_client = DataforSEOClient()
