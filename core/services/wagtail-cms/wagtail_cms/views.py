from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Check database connectivity
        db_conn = connections['default']
        db_conn.cursor()
        
        # Check cache connectivity
        cache.set('health_check', 'ok', 30)
        cache_status = cache.get('health_check') == 'ok'
        
        return JsonResponse({
            "status": "healthy",
            "database": "connected",
            "cache": "connected" if cache_status else "disconnected",
            "service": "wagtail-cms"
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JsonResponse({
            "status": "unhealthy",
            "error": str(e),
            "service": "wagtail-cms"
        }, status=503)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def create_superuser_endpoint(request):
    """
    Temporary endpoint to create a superuser
    GET: Check current users
    POST: Create/update superuser
    """
    
    User = get_user_model()
    
    if request.method == "GET":
        # Return current user status
        users = []
        for user in User.objects.all():
            users.append({
                'username': user.username,
                'email': user.email,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
                'date_joined': user.date_joined.isoformat() if user.date_joined else None
            })
        
        return JsonResponse({
            'status': 'success',
            'users': users,
            'total_users': User.objects.count(),
            'superusers': User.objects.filter(is_superuser=True).count()
        })
    
    elif request.method == "POST":
        try:
            # Get credentials from request or use defaults
            data = {}
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
            
            username = data.get('username', 'admin')
            email = data.get('email', 'admin@bizosaas.local')
            password = data.get('password', 'bizosaas123')
            
            # Delete existing user with same username
            existing_user = User.objects.filter(username=username).first()
            if existing_user:
                existing_user.delete()
                
            # Create new superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Superuser created successfully',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'is_superuser': user.is_superuser,
                    'is_active': user.is_active
                },
                'credentials': {
                    'username': username,
                    'password': password,
                    'admin_url': 'http://localhost:8006/admin/'
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)