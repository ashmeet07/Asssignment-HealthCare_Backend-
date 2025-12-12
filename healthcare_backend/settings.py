# healthcare_backend/settings.py
import os
import environ
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- ENVIRONMENT SETUP ---
env = environ.Env(
    # Set default cast and value for DEBUG
    DEBUG=(bool, False)
)
# Read .env file (make sure your .env is in the root directory)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- CORE SETTINGS ---
# 1. SECURITY WARNING: Use SECRET_KEY from .env
SECRET_KEY = env('SECRET_KEY')

# 2. SECURITY WARNING: Use DEBUG from .env
DEBUG = env('DEBUG')

# 3. ALLOWED HOSTS
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS') if not DEBUG else ['*']

# Application definition
INSTALLED_APPS = [
    # 1. CORE DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 2. THIRD-PARTY LIBRARIES (API & SECURITY)
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # 3. LOCAL APPS
    'core',
    'records',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # CORS Middleware MUST come before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "healthcare_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "healthcare_backend.wsgi.application"


# --- DATABASE CONFIGURATION (POSTGRESQL) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env('DB_NAME'),
        "USER": env('DB_USER'),
        "PASSWORD": env('DB_PASSWORD'),
        "HOST": env('DB_HOST'),
        "PORT": env('DB_PORT'),
    }
}


# --- REST FRAMEWORK CONFIGURATION ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    )
}

# --- JWT CONFIGURATION ---
SIMPLE_JWT = {
    'ALGORITHM': 'HS256', 
    'SIGNING_KEY': SECRET_KEY, 
    
    # Standard Expiration for Security
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    "USERNAME_FIELD": "email",
    'JTI_CLAIM': 'jti',
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# --- CORS CONFIGURATION ---
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_CREDENTIALS = True

# We keep the custom header list you provided earlier
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrf-token',
    'x-requested-with',
]


# --- PASSWORD VALIDATION, I18N, STATIC FILES (Standard Django) ---
AUTH_PASSWORD_VALIDATORS = [
    # ... (Keep standard password validators) ...
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata" 
USE_I18N = True
USE_TZ = True # Crucial for PostgreSQL time zones

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"