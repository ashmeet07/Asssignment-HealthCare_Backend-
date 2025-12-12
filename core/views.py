from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
# Import the custom serializers
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

# View for: POST /api/auth/register/
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save() 
        
        return Response({
            "message": "User registered successfully.", 
            "email": user.email, 
            "name": user.first_name
        }, status=status.HTTP_201_CREATED)


# View for: POST /api/auth/login/
# Inherits the JWT view and uses the custom serializer
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    # CRITICAL: Use the custom serializer
    serializer_class = CustomTokenObtainPairSerializer