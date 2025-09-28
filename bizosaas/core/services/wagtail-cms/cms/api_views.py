from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
# Simplified API views without Wagtail API dependencies
# IMPORTANT: This is now a STORAGE LAYER only
# All business logic has been moved to FastAPI Brain (port 8001)
# These endpoints are for data storage/retrieval ONLY

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated  # No auth here - brain handles it
import json

from .models import Tenant, LandingPage, CampaignPage, ContentPage, SiteSettings


@api_view(['GET'])
@permission_classes([])  # Allow public access
def tenant_list(request):
    """List all active tenants"""
    tenants = Tenant.objects.filter(is_active=True)
    data = []
    
    for tenant in tenants:
        data.append({
            'id': tenant.bizosaas_tenant_id,
            'name': tenant.name,
            'domain': tenant.domain,
            'subdomain': tenant.subdomain,
            'created_at': tenant.created_at.isoformat(),
        })
    
    return JsonResponse({
        'tenants': data,
        'count': len(data)
    })


@api_view(['GET'])
def tenant_pages(request, tenant_id):
    """Get all pages for a specific tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    # Get all pages for this tenant
    pages = tenant.pages.filter(live=True)
    
    # Paginate results
    paginator = Paginator(pages, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    data = []
    for page in page_obj:
        data.append({
            'id': page.id,
            'title': page.title,
            'slug': page.slug,
            'url': page.url,
            'content_type': page.content_type.model,
            'first_published_at': page.first_published_at.isoformat() if page.first_published_at else None,
            'last_published_at': page.last_published_at.isoformat() if page.last_published_at else None,
        })
    
    return JsonResponse({
        'pages': data,
        'pagination': {
            'page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    })


@api_view(['GET'])
def tenant_content(request, tenant_id):
    """Get content summary for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    # Count different types of pages
    landing_pages_count = LandingPage.objects.filter(tenant=tenant, live=True).count()
    campaign_pages_count = CampaignPage.objects.filter(tenant=tenant, live=True).count()
    content_pages_count = ContentPage.objects.filter(tenant=tenant, live=True).count()
    
    return JsonResponse({
        'tenant': {
            'id': tenant.bizosaas_tenant_id,
            'name': tenant.name,
        },
        'content_summary': {
            'landing_pages': landing_pages_count,
            'campaign_pages': campaign_pages_count,
            'content_pages': content_pages_count,
            'total_pages': landing_pages_count + campaign_pages_count + content_pages_count,
        }
    })


@api_view(['GET', 'POST'])
def landing_pages(request, tenant_id):
    """Get or create landing pages for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    if request.method == 'GET':
        pages = LandingPage.objects.filter(tenant=tenant, live=True)
        
        data = []
        for page in pages:
            data.append({
                'id': page.id,
                'title': page.title,
                'subtitle': page.subtitle,
                'slug': page.slug,
                'url': page.url,
                'variant_name': page.variant_name,
                'is_control': page.is_control,
                'campaign_id': page.campaign_id,
                'first_published_at': page.first_published_at.isoformat() if page.first_published_at else None,
            })
        
        return JsonResponse({
            'landing_pages': data,
            'count': len(data)
        })
    
    elif request.method == 'POST':
        # Create new landing page
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        # This would typically create a new landing page
        # Implementation depends on your specific requirements
        return JsonResponse({'message': 'Landing page creation endpoint'}, status=201)


@api_view(['GET'])
def campaign_pages(request, tenant_id):
    """Get campaign pages for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    pages = CampaignPage.objects.filter(tenant=tenant, live=True)
    
    data = []
    for page in pages:
        data.append({
            'id': page.id,
            'title': page.title,
            'slug': page.slug,
            'url': page.url,
            'campaign_type': page.campaign_type,
            'start_date': page.start_date.isoformat() if page.start_date else None,
            'end_date': page.end_date.isoformat() if page.end_date else None,
            'budget': str(page.budget) if page.budget else None,
            'impressions': page.impressions,
            'clicks': page.clicks,
            'conversions': page.conversions,
            'ctr': round(page.ctr(), 2),
            'conversion_rate': round(page.conversion_rate(), 2),
        })
    
    return JsonResponse({
        'campaign_pages': data,
        'count': len(data)
    })


@api_view(['GET'])
def content_pages(request, tenant_id):
    """Get content pages for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    pages = ContentPage.objects.filter(tenant=tenant, live=True)
    
    data = []
    for page in pages:
        data.append({
            'id': page.id,
            'title': page.title,
            'slug': page.slug,
            'url': page.url,
            'author': page.author,
            'publish_date': page.publish_date.isoformat() if page.publish_date else None,
            'excerpt': page.excerpt,
            'keywords': page.keywords,
            'reading_time': page.reading_time,
            'first_published_at': page.first_published_at.isoformat() if page.first_published_at else None,
        })
    
    return JsonResponse({
        'content_pages': data,
        'count': len(data)
    })


@api_view(['GET', 'PUT'])
def site_settings(request, site_id=None):
    """Get or update site settings for branding and configuration"""
    from wagtail.models import Site
    
    # Get site by ID or default site
    if site_id:
        try:
            site = Site.objects.get(id=site_id)
        except Site.DoesNotExist:
            return JsonResponse({'error': 'Site not found'}, status=404)
    else:
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            return JsonResponse({'error': 'No default site found'}, status=404)
    
    # Get or create site settings
    settings = SiteSettings.for_site(site)
    
    if request.method == 'GET':
        # Return current settings
        data = {
            'site_id': site.id,
            'site_name': site.site_name,
            'hostname': site.hostname,
            'branding': {
                'site_logo': settings.site_logo.url if settings.site_logo else None,
                'site_logo_height': settings.site_logo_height,
                'favicon': settings.favicon.url if settings.favicon else None,
                'primary_color': settings.primary_color,
                'secondary_color': settings.secondary_color,
                'site_name': settings.site_name,
                'show_site_name': settings.show_site_name,
            },
            'typography': {
                'heading_font': settings.heading_font,
                'body_font': settings.body_font,
            },
            'contact': {
                'contact_email': settings.contact_email,
                'contact_phone': settings.contact_phone,
            },
            'social_media': {
                'twitter_url': settings.twitter_url,
                'linkedin_url': settings.linkedin_url,
                'facebook_url': settings.facebook_url,
                'youtube_url': settings.youtube_url,
            },
            'analytics': {
                'google_analytics_id': settings.google_analytics_id,
                'facebook_pixel_id': settings.facebook_pixel_id,
            },
            'footer': {
                'footer_text': settings.footer_text,
            }
        }
        
        return JsonResponse({'settings': data})
    
    elif request.method == 'PUT':
        # Update settings
        try:
            data = json.loads(request.body)
            
            # Update branding settings
            if 'branding' in data:
                branding = data['branding']
                if 'primary_color' in branding:
                    settings.primary_color = branding['primary_color']
                if 'secondary_color' in branding:
                    settings.secondary_color = branding['secondary_color']
                if 'site_name' in branding:
                    settings.site_name = branding['site_name']
                if 'show_site_name' in branding:
                    settings.show_site_name = branding['show_site_name']
                if 'site_logo_height' in branding:
                    settings.site_logo_height = branding['site_logo_height']
            
            # Update typography
            if 'typography' in data:
                typography = data['typography']
                if 'heading_font' in typography:
                    settings.heading_font = typography['heading_font']
                if 'body_font' in typography:
                    settings.body_font = typography['body_font']
            
            # Update contact information
            if 'contact' in data:
                contact = data['contact']
                if 'contact_email' in contact:
                    settings.contact_email = contact['contact_email']
                if 'contact_phone' in contact:
                    settings.contact_phone = contact['contact_phone']
            
            # Update social media URLs
            if 'social_media' in data:
                social = data['social_media']
                if 'twitter_url' in social:
                    settings.twitter_url = social['twitter_url']
                if 'linkedin_url' in social:
                    settings.linkedin_url = social['linkedin_url']
                if 'facebook_url' in social:
                    settings.facebook_url = social['facebook_url']
                if 'youtube_url' in social:
                    settings.youtube_url = social['youtube_url']
            
            # Update analytics
            if 'analytics' in data:
                analytics = data['analytics']
                if 'google_analytics_id' in analytics:
                    settings.google_analytics_id = analytics['google_analytics_id']
                if 'facebook_pixel_id' in analytics:
                    settings.facebook_pixel_id = analytics['facebook_pixel_id']
            
            # Update footer
            if 'footer' in data:
                footer = data['footer']
                if 'footer_text' in footer:
                    settings.footer_text = footer['footer_text']
            
            # Save settings
            settings.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Site settings updated successfully'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def tenant_branding(request, tenant_id):
    """Get branding settings for a specific tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    # Get site settings for this tenant's Wagtail site
    if tenant.wagtail_site:
        settings = SiteSettings.for_site(tenant.wagtail_site)
        
        data = {
            'tenant_id': tenant.bizosaas_tenant_id,
            'tenant_name': tenant.name,
            'domain': tenant.full_domain,
            'branding': {
                'site_logo': settings.site_logo.url if settings.site_logo else None,
                'site_logo_height': settings.site_logo_height,
                'favicon': settings.favicon.url if settings.favicon else None,
                'primary_color': settings.primary_color,
                'secondary_color': settings.secondary_color,
                'site_name': settings.site_name,
                'show_site_name': settings.show_site_name,
                'heading_font': settings.heading_font,
                'body_font': settings.body_font,
            },
            'theme_settings': tenant.theme_settings,
        }
        
        return JsonResponse(data)
    else:
        return JsonResponse({
            'tenant_id': tenant.bizosaas_tenant_id,
            'tenant_name': tenant.name,
            'domain': tenant.full_domain,
            'branding': None,
            'theme_settings': tenant.theme_settings,
            'message': 'No Wagtail site configured for this tenant'
        })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_tenant_branding(request, tenant_id):
    """Update branding settings for a specific tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    # Ensure tenant has a Wagtail site
    if not tenant.wagtail_site:
        tenant.create_wagtail_site()
        if not tenant.wagtail_site:
            return JsonResponse({
                'error': 'Could not create Wagtail site for tenant'
            }, status=500)
    
    # Update site settings for this tenant
    settings = SiteSettings.for_site(tenant.wagtail_site)
    
    try:
        data = json.loads(request.body)
        
        # Update branding
        if 'branding' in data:
            branding = data['branding']
            for key, value in branding.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
        
        # Update theme settings in tenant model
        if 'theme_settings' in data:
            tenant.theme_settings.update(data['theme_settings'])
            tenant.save(update_fields=['theme_settings'])
        
        settings.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Branding updated for tenant {tenant.name}'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)