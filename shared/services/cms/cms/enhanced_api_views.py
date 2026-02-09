from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json

from .models import (
    Tenant, LandingPage, CampaignPage, ContentPage, ServicePage, 
    TeamMember, ClientTestimonial, FAQPage, AIContentTemplate
)


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
    
    # Get all pages for this tenant using the generic relation
    from wagtail.models import Page
    pages = Page.objects.filter(
        id__in=[
            *tenant.landing_pages.values_list('id', flat=True),
            *tenant.campaign_pages.values_list('id', flat=True),
            *tenant.content_pages.values_list('id', flat=True),
            *tenant.service_pages.values_list('id', flat=True),
            *tenant.faq_pages.values_list('id', flat=True),
        ],
        live=True
    )
    
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
def tenant_content_summary(request, tenant_id):
    """Get content summary for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    # Count different types of pages
    landing_pages_count = tenant.landing_pages.filter(live=True).count()
    campaign_pages_count = tenant.campaign_pages.filter(live=True).count()
    content_pages_count = tenant.content_pages.filter(live=True).count()
    service_pages_count = tenant.service_pages.filter(live=True).count()
    faq_pages_count = tenant.faq_pages.filter(live=True).count()
    
    # Count snippets
    team_members_count = tenant.team_members.count()
    testimonials_count = tenant.testimonials.count()
    ai_templates_count = tenant.ai_templates.count()
    
    return JsonResponse({
        'tenant': {
            'id': tenant.bizosaas_tenant_id,
            'name': tenant.name,
        },
        'content_summary': {
            'pages': {
                'landing_pages': landing_pages_count,
                'campaign_pages': campaign_pages_count,
                'content_pages': content_pages_count,
                'service_pages': service_pages_count,
                'faq_pages': faq_pages_count,
                'total_pages': sum([
                    landing_pages_count, campaign_pages_count, 
                    content_pages_count, service_pages_count, faq_pages_count
                ]),
            },
            'snippets': {
                'team_members': team_members_count,
                'testimonials': testimonials_count,
                'ai_templates': ai_templates_count,
            }
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
        pages = tenant.landing_pages.filter(live=True)
        
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
        try:
            data = json.loads(request.body)
            
            # Create new landing page (this would be implemented with proper page creation)
            return JsonResponse({
                'message': 'Landing page would be created here',
                'data': data
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


@api_view(['GET', 'POST'])
def service_pages(request, tenant_id):
    """Get or create service pages for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    if request.method == 'GET':
        pages = tenant.service_pages.filter(live=True).order_by('order', 'title')
        
        data = []
        for page in pages:
            data.append({
                'id': page.id,
                'title': page.title,
                'service_description': page.service_description,
                'slug': page.slug,
                'url': page.url,
                'icon': page.icon,
                'badge': page.badge,
                'category': page.category,
                'featured': page.featured,
                'order': page.order,
                'price_data': page.price_data,
                'first_published_at': page.first_published_at.isoformat() if page.first_published_at else None,
            })
        
        return JsonResponse({
            'service_pages': data,
            'count': len(data)
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # AI agents can create service pages here
            return JsonResponse({'message': 'Service page creation endpoint'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


@api_view(['GET', 'POST'])
def content_pages(request, tenant_id):
    """Get or create content pages for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    if request.method == 'GET':
        pages = tenant.content_pages.filter(live=True)
        
        # Filter by category if provided
        category = request.GET.get('category')
        if category:
            pages = pages.filter(keywords__icontains=category)
        
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
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # AI agents can create content pages here
            return JsonResponse({'message': 'Content page creation endpoint'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


@api_view(['GET'])
def team_members(request, tenant_id):
    """Get team members for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    members = tenant.team_members.all()
    
    data = []
    for member in members:
        data.append({
            'id': member.id,
            'name': member.name,
            'position': member.position,
            'bio': member.bio,
            'photo': member.photo.url if member.photo else None,
            'email': member.email,
            'linkedin': member.linkedin,
            'twitter': member.twitter,
        })
    
    return JsonResponse({
        'team_members': data,
        'count': len(data)
    })


@api_view(['GET'])
def testimonials(request, tenant_id):
    """Get client testimonials for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    testimonials = tenant.testimonials.all()
    featured_only = request.GET.get('featured', 'false').lower() == 'true'
    
    if featured_only:
        testimonials = testimonials.filter(featured=True)
    
    data = []
    for testimonial in testimonials:
        data.append({
            'id': testimonial.id,
            'client_name': testimonial.client_name,
            'company': testimonial.company,
            'position': testimonial.position,
            'testimonial': testimonial.testimonial,
            'photo': testimonial.photo.url if testimonial.photo else None,
            'rating': testimonial.rating,
            'featured': testimonial.featured,
        })
    
    return JsonResponse({
        'testimonials': data,
        'count': len(data)
    })


@api_view(['GET'])
def faq_pages(request, tenant_id):
    """Get FAQ pages for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    pages = tenant.faq_pages.filter(live=True)
    category = request.GET.get('category')
    
    if category:
        pages = pages.filter(category=category)
    
    data = []
    for page in pages:
        data.append({
            'id': page.id,
            'title': page.title,
            'slug': page.slug,
            'url': page.url,
            'category': page.category,
            'first_published_at': page.first_published_at.isoformat() if page.first_published_at else None,
        })
    
    return JsonResponse({
        'faq_pages': data,
        'count': len(data)
    })


# AI Agent Integration Endpoints
@api_view(['POST'])
def ai_create_content(request, tenant_id):
    """AI agents can create content through this endpoint"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    try:
        data = json.loads(request.body)
        content_type = data.get('content_type')
        content_data = data.get('content', {})
        
        if content_type == 'landing_page':
            # Create landing page
            return JsonResponse({
                'message': 'Landing page would be created here',
                'content_type': content_type,
                'tenant_id': tenant_id
            }, status=201)
            
        elif content_type == 'blog_post':
            # Create content page
            return JsonResponse({
                'message': 'Blog post would be created here',
                'content_type': content_type,
                'tenant_id': tenant_id
            }, status=201)
            
        elif content_type == 'service_page':
            # Create service page
            return JsonResponse({
                'message': 'Service page would be created here',
                'content_type': content_type,
                'tenant_id': tenant_id
            }, status=201)
        
        else:
            return JsonResponse({'error': 'Unsupported content type'}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['PUT'])
def ai_update_content(request, tenant_id, content_id):
    """AI agents can update content through this endpoint"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    try:
        data = json.loads(request.body)
        
        # Find the content by ID (this would need proper implementation)
        return JsonResponse({
            'message': f'Content {content_id} would be updated here',
            'tenant_id': tenant_id,
            'updates': data
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def site_navigation(request, tenant_id):
    """Get site navigation structure for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    # Get all live pages for this tenant
    from wagtail.models import Page
    pages = Page.objects.filter(
        id__in=[
            *tenant.landing_pages.values_list('id', flat=True),
            *tenant.campaign_pages.values_list('id', flat=True),
            *tenant.content_pages.values_list('id', flat=True),
            *tenant.service_pages.values_list('id', flat=True),
            *tenant.faq_pages.values_list('id', flat=True),
        ],
        live=True,
        show_in_menus=True
    ).order_by('path')
    
    def build_nav_tree(pages_list):
        """Build hierarchical navigation structure"""
        nav_items = []
        for page in pages_list:
            nav_items.append({
                'id': page.id,
                'title': page.title,
                'url': page.url,
                'slug': page.slug,
                'content_type': page.content_type.model,
                'depth': page.depth,
            })
        return nav_items
    
    navigation = build_nav_tree(pages)
    
    return JsonResponse({
        'navigation': navigation,
        'tenant': {
            'id': tenant.bizosaas_tenant_id,
            'name': tenant.name,
        }
    })


@api_view(['GET'])
def ai_content_templates(request, tenant_id):
    """Get AI content templates for a tenant"""
    try:
        tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    templates = tenant.ai_templates.all()
    content_type = request.GET.get('content_type')
    
    if content_type:
        templates = templates.filter(content_type=content_type)
    
    data = []
    for template in templates:
        data.append({
            'id': template.id,
            'name': template.name,
            'content_type': template.content_type,
            'template_content': template.template_content,
            'ai_prompt': template.ai_prompt,
            'variables': template.variables,
        })
    
    return JsonResponse({
        'ai_templates': data,
        'count': len(data)
    })


# Unified CMS API endpoints as requested
@api_view(['GET'])
def cms_pages(request):
    """Get all pages with content - unified endpoint"""
    # Get tenant from request (could be via header, subdomain, etc.)
    tenant_id = request.GET.get('tenant_id')
    
    if tenant_id:
        try:
            tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
            return tenant_pages(request, tenant_id)
        except Tenant.DoesNotExist:
            return JsonResponse({'error': 'Tenant not found'}, status=404)
    
    # Return all pages if no tenant specified (for super admin)
    from wagtail.models import Page
    pages = Page.objects.filter(live=True)
    
    data = []
    for page in pages[:50]:  # Limit for performance
        data.append({
            'id': page.id,
            'title': page.title,
            'slug': page.slug,
            'url': page.url,
            'content_type': page.content_type.model,
            'first_published_at': page.first_published_at.isoformat() if page.first_published_at else None,
        })
    
    return JsonResponse({
        'pages': data,
        'count': len(data)
    })


@api_view(['GET'])
def cms_content_by_type(request, content_type):
    """Get content by type - unified endpoint"""
    tenant_id = request.GET.get('tenant_id')
    
    # Map content types to models
    content_models = {
        'landing_pages': LandingPage,
        'campaign_pages': CampaignPage,
        'content_pages': ContentPage,
        'service_pages': ServicePage,
        'faq_pages': FAQPage,
    }
    
    if content_type not in content_models:
        return JsonResponse({'error': 'Invalid content type'}, status=400)
    
    model = content_models[content_type]
    
    if tenant_id:
        try:
            tenant = Tenant.objects.get(bizosaas_tenant_id=tenant_id)
            pages = model.objects.filter(tenant=tenant, live=True)
        except Tenant.DoesNotExist:
            return JsonResponse({'error': 'Tenant not found'}, status=404)
    else:
        pages = model.objects.filter(live=True)
    
    data = []
    for page in pages:
        data.append({
            'id': page.id,
            'title': page.title,
            'slug': page.slug,
            'url': page.url,
            'first_published_at': page.first_published_at.isoformat() if page.first_published_at else None,
        })
    
    return JsonResponse({
        content_type: data,
        'count': len(data)
    })