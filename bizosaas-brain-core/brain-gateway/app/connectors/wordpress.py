import httpx
import base64
import logging
from typing import Dict, Any, List, Optional
from ..ports.cms_port import CMSPort, Page, Post, CMSStats
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class WordPressConnector(BaseConnector, CMSPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="wordpress",
            name="WordPress",
            type=ConnectorType.CMS,
            description="Connect your WordPress site to sync content and media.",
            icon="wordpress",
            version="2.0.0",
            auth_schema={
                "url": {"type": "string", "label": "WordPress Site URL", "placeholder": "https://your-site.com"},
                "username": {"type": "string", "label": "Username"},
                "application_password": {"type": "string", "label": "Application Password", "help": "Generate in Users > Profile"}
            }
        )

    def _get_auth_header(self) -> Dict[str, str]:
        username = self.credentials.get("username")
        password = self.credentials.get("application_password")
        if not username or not password:
            return {}
        credentials = f"{username}:{password}"
        token = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {token}"}

    def _get_api_url(self, path: str) -> str:
        base_url = self.credentials.get("url", "").rstrip("/")
        if "wp-json" in base_url:
             return f"{base_url}/wp/v2/{path.lstrip('/')}"
        return f"{base_url}/wp-json/wp/v2/{path.lstrip('/')}"

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self._get_api_url("users/me"),
                    headers=self._get_auth_header(),
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Legacy sync support"""
        if resource_type == 'posts':
            items = await self.get_posts()
            return {"data": [p.dict() for p in items]}
        elif resource_type == 'pages':
            items = await self.get_pages()
            return {"data": [p.dict() for p in items]}
        return {"data": []}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy action support"""
        return {}

    # --- CMSPort Implementation ---
    async def get_stats(self) -> CMSStats:
        async with httpx.AsyncClient() as client:
            try:
                # Parallel fetch for headers to get totals
                # WordPress uses X-WP-Total header for counts
                auth = self._get_auth_header()
                stats = {"pages": 0, "posts": 0, "media": 0}
                
                endpoints = {
                    "pages": "pages", 
                    "posts": "posts", 
                    "media": "media"
                }
                
                for key, endpoint in endpoints.items():
                    try:
                        resp = await client.head(
                            self._get_api_url(endpoint), 
                            headers=auth, 
                            params={"per_page": 1}
                        )
                        if resp.status_code == 200:
                            stats[key] = int(resp.headers.get("X-WP-Total", 0))
                    except Exception:
                         pass

                return CMSStats(
                    pages=stats["pages"],
                    posts=stats["posts"],
                    media=stats["media"]
                )
            except Exception as e:
                logger.error(f"Stats fetch failed: {e}")
                return CMSStats(pages=0, posts=0, media=0)

    async def get_pages(self, limit: int = 100) -> List[Page]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("pages"),
                headers=self._get_auth_header(),
                params={"per_page": limit},
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()
            return [
                Page(
                    id=str(p["id"]),
                    title=p["title"]["rendered"],
                    slug=p["slug"],
                    content=p["content"]["rendered"],
                    status=p["status"],
                    author_id=str(p["author"])
                ) for p in data
            ]

    async def get_page(self, page_id: str) -> Optional[Page]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url(f"pages/{page_id}"),
                    headers=self._get_auth_header()
                )
                if response.status_code == 404: return None
                p = response.json()
                return Page(
                    id=str(p["id"]),
                    title=p["title"]["rendered"],
                    slug=p["slug"],
                    content=p["content"]["rendered"],
                    status=p["status"]
                )
            except Exception:
                return None

    async def create_page(self, page: Page) -> Page:
        payload = {
            "title": page.title,
            "content": page.content,
            "status": page.status,
            "slug": page.slug
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("pages"),
                headers=self._get_auth_header(),
                json=payload
            )
            response.raise_for_status()
            p = response.json()
            page.id = str(p["id"])
            return page
            
    async def update_page(self, page_id: str, updates: Dict[str, Any]) -> Page:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url(f"pages/{page_id}"),
                headers=self._get_auth_header(),
                json=updates
            )
            response.raise_for_status()
            # return updated page logic
            return await self.get_page(page_id)

    async def get_posts(self, limit: int = 100) -> List[Post]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("posts"),
                headers=self._get_auth_header(),
                params={"per_page": limit}
            )
            response.raise_for_status()
            data = response.json()
            return [
                Post(
                    id=str(p["id"]),
                    title=p["title"]["rendered"],
                    slug=p["slug"],
                    content=p["content"]["rendered"],
                    status=p["status"],
                    excerpt=p["excerpt"]["rendered"]
                ) for p in data
            ]

    async def get_post(self, post_id: str) -> Optional[Post]:
        # Implementation similar to get_page
        return None

    async def create_post(self, post: Post) -> Post:
        # Implementation similar to create_page
        return post

    async def update_post(self, post_id: str, updates: Dict[str, Any]) -> Post:
        return Post(title="Updated", slug="updated", content="") # Mock

    async def delete_post(self, post_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._get_api_url(f"posts/{post_id}"),
                headers=self._get_auth_header()
            )
            return response.status_code == 200
