import json
import logging
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login
from django.conf import settings
from .authentication import BizOSaaSUserSync
import jwt

logger = logging.getLogger(__name__)

def sso_login(request):
    """
    Initiate SSO login flow - redirect to BizOSaaS login
    """
    bizosaas_login_url = f"{settings.BIZOSAAS_API_URL}/auth/login"
    callback_url = request.build_absolute_uri('/auth/sso-callback/')
    
    redirect_url = f"{bizosaas_login_url}?callback={callback_url}"
    return redirect(redirect_url)

@csrf_exempt
def sso_callback(request):
    """
    Handle SSO callback from BizOSaaS
    """
    try:
        token = request.GET.get('token') or request.POST.get('token')
        
        if not token:
            return JsonResponse({'error': 'No token provided'}, status=400)
        
        # Validate token and get user data
        try:
            payload = jwt.decode(
                token,
                settings.BIZOSAAS_JWT_SECRET,
                algorithms=['HS256']
            )
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        # Sync user to Wagtail
        user, created = BizOSaaSUserSync.sync_user_from_bizosaas(payload)
        
        # Log user into Wagtail
        login(request, user)
        
        # Redirect to admin
        return redirect('/admin/')
        
    except Exception as e:
        logger.error(f"SSO callback error: {str(e)}")
        return JsonResponse({'error': 'SSO callback failed'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def sync_user(request):
    """
    API endpoint to sync a user from BizOSaaS
    """
    try:
        data = json.loads(request.body)
        user_data = data.get('user_data')
        
        if not user_data:
            return JsonResponse({'error': 'user_data required'}, status=400)
        
        user, created = BizOSaaSUserSync.sync_user_from_bizosaas(user_data)
        
        return JsonResponse({
            'success': True,
            'user_id': user.id,
            'created': created,
            'email': user.email
        })
        
    except Exception as e:
        logger.error(f"User sync error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def validate_token(request):
    """
    Validate a JWT token from BizOSaaS
    """
    try:
        data = json.loads(request.body)
        token = data.get('token')
        
        if not token:
            return JsonResponse({'error': 'token required'}, status=400)
        
        try:
            payload = jwt.decode(
                token,
                settings.BIZOSAAS_JWT_SECRET,
                algorithms=['HS256']
            )
            
            return JsonResponse({
                'valid': True,
                'payload': payload
            })
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'valid': False, 'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'valid': False, 'error': 'Invalid token'}, status=401)
            
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)