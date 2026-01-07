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
        url = self.credentials.get("url", "")
        if not url:
            logger.error("WordPress validation failed: Missing site URL")
            return False
            
        try:
            async with httpx.AsyncClient() as client:
                api_url = self._get_api_url("users/me")
                logger.info(f"Validating WordPress connection to: {api_url}")
                
                response = await client.get(
                    api_url,
                    headers=self._get_auth_header(),
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    logger.info("WordPress connection validated successfully")
                    return True
                else:
                    logger.error(f"WordPress validation failed: HTTP {response.status_code} - {response.text[:100]}")
                    return False
        except httpx.ConnectError:
            logger.error(f"WordPress validation failed: Could not connect to {url}")
            return False
        except Exception as e:
            logger.error(f"WordPress validation failed: {str(e)}")
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
            p = response.json()
            return Page(
                id=str(p["id"]),
                title=p["title"]["rendered"],
                slug=p["slug"],
                content=p["content"]["rendered"],
                status=p["status"]
            )

    async def delete_page(self, page_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._get_api_url(f"pages/{page_id}"),
                headers=self._get_auth_header(),
                params={"force": "true"}
            )
            return response.status_code in [200, 204]

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
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url(f"posts/{post_id}"),
                    headers=self._get_auth_header()
                )
                if response.status_code == 404: return None
                p = response.json()
                return Post(
                    id=str(p["id"]),
                    title=p["title"]["rendered"],
                    slug=p["slug"],
                    content=p["content"]["rendered"],
                    status=p["status"],
                    excerpt=p["excerpt"]["rendered"]
                )
            except Exception:
                return None

    async def create_post(self, post: Post) -> Post:
        payload = {
            "title": post.title,
            "content": post.content,
            "status": post.status or "publish",
            "slug": post.slug
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("posts"),
                headers=self._get_auth_header(),
                json=payload
            )
            response.raise_for_status()
            p = response.json()
            post.id = str(p["id"])
            return post

    async def update_post(self, post_id: str, updates: Dict[str, Any]) -> Post:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url(f"posts/{post_id}"),
                headers=self._get_auth_header(),
                json=updates
            )
            response.raise_for_status()
            p = response.json()
            return Post(
                id=str(p["id"]),
                title=p["title"]["rendered"],
                slug=p["slug"],
                content=p["content"]["rendered"],
                status=p["status"],
                excerpt=p["excerpt"]["rendered"]
            )

    async def delete_post(self, post_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._get_api_url(f"posts/{post_id}"),
                headers=self._get_auth_header(),
                params={"force": "true"}
            )
            return response.status_code in [200, 204]

    async def discover_plugins(self) -> List[Dict[str, Any]]:
        """
        Discover installed plugins on the WordPress site.
        Returns list of plugins with connection suggestions.
        """
        KNOWN_PLUGINS = {
            "fluent-crm": {"id": "fluentcrm", "name": "FluentCRM", "connector_id": "fluentcrm"},
            "woocommerce": {"id": "woocommerce", "name": "WooCommerce", "connector_id": "woocommerce"},
            "elementor": {"id": "elementor", "name": "Elementor Builder", "connector_id": "elementor"},
            "contact-form-7": {"id": "cf7", "name": "Contact Form 7", "connector_id": "cf7"},
            "wpforms-lite": {"id": "wpforms", "name": "WPForms", "connector_id": "wpforms"},
            "yoast-seo": {"id": "yoast", "name": "Yoast SEO", "connector_id": "yoast"},
        }

        async with httpx.AsyncClient() as client:
            try:
                # The 'plugins' endpoint requires administrative permissions
                # It might not be enabled on all WP installations by default without a specific plugin/config
                response = await client.get(
                    self._get_api_url("plugins"), # Note: path might need adjustment for some WP versions
                    headers=self._get_auth_header(),
                    timeout=15.0
                )
                
                # Fallback: if 'plugins' endpoint is not found, we return an empty list or try scanning
                if response.status_code == 404:
                    logger.warning("WordPress 'plugins' endpoint not found. Discovery limited.")
                    return []
                
                response.raise_for_status()
                data = response.json()
                
                discovered = []
                for p in data:
                    # WordPress returns plugin info in various formats depending on version
                    # Usually 'textdomain' or 'name' can be used
                    slug = p.get("textdomain") or p.get("plugin", "").split("/")[0].lower()
                    
                    plugin_info = {
                        "id": slug,
                        "name": p.get("name"),
                        "status": p.get("status"),
                        "version": p.get("version"),
                        "can_auto_connect": slug in KNOWN_PLUGINS
                    }
                    
                    if slug in KNOWN_PLUGINS:
                        plugin_info.update(KNOWN_PLUGINS[slug])
                        
                    discovered.append(plugin_info)
                    
                return discovered
            except Exception as e:
                logger.error(f"WordPress plugin discovery failed: {e}")
                return []
