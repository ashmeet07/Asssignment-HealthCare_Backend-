# core/urls.py
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 1. POST /api/auth/register/
    path('register/', RegisterView.as_view(), name='auth_register'),
    
    # 2. POST /api/auth/login/ (Uses simplejwt's built-in view for token creation)
    path('login/', TokenObtainPairView.as_view(), name='auth_login'),
    
    # 3. Token Refresh (POST /api/auth/token/refresh/)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]