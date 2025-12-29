from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType, ConnectorStatus
from app.ports.cms_port import CMSPort, Page as PortPage, Post as PortPost
from app.dependencies import get_secret_service
from app.domain.services.secret_service import SecretService

router = APIRouter()

class PageMessage(BaseModel):
    id: str
    title: str
    slug: str
    content: Optional[str] = ""
    status: str
    published_at: Optional[datetime]
    updated_at: Optional[datetime] = None
    author: Optional[str] = ""

class PostMessage(BaseModel):
    id: str
    title: str
    slug: str
    content: Optional[str] = ""
    excerpt: Optional[str] = ""
    category: Optional[str] = ""
    status: str
    published_at: Optional[datetime] = None
    author: Optional[str] = ""

class MediaMessage(BaseModel):
    id: str
    url: str
    title: Optional[str] = ""
    mime_type: Optional[str] = ""

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
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        pages = await connector.get_pages() # Returns List[PortPage]
        
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
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        # Convert to dict, excluding auto-fields if needed
        payload = page.dict(exclude={"id", "published_at", "updated_at"})
        # CMSPort.create_page likely expects dict or Page model
        # Assuming connector accepts dict for now
        result = await connector.create_page(payload)
        
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
    secret_service: SecretService = Depends(get_secret_service)
):
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
    secret_service: SecretService = Depends(get_secret_service)
):
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
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    
    try:
        posts = await connector.get_posts()
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
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        payload = post.dict(exclude={"id", "published_at", "updated_at"})
        result = await connector.create_post(payload)
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
    secret_service: SecretService = Depends(get_secret_service)
):
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
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_cms_connector(tenant_id, secret_service)
    try:
        await connector.delete_post(post_id)
        return {"status": "success", "id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CMS Error: {str(e)}")

@router.get("/media", response_model=List[MediaMessage])
async def list_media(
    user: AuthenticatedUser = Depends(get_current_user)
):
    # Media port undefined in base yet, placeholder
    return []
