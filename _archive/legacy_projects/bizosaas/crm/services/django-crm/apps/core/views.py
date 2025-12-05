"""
Core views for Django CRM
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .authentication import TokenManager


class LoginView(APIView):
    """User login with JWT token generation"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        tenant_id = request.data.get('tenant_id')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, username=email, password=password)
        if user:
            token = TokenManager.generate_token(user, tenant_id)
            return Response({
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                }
            })
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class RefreshTokenView(APIView):
    """Refresh JWT token"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response(
                {'error': 'Token required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_token = TokenManager.refresh_token(token)
            return Response({'token': new_token})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """User logout"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # In a production system, you might want to blacklist the token
        return Response({'message': 'Logged out successfully'})


class UserProfileView(APIView):
    """User profile management"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
        })


# Error handlers
def bad_request(request, exception):
    return JsonResponse({'error': 'Bad request'}, status=400)

def permission_denied(request, exception):
    return JsonResponse({'error': 'Permission denied'}, status=403)

def not_found(request, exception):
    return JsonResponse({'error': 'Not found'}, status=404)

def server_error(request):
    return JsonResponse({'error': 'Internal server error'}, status=500)