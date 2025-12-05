# API endpoints for services and homepage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from cms.models import ServicePage, BizoholicHomePage

@api_view(['GET'])
@permission_classes([AllowAny])
def get_services(request):
    """Get all service pages"""
    services = ServicePage.objects.live().public().order_by('order', 'title')
    
    data = []
    for service in services:
        data.append({
            'id': service.id,
            'title': service.title,
            'slug': service.slug,
            'service_description': service.service_description,
            'icon': service.icon,
            'badge': service.badge,
            'category': service.category,
            'featured': service.featured,
            'order': service.order,
            'price_data': service.price_data,
        })
    
    return Response({
        'services': data,
        'count': len(data),
        'source': 'wagtail'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_homepage(request):
    """Get homepage data"""
    try:
        homepage = BizoholicHomePage.objects.live().first()
        
        if not homepage:
            return Response({
                'error': 'Homepage not found'
            }, status=404)
        
        # Serialize stats
        stats = []
        for block in homepage.stats_content:
            if block.block_type == 'stat':
                stats.append({
                    'number': block.value.get('stat_number', ''),
                    'label': block.value.get('stat_label', ''),
                    'description': block.value.get('stat_description', ''),
                })
        
        # Serialize features
        features = []
        for block in homepage.features_content:
            if block.block_type == 'feature':
                features.append({
                    'icon': '🚀',  # Default icon
                    'title': block.value.get('title', ''),
                    'description': block.value.get('description', ''),
                })
        
        data = {
            'homepage': {
                'title': homepage.title,
                'hero_title': homepage.hero_title,
                'hero_subtitle': homepage.hero_subtitle,
                'hero_cta_text': homepage.hero_cta_text,
                'hero_cta_url': homepage.hero_cta_url,
                'features_title': homepage.features_title,
                'features': features,
                'stats': stats,
                'show_service_status': homepage.show_service_status,
                'tenant_id': 'bizoholic'
            },
            'source': 'wagtail'
        }
        
        return Response(data)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)
