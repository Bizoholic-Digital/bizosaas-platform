import httpx
import base64
import logging
from typing import Dict, Any, List, Optional
from ..ports.cms_port import CMSPort, Page, Post, CMSStats
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from app.observability.decorators import instrument_connector_operation, instrument_sync_operation

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

    @instrument_sync_operation("pages")
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

    @instrument_sync_operation("posts")
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
        KNOWN_PLUGINS = {
            "fluent-crm": {"id": "fluentcrm", "name": "FluentCRM", "connector_id": "fluentcrm"},
            "woocommerce": {"id": "woocommerce", "name": "WooCommerce", "connector_id": "woocommerce"},
            "elementor": {"id": "elementor", "name": "Elementor Builder", "connector_id": "elementor"},
            "contact-form-7": {"id": "cf7", "name": "Contact Form 7", "connector_id": "cf7"},
            "wpforms-lite": {"id": "wpforms", "name": "WPForms", "connector_id": "wpforms"},
            "yoast-seo": {"id": "yoast", "name": "Yoast SEO", "connector_id": "yoast"},
        }

        # Get raw plugins
        plugins = await self.get_plugins()
        results = []
        
        for p in plugins:
            p_dict = p.dict()
            # Check against known plugins by ID/slug
            # Note: WP slugs can vary, e.g. 'fluent-crm' vs 'fluent-crm-pro'
            # We match exactly for now or startswith check could be better
            if p.id in KNOWN_PLUGINS:
                 p_dict.update(KNOWN_PLUGINS[p.id])
                 p_dict["can_auto_connect"] = True
            else:
                 p_dict["can_auto_connect"] = False
            results.append(p_dict)
            
        return results

    async def get_plugins(self) -> List[Any]: # using List[Any] to avoid circular imports if Plugin isn't imported, but assuming it is available as it is in CMSPort
        # Import Plugin here or ensure it's imported at top
        from ..ports.cms_port import Plugin

        async with httpx.AsyncClient() as client:
            try:
                 response = await client.get(
                    self._get_api_url("plugins"),
                    headers=self._get_auth_header(),
                    params={"status": "all"},
                    timeout=15.0
                )
                 if response.status_code == 404:
                     return []
                 
                 response.raise_for_status()
                 data = response.json()
                 
                 plugins = []
                 for p in data:
                     # Helper to extract name/slug
                     slug = p["plugin"] 

                     # Some WP versions return full path 'plugin-slug/plugin-file.php', extract slug
                     if "/" in slug:
                        slug = slug.split("/")[0]

                     plugins.append(Plugin(
                         id=slug,
                         name=p.get("name") or slug,
                         description=p.get("description", {}).get("rendered"),
                         status=p.get("status", "inactive"),
                         version=p.get("version"),
                         author=p.get("author", {}).get("name"),
                         installed=True
                     ))
                 return plugins
            except Exception as e:
                logger.error(f"Plugin fetch failed: {e}")
                return []

    async def install_plugin(self, slug: str) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._get_api_url("plugins"),
                    headers=self._get_auth_header(),
                    json={"slug": slug, "status": "active"} 
                )
                if response.status_code in [200, 201]:
                    return True
                
                logger.error(f"Install plugin failed: {response.text}")
                return False
            except Exception as e:
                logger.error(f"Install plugin failed: {e}")
                return False

    async def activate_plugin(self, slug: str) -> bool:
        # WP API usually uses the plugin path (e.g. hello-dolly/hello.php) to activate.
        # We might need to look it up or guess. The 'plugins' endpoint often accepts the slug/path.
        # Standard WP REST API needs path.
        
        # First, find the plugin path
        plugins = await self.get_plugins()
        target_path = slug
        
        # This is tricky because get_plugins logic above extracted the slug.
        # We might need to refactor get_plugins to store the real ID (path).
        # For now, let's assume we can re-fetch raw to find the path.
        
        async with httpx.AsyncClient() as client:
             # Find path logic
             data = (await client.get(self._get_api_url("plugins"), headers=self._get_auth_header())).json()
             for p in data:
                 raw_slug = p["plugin"]
                 if raw_slug == slug or raw_slug.startswith(f"{slug}/"):
                     target_path = raw_slug
                     break
            
             response = await client.post(
                self._get_api_url(f"plugins/{target_path}"),
                headers=self._get_auth_header(),
                json={"status": "active"}
            )
             return response.status_code == 200

    async def deactivate_plugin(self, slug: str) -> bool:
         # Similar logic to activate
        target_path = slug
        async with httpx.AsyncClient() as client:
             data = (await client.get(self._get_api_url("plugins"), headers=self._get_auth_header())).json()
             for p in data:
                 raw_slug = p["plugin"]
                 if raw_slug == slug or raw_slug.startswith(f"{slug}/"):
                     target_path = raw_slug
                     break

             response = await client.post(
                self._get_api_url(f"plugins/{target_path}"),
                headers=self._get_auth_header(),
                json={"status": "inactive"}
            )
             return response.status_code == 200

    async def delete_plugin(self, slug: str) -> bool:
        target_path = slug
        async with httpx.AsyncClient() as client:
             data = (await client.get(self._get_api_url("plugins"), headers=self._get_auth_header())).json()
             for p in data:
                 raw_slug = p["plugin"]
                 if raw_slug == slug or raw_slug.startswith(f"{slug}/"):
                     target_path = raw_slug
                     break

             response = await client.delete(
                self._get_api_url(f"plugins/{target_path}"),
                headers=self._get_auth_header()
            )
             return response.status_code in [200, 204]

    async def get_categories(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url("categories"),
                    headers=self._get_auth_header(),
                    params={"per_page": 100},
                    timeout=15.0
                )
                response.raise_for_status()
                data = response.json()
                
                return [
                    {
                        'id': c.get('id'),
                        'name': c.get('name'),
                        'slug': c.get('slug'),
                        'description': c.get('description', ''),
                        'count': c.get('count', 0)
                    } for c in data
                ]
            except Exception as e:
                logger.error(f"Categories fetch failed: {e}")
                return []

    async def create_category(self, category: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._get_api_url("categories"),
                    headers=self._get_auth_header(),
                    json=category
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Category creation failed: {e}")
                raise

    async def update_category(self, category_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._get_api_url(f"categories/{category_id}"),
                    headers=self._get_auth_header(),
                    json=updates
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Category update failed: {e}")
                raise

    async def delete_category(self, category_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    self._get_api_url(f"categories/{category_id}"),
                    headers=self._get_auth_header(),
                    params={"force": True}
                )
                return response.status_code in [200, 204]
            except Exception as e:
                logger.error(f"Category deletion failed: {e}")
                return False

    async def list_media(self, limit: int = 100) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url("media"),
                    headers=self._get_auth_header(),
                    params={"per_page": limit},
                    timeout=15.0
                )
                response.raise_for_status()
                data = response.json()
                
                return [
                    {
                        'id': m.get('id'),
                        'title': m.get('title'),
                        'source_url': m.get('source_url'),
                        'mime_type': m.get('mime_type'),
                        'alt_text': m.get('alt_text', ''),
                        'caption': m.get('caption')
                    } for m in data
                ]
            except Exception as e:
                logger.error(f"Media fetch failed: {e}")
                return []

    async def upload_media(self, file_data: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                headers = self._get_auth_header()
                headers.update({
                    "Content-Disposition": f"attachment; filename={filename}",
                    "Content-Type": mime_type
                })
                
                response = await client.post(
                    self._get_api_url("media"),
                    headers=headers,
                    content=file_data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Media upload failed: {e}")
                raise

    async def delete_media(self, media_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    self._get_api_url(f"media/{media_id}"),
                    headers=self._get_auth_header(),
                    params={"force": True}
                )
                return response.status_code in [200, 204]
            except Exception as e:
                logger.error(f"Media deletion failed: {e}")
                return False
