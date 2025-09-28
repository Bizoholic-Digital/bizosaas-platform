"""
Wagtail CMS Storage Layer API
IMPORTANT: This contains NO business logic - only data storage/retrieval
All business logic is handled by FastAPI Brain (port 8001)
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import json
from datetime import datetime

from .models import Tenant, SiteSettings

# ========================================================================================
# STORAGE LAYER - Data operations only (no business logic)
# ========================================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def health_storage():
    """Storage layer health check"""
    return JsonResponse({
        "status": "healthy",
        "service": "Wagtail CMS Storage Layer",
        "mode": "storage_only",
        "business_logic": "handled_by_brain",
        "timestamp": datetime.now().isoformat()
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_tenant_data(request, tenant_id):
    """Get tenant data - STORAGE ONLY (no business validation)"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
        return JsonResponse({
            "tenant_id": tenant.bizosaas_tenant_id,
            "name": tenant.name,
            "domain": tenant.domain,
            "theme_settings": tenant.theme_settings,
            "seo_settings": tenant.seo_settings,
            "is_active": tenant.is_active,
            "created_at": tenant.created_at.isoformat()
        })
    except Tenant.DoesNotExist:
        return JsonResponse({"error": "Tenant not found"}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def store_tenant_data(request):
    """Store tenant data - STORAGE ONLY (no business validation)"""
    try:
        data = json.loads(request.body)
        
        # Just store the data - no business logic validation
        tenant, created = Tenant.objects.update_or_create(
            bizosaas_tenant_id=data.get("tenant_id"),
            defaults={
                "name": data.get("name", ""),
                "domain": data.get("domain", ""),
                "subdomain": data.get("subdomain", ""),
                "theme_settings": data.get("theme_settings", {}),
                "seo_settings": data.get("seo_settings", {}),
                "is_active": data.get("is_active", True)
            }
        )
        
        return JsonResponse({
            "success": True,
            "tenant_id": tenant.bizosaas_tenant_id,
            "created": created
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_site_settings(request, site_id):
    """Get site settings - STORAGE ONLY"""
    try:
        from wagtail.models import Site
        site = Site.objects.get(id=site_id)
        settings = SiteSettings.for_site(site)
        
        return JsonResponse({
            "site_id": site.id,
            "settings": {
                "primary_color": settings.primary_color,
                "secondary_color": settings.secondary_color,
                "site_name": settings.site_name,
                "heading_font": settings.heading_font,
                "body_font": settings.body_font,
                "contact_email": settings.contact_email,
                "contact_phone": settings.contact_phone,
                "footer_text": settings.footer_text,
            }
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def store_site_settings(request, site_id):
    """Store site settings - STORAGE ONLY (no business validation)"""
    try:
        from wagtail.models import Site
        site = Site.objects.get(id=site_id)
        settings = SiteSettings.for_site(site)
        
        data = json.loads(request.body)
        
        # Just store the data - no business logic
        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        
        settings.save()
        
        return JsonResponse({
            "success": True,
            "site_id": site_id,
            "updated_fields": list(data.keys())
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_tenants(request):
    """List all tenants - STORAGE ONLY"""
    tenants = Tenant.objects.all()
    data = []
    
    for tenant in tenants:
        data.append({
            "tenant_id": tenant.bizosaas_tenant_id,
            "name": tenant.name,
            "domain": tenant.domain,
            "is_active": tenant.is_active,
            "created_at": tenant.created_at.isoformat()
        })
    
    return JsonResponse({
        "tenants": data,
        "count": len(data),
        "storage_mode": True
    })

# ========================================================================================
# PAGE STORAGE - Simple CRUD for pages (no business logic)
# ========================================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_tenant_pages(request, tenant_id):
    """Get pages for tenant - STORAGE ONLY"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
        pages = tenant.get_site_pages()
        
        data = []
        for page in pages:
            data.append({
                "id": page.id,
                "title": page.title,
                "slug": page.slug,
                "content_type": page.content_type.name,
                "live": page.live,
                "last_published_at": page.last_published_at.isoformat() if page.last_published_at else None
            })
        
        return JsonResponse({
            "tenant_id": tenant_id,
            "pages": data,
            "count": len(data)
        })
        
    except Tenant.DoesNotExist:
        return JsonResponse({"error": "Tenant not found"}, status=404)

# Note: This file contains NO business logic
# All validation, permissions, workflows are handled by FastAPI Brain