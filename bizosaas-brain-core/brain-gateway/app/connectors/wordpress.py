import httpx
import base64
import logging
from typing import Dict, Any, List, Optional
from ..ports.cms_port import CMSPort, Page, Post, CMSStats, Plugin
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
            version="2.1.0",
            auth_schema={
                "url": {"type": "string", "label": "WordPress Site URL", "placeholder": "https://your-site.com"},
                "username": {"type": "string", "label": "Username"},
                "application_password": {"type": "password", "label": "Application Password", "help": "Generate in Users > Profile"}
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
        url = self.credentials.get("url", "").strip()
        if not url:
            return ""
        
        base_url = url.rstrip("/")
        # Check if we should use standard wp-json or if it's already provided
        if "wp-json" in base_url:
             return f"{base_url}/wp/v2/{path.lstrip('/')}"
        return f"{base_url}/wp-json/wp/v2/{path.lstrip('/')}"

    def _get_plugin_api_url(self, plugin_prefix: str, path: str) -> str:
        url = self.credentials.get("url", "").strip().rstrip("/")
        if not url: return ""
        if "wp-json" in url:
            return f"{url}/{plugin_prefix}/{path.lstrip('/')}"
        return f"{url}/wp-json/{plugin_prefix}/{path.lstrip('/')}"

    async def validate_credentials(self) -> bool:
        url = self.credentials.get("url", "")
        if not url:
            logger.error("WordPress validation failed: Missing site URL")
            return False
            
        try:
            async with httpx.AsyncClient() as client:
                # Use /users/me to verify credentials and permissions
                api_url = self._get_api_url("users/me")
                logger.info(f"Validating WordPress connection to: {api_url}")
                
                response = await client.get(
                    api_url,
                    headers=self._get_auth_header(),
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    # Check if user has administrator or editor capabilities
                    capabilities = user_data.get("capabilities", {})
                    is_admin = capabilities.get("administrator", False)
                    logger.info(f"WordPress connection validated successfully. Is Admin: {is_admin}")
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
            # Check for required plugins
            discovery = await self._discover_plugins()
            plugins = discovery.get("plugins", {})
            
            # If any detected is false, we're degraded
            if any(not p.get("detected") for p in plugins.values()):
                return ConnectorStatus.DEGRADED
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
        elif resource_type == 'plugins':
            items = await self.get_plugins()
            return {"data": [p.dict() for p in items]}
        return {"data": []}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Perform actions like plugin discovery, install, etc."""
        if action == "discover_plugins":
            return await self._discover_plugins()
        elif action == "toggle_plugin":
            success = await self.toggle_plugin(payload.get("slug"), payload.get("active", False))
            return {"status": "success" if success else "error"}
        elif action == "install_plugin":
            success = await self.install_plugin(payload.get("slug"))
            return {"status": "success" if success else "error"}
        elif action == "uninstall_plugin":
            success = await self.uninstall_plugin(payload.get("slug"))
            return {"status": "success" if success else "error"}
        elif action == "search_plugin_directory":
            return await self._search_wp_org_plugins(payload.get("query", ""))
        elif action == "create_post":
            from app.ports.cms_port import Post
            post = Post(**payload)
            result = await self.create_post(post)
            return result.dict()
        elif action == "create_page":
            from app.ports.cms_port import Page
            page = Page(**payload)
            result = await self.create_page(page)
            return result.dict()
        elif action == "delete_post":
            success = await self.delete_post(payload.get("post_id"))
            return {"status": "success" if success else "error"}
        elif action == "delete_page":
            success = await self.delete_page(payload.get("page_id"))
            return {"status": "success" if success else "error"}
        return {"status": "error", "message": f"Unknown action: {action}"}

    async def _discover_plugins(self) -> Dict[str, Any]:
        """Detect WooCommerce, FluentCRM, etc."""
        # Requirements map: name -> {prefix, path, label}
        requirements = {
            "woocommerce": {"prefix": "wc/v3", "path": "", "label": "WooCommerce"},
            "fluent-crm": {"prefix": "fluent-crm/v1", "path": "contacts", "label": "FluentCRM"}
        }
        
        plugins = {}
        auth = self._get_auth_header()
        
        async with httpx.AsyncClient() as client:
            # First, fetch the /wp-json index to see available namespaces globally
            # This is the most reliable way to check for plugin activations
            namespaces = []
            try:
                index_url = self.credentials.get("url", "").rstrip("/") + "/wp-json"
                index_resp = await client.get(index_url, timeout=5.0)
                if index_resp.status_code == 200:
                    namespaces = index_resp.json().get("namespaces", [])
            except Exception as e:
                logger.warning(f"Failed to fetch WordPress index: {e}")

            for slug, req in requirements.items():
                try:
                    # Check namespace list first
                    detected = req["prefix"] in namespaces
                    
                    # Fallback or confirmation: try hitting the specific endpoint
                    if not detected:
                        url = self._get_plugin_api_url(req["prefix"], req["path"])
                        resp = await client.get(url, headers=auth, timeout=5.0)
                        # 200 means it definitely exists and is public
                        # 401/403 means the endpoint is registered but we lack permissions 
                        # (common for CRM/WooCommerce depending on API key scope)
                        if resp.status_code in [200, 401, 403]:
                            detected = True
                    
                    plugins[slug] = {
                        "detected": detected,
                        "label": req["label"]
                    }
                except Exception:
                    plugins[slug] = {"detected": False, "label": req["label"]}

        return {
            "status": "success",
            "plugins": plugins
        }

    async def _search_wp_org_plugins(self, query: str) -> Dict[str, Any]:
        """Search WordPress.org plugin directory"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]={query}&request[per_page]=10"
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "status": "success",
                        "plugins": data.get("plugins", [])
                    }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        return {"status": "error", "message": "Failed to search directory"}

    # --- Plugin Management Implementation ---
    async def get_plugins(self) -> List[Plugin]:
        async with httpx.AsyncClient() as client:
            try:
                # Requires 'activate_plugins' capability
                response = await client.get(
                    self._get_api_url("plugins"),
                    headers=self._get_auth_header(),
                    timeout=15.0
                )
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch plugins: {response.status_code} - {response.text}")
                    return []
                
                data = response.json()
                return [
                    Plugin(
                        id=p["plugin"],
                        name=p["name"],
                        slug=p["plugin"].split('/')[0],
                        version=p["version"],
                        status=p["status"],
                        description=p.get("description", {}).get("rendered", ""),
                        author=p.get("author_name", ""),
                        plugin_url=p.get("plugin_uri", "")
                    ) for p in data
                ]
            except Exception as e:
                logger.error(f"Plugin fetch failed: {e}")
                return []

    async def toggle_plugin(self, slug: str, active: bool) -> bool:
        """Activate or deactivate a plugin"""
        async with httpx.AsyncClient() as client:
            try:
                # WP REST API uses the relative path as the identifier (e.g. 'akismet/akismet.php')
                # But sometimes users just provide the slug. We need the full id.
                plugins = await self.get_plugins()
                plugin_id = next((p.id for p in plugins if p.slug == slug or p.id == slug), slug)
                
                status = "active" if active else "inactive"
                response = await client.post(
                    self._get_api_url(f"plugins/{plugin_id}"),
                    headers=self._get_auth_header(),
                    json={"status": status}
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Plugin toggle failed: {e}")
                return False

    async def install_plugin(self, slug: str) -> bool:
        """
        WordPress core REST API doesn't support installation from repo. 
        This usually requires WP-CLI or a helper plugin.
        We'll log this as a limitation or suggest using the WP dashboard for now.
        Alternatively, if we had a helper plugin on the client side, we could do it.
        """
        logger.info(f"Install plugin requested for: {slug}. Standard REST API does not support remote installs.")
        return False

    async def uninstall_plugin(self, slug: str) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                plugins = await self.get_plugins()
                plugin_id = next((p.id for p in plugins if p.slug == slug or p.id == slug), slug)
                
                response = await client.delete(
                    self._get_api_url(f"plugins/{plugin_id}"),
                    headers=self._get_auth_header()
                )
                return response.status_code in [200, 204]
            except Exception as e:
                logger.error(f"Plugin uninstall failed: {e}")
                return False

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
        # Standard WordPress post payload
        payload = {
            "title": post.title,
            "content": post.content,
            "status": post.status if post.status in ["publish", "draft", "private", "pending"] else "publish",
            "slug": post.slug
        }
        
        # Add basic fields that might prevent success on some themes/plugins
        if post.excerpt:
            payload["excerpt"] = post.excerpt
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._get_api_url("posts"),
                    headers=self._get_auth_header(),
                    json=payload,
                    timeout=20.0
                )
                
                if response.status_code != 201:
                    logger.error(f"WordPress create post failed: {response.status_code} - {response.text}")
                    # Special check for permissions
                    if response.status_code == 403:
                         raise Exception("Permission denied. Check if Application Password has administrator/editor role.")
                    response.raise_for_status()
                
                p = response.json()
                post.id = str(p["id"])
                logger.info(f"Successfully created WordPress post: {post.id}")
                return post
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP Error creating post: {e.response.text}")
                raise Exception(f"WordPress API Error: {e.response.text}")
            except Exception as e:
                logger.error(f"Error creating post: {str(e)}")
                raise

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
