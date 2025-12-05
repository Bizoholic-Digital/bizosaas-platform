from django.shortcuts import redirect
from django.contrib.auth import login, get_user_model
from django.core import signing
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.cache import never_cache

User = get_user_model()

@never_cache
def sso_login(request):
    """
    Handle Single Sign-On login via signed token.
    Token is short-lived (60s) and contains user ID.
    """
    token = request.GET.get('token')
    next_url = request.GET.get('next', '/admin/')
    
    if not token:
        return HttpResponseBadRequest("Missing token")
    
    try:
        # Validate token (max_age=60 seconds)
        data = signing.loads(token, max_age=60)
        user_id = data.get('user_id')
        
        if not user_id:
            return HttpResponseBadRequest("Invalid token data")
            
        user = User.objects.get(pk=user_id)
        
        # Log the user in
        login(request, user)
        
        # Redirect to dashboard
        return redirect(next_url)
        
    except signing.SignatureExpired:
        return HttpResponseForbidden("Token expired")
    except signing.BadSignature:
        return HttpResponseForbidden("Invalid token")
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found")
    except Exception as e:
        return HttpResponseBadRequest(f"Login failed: {str(e)}")
