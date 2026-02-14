from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from app.domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType, ConnectorStatus
from app.ports.cms_port import CMSPort, Page as PortPage, Post as PortPost
from app.domain.services.secret_service import SecretService
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_secret_service
from app.models.mcp import UserMcpInstallation, McpRegistry
from app.services.billing_service import BillingService

router = APIRouter()

class PageMessage(BaseModel):
    id: Optional[str] = None
    title: str
    slug: str
    content: Optional[str] = ""
    status: str = "draft"
    published_at: Optional[datetime]
    updated_at: Optional[datetime] = None
    author: Optional[str] = ""

class PostMessage(BaseModel):
    id: Optional[str] = None
    title: str
    slug: str
    content: Optional[str] = ""
    excerpt: Optional[str] = ""
    category: Optional[str] = ""
    status: str = "draft"
    published_at: Optional[datetime] = None
    author: Optional[str] = ""

class CategoryMessage(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = ""
    count: Optional[int] = 0

class MediaMessage(BaseModel):
    id: str
    title: str
    source_url: str
    mime_type: str
    alt_text: Optional[str] = ""
    caption: Optional[str] = ""

async def get_active_cms_connector(tenant_id: str, secret_service: SecretService) -> CMSPort:
    # Find any connected CMS connector for this tenant
    # 1. Get all CMS connector types
    cms_configs = [c for c in ConnectorRegistry.get_all_configs() if c.type == ConnectorType.CMS]
    
    # 2. Check in-memory store first
    for config in cms_configs:
        key = f"{tenant_id}:{config.id}"
        if key in active_connectors:
            data = active_connectors[key]
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, data["credentials"])
            return connector
            
    # 3. Check secret service (persistent)
    for config in cms_configs:
        credentials = await secret_service.get_connector_credentials(tenant_id, config.id)
        if credentials:
            # Re-verify and cache in memory
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, credentials)
            active_connectors[f"{tenant_id}:{config.id}"] = {"credentials": credentials}
            return connector
            
    raise HTTPException(status_code=404, detail="No CMS connector configured. Please connect a CMS (e.g. WordPress) in Connectors settings.")

async def check_cms_capability(
    capability: str,
    user: AuthenticatedUser,
    db: Session
):
    """
    Check if the current user/tenant is allowed to perform a specific CMS action.
    Checks both the subscription plan features and user-defined toggles.
    """
    tenant_id = user.tenant_id or "default_tenant"
    
    # 1. Plan-based Gate (AI Agent limits)
    # Mapping capabilities to feature slugs
    cap_to_feature = {
        "pages": "cms_basic",
        "posts": "cms_basic",
        "media": "cms_media",
        "seo": "cms_seo",
        "plugins": "cms_advanced",
        "settings": "cms_advanced"
    }
    
    feature_slug = cap_to_feature.get(capability)
    if feature_slug:
        billing_service = BillingService(db)
        subscription = await billing_service.get_tenant_subscription(tenant_id)
        
        plan_features = []
        if subscription and subscription.plan:
             plan_features = (subscription.plan.features or {}).get('feature_slugs', [])
        
        # Super Admin bypass
        if "super admin" not in [r.lower() for r in user.roles]:
            if feature_slug not in plan_features:
                raise HTTPException(
                    status_code=403, 
                    detail=f"This operation requires the '{feature_slug}' plan feature. Please upgrade your subscription."
                )

    # 2. User-defined Toggle Gate (Privacy/Control)
    # Check UserMcpInstallation.config for manual overrides
    # Find active CMS installation
    installation = db.query(UserMcpInstallation).join(McpRegistry).filter(
        UserMcpInstallation.user_id == user.id, # Or use tenant_id if shared
        McpRegistry.category_slug == "cms"
    ).first()
    
    if installation and installation.config:
        enabled_caps = installation.config.get("enabled_capabilities", [])
        # If config exists, it must explicitly allow the capability
        if capability not in enabled_caps:
            raise HTTPException(
                status_code=403,
                detail=f"Operation '{capability}' has been disabled for this site by the administrator."
            )

@router.get("/status")
async def get_cms_status(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Check connectivity to the active CMS"""
    tenant_id = user.tenant_id or "default_tenant"
    try:
        connector = await get_active_cms_connector(tenant_id, secret_service)
        # Verify deeper connectivity if possible
        # For now, if we got the connector, it's configured
        is_valid = await connector.validate_credentials()
        
        return {
            "connected": is_valid,
            "platform": connector.config.name if hasattr(connector, 'config') else "WordPress",
            "version": "Unknown" # TODO: Fetch version from WP API
        }
    except HTTPException:
        return {"connected": False}
    except Exception as e:
         return {"connected": False, "error": str(e)}

@router.get("/stats")
async def get_cms_stats(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Get content statistics"""
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        stats = await connector.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats Error: {str(e)}")

@router.get("/pages", response_model=List[PageMessage])
async def list_pages(
    slug: Optional[str] = None,
    limit: int = 100,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("pages", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        kwargs = {}
        if slug:
            kwargs["slug"] = slug
            
        pages = await connector.get_pages(limit=limit, **kwargs) # Returns List[PortPage]
        
        # Map to response model
        return [
            PageMessage(
                id=p.id,
                title=p.title,
                slug=p.slug,
                content=p.content,
                status=p.status,
                published_at=datetime.now(), # TODO: PortPage needs date fields
                updated_at=datetime.now(),
                author=p.author_id or "System"
            ) for p in pages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

@router.post("/pages", response_model=PageMessage)
async def create_page(
    page: PageMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("pages", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        # Convert to the Page model expected by the connector
        page_obj = PortPage(
            title=page.title,
            slug=page.slug,
            content=page.content or "",
            status=page.status
        )
        result = await connector.create_page(page_obj)
        
        return PageMessage(
            id=result.id,
            title=result.title,
            slug=result.slug,
            content=result.content,
            status=result.status,
            published_at=datetime.now(),
            updated_at=datetime.now(),
            author=result.author_id or "System"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

@router.delete("/pages/{page_id}")
async def delete_page(
    page_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("pages", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        await connector.delete_page(page_id)
        return {"status": "success", "id": page_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

@router.put("/pages/{page_id}", response_model=PageMessage)
async def update_page(
    page_id: str,
    page: PageMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("pages", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        payload = page.dict(exclude={"id", "published_at", "updated_at"})
        result = await connector.update_page(page_id, payload)
        
        return PageMessage(
            id=result.id,
            title=result.title,
            slug=result.slug,
            content=result.content,
            status=result.status,
            published_at=datetime.now(),
            updated_at=datetime.now(),
            author=result.author_id or "System"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

@router.get("/posts", response_model=List[PostMessage])
async def list_posts(
    slug: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 100,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("posts", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        kwargs = {}
        if slug:
            kwargs["slug"] = slug
        if category:
            kwargs["category"] = category
            
        posts = await connector.get_posts(limit=limit, **kwargs)
        return [
            PostMessage(
                id=p.id,
                title=p.title,
                slug=p.slug,
                excerpt=p.excerpt,
                content=p.content,
                status=p.status,
                # featured_image=p.featured_image, # This field is not in the current PostMessage model
                published_at=datetime.now(),
                author=p.author_id or "System",
                # categories=p.categories, # This field is not in the current PostMessage model
                # tags=p.tags # This field is not in the current PostMessage model
            ) for p in posts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

@router.post("/posts", response_model=PostMessage)
async def create_post(
    post: PostMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("posts", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        # Convert to the Post model expected by the connector
        post_obj = PortPost(
            title=post.title,
            slug=post.slug,
            content=post.content or "",
            excerpt=post.excerpt,
            status=post.status or "publish"
        )
        result = await connector.create_post(post_obj)
        return PostMessage(
             id=result.id,
             title=result.title,
             slug=result.slug,
             content=result.content,
             status=result.status,
             published_at=datetime.now(),
             author=result.author_id or "System"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

@router.put("/posts/{post_id}", response_model=PostMessage)
async def update_post(
    post_id: str,
    post: PostMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("posts", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        payload = post.dict(exclude={"id", "published_at", "updated_at"})
        result = await connector.update_post(post_id, payload)
        return PostMessage(
             id=result.id,
             title=result.title,
             slug=result.slug,
             content=result.content,
             status=result.status,
             published_at=datetime.now(),
             author=result.author_id or "System"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("posts", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        await connector.delete_post(post_id)
        return {"status": "success", "id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

class PluginMessage(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    version: Optional[str] = None
    author: Optional[str] = None
    icon: Optional[str] = None
    installed: bool = False

# ... existing endpoints ...

@router.get("/plugins", response_model=List[PluginMessage])
async def list_plugins(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("plugins", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        if not hasattr(connector, 'get_plugins'):
             # If connector doesn't support plugins
             return []
        
        plugins = await connector.get_plugins()
        return [
            PluginMessage(
                id=p.id,
                name=p.name,
                description=p.description,
                status=p.status,
                version=p.version,
                author=p.author,
                icon=p.icon,
                installed=p.installed
            ) for p in plugins
        ]
    except Exception as e:
        # Fallback empty if not supported or error
        return []

@router.post("/plugins/{slug}/install")
async def install_plugin(
    slug: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("plugins", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        success = await connector.install_plugin(slug)
        if not success:
             raise HTTPException(status_code=400, detail="Installation failed")
        return {"status": "success", "slug": slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plugin Error: {str(e)}")

@router.post("/plugins/{slug}/activate")
async def activate_plugin(
    slug: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("plugins", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        success = await connector.activate_plugin(slug)
        if not success:
             raise HTTPException(status_code=400, detail="Activation failed")
        return {"status": "success", "slug": slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plugin Error: {str(e)}")

@router.post("/plugins/{slug}/deactivate")
async def deactivate_plugin(
    slug: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("plugins", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        success = await connector.deactivate_plugin(slug)
        if not success:
             raise HTTPException(status_code=400, detail="Deactivation failed")
        return {"status": "success", "slug": slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plugin Error: {str(e)}")

@router.delete("/plugins/{slug}")
async def delete_plugin(
    slug: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("plugins", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        success = await connector.delete_plugin(slug)
        if not success:
             raise HTTPException(status_code=400, detail="Deletion failed")
        return {"status": "success", "slug": slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plugin Error: {str(e)}")

# Categories endpoints
@router.get("/categories", response_model=List[CategoryMessage])
async def list_categories(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("posts", user, db) # Categories are part of posts
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        if not hasattr(connector, 'get_categories'):
            return []
        
        categories = await connector.get_categories()
        return [
            CategoryMessage(
                id=str(c.get('id', c.get('slug', ''))),
                name=c.get('name', ''),
                slug=c.get('slug', ''),
                description=c.get('description', ''),
                count=c.get('count', 0)
            ) for c in categories
        ]
    except Exception as e:
        return []

@router.post("/categories")
async def create_category(
    category: CategoryMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("posts", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        result = await connector.create_category({
            'name': category.name,
            'slug': category.slug,
            'description': category.description
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Category Error: {str(e)}")

@router.put("/categories/{category_id}")
async def update_category(
    category_id: str,
    category: CategoryMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("posts", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        result = await connector.update_category(category_id, {
            'name': category.name,
            'slug': category.slug,
            'description': category.description
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Category Error: {str(e)}")

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("posts", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        success = await connector.delete_category(category_id)
        if not success:
            raise HTTPException(status_code=400, detail="Deletion failed")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Category Error: {str(e)}")

# Media endpoints
@router.get("/media", response_model=List[MediaMessage])
async def list_media(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("media", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        if not hasattr(connector, 'list_media'):
            return []
        
        media = await connector.list_media()
        return [
            MediaMessage(
                id=str(m.get('id', '')),
                title=m.get('title', {}).get('rendered', '') if isinstance(m.get('title'), dict) else m.get('title', ''),
                source_url=m.get('source_url', ''),
                mime_type=m.get('mime_type', ''),
                alt_text=m.get('alt_text', ''),
                caption=m.get('caption', {}).get('rendered', '') if isinstance(m.get('caption'), dict) else m.get('caption', '')
            ) for m in media
        ]
    except Exception as e:
        return []

@router.post("/media")
async def upload_media(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("media", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        if not hasattr(connector, 'upload_media'):
            raise HTTPException(status_code=400, detail="Connected CMS does not support media upload")
            
        file_data = await file.read()
        result = await connector.upload_media(
            file_data=file_data,
            filename=file.filename,
            mime_type=file.content_type
        )
        
        return {
            "id": str(result.get('id', '')),
            "title": result.get('title', {}).get('rendered', '') if isinstance(result.get('title'), dict) else result.get('title', ''),
            "source_url": result.get('source_url', ''),
            "mime_type": result.get('mime_type', ''),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload Error: {str(e)}")

@router.delete("/media/{media_id}")
async def delete_media(
    media_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    await check_cms_capability("media", user, db)
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        success = await connector.delete_media(media_id)
        if not success:
            raise HTTPException(status_code=400, detail="Deletion failed")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Media Error: {str(e)}")
