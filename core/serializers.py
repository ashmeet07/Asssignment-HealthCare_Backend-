from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# -------------------------------------------------------------
# 1. User Registration Serializer
# -------------------------------------------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    # Field added explicitly to satisfy the ModelSerializer check without requiring client input
    username = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=True) 
    
    class Meta:
        model = User
        # Include username here so DRF knows it's a field being handled.
        fields = ('name', 'email', 'password', 'password2', 'username') 
        extra_kwargs = {
            'email': {
                'required': True, 
                'validators': [UniqueValidator(queryset=User.objects.all())]
            }, 
            'password': {'write_only': True}, 
            'password2': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']: 
            raise serializers.ValidationError({"password2": "Passwords must match."})
        
        # KEY STEP: Inject the email as the username before returning validated data.
        attrs['username'] = attrs['email']
        
        return attrs
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        name = validated_data.pop('name')
        
        # 'username' is now available because it was set in validate()
        username = validated_data.pop('username') 
        email = validated_data['email']

        user = User.objects.create_user(
            username=username, 
            email=email,
            password=password, 
            first_name=name
        )
        return user


# -------------------------------------------------------------
# 2. Custom JWT Serializer (Ensures email is in the token payload)
# -------------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token payload
        token['email'] = user.email
        token['name'] = user.first_name 

        return token