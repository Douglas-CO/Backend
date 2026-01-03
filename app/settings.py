import os
from urllib.parse import urlparse, parse_qsl
from decouple import config

# -----------------------
# SECURITY & DEBUG
# -----------------------
SECRET_KEY = config(
    'SECRET_KEY',
    default='demo-secret-key'
)
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']  # demo / desarrollo

# -----------------------
# DATABASE (PostgreSQL Neon)
# -----------------------
# Se asegura que DATABASE_URL exista, si no usamos un valor por defecto
database_url = config(
    'DATABASE_URL',
    default='postgresql://user:pass@localhost:5432/db_demo'
)
parsed_url = urlparse(database_url)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed_url.path.lstrip('/'),
        'USER': parsed_url.username,
        'PASSWORD': parsed_url.password,
        'HOST': parsed_url.hostname,
        'PORT': parsed_url.port or 5432,
        'OPTIONS': dict(parse_qsl(parsed_url.query)),  # sslmode, channel_binding, etc
    }
}

# -----------------------
# APPS
# -----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'django_extensions',
    'corsheaders',  # CORS
    # tus apps
    'usuarios',
    'inventario',
    'venta',
    'cliente',
]

# -----------------------
# MIDDLEWARE
# -----------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # debe ir arriba
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------
# CORS
# -----------------------
CORS_ALLOW_ALL_ORIGINS = True  # permite todos los orígenes (demo)

# -----------------------
# URLS / TEMPLATES / WSGI
# -----------------------
ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# -----------------------
# STATIC FILES
# -----------------------
STATIC_URL = '/static/'

# -----------------------
# REST FRAMEWORK (demo)
# -----------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # demo: sin login
    ],
}

# -----------------------
# INTERNATIONALIZATION
# -----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------
# AUTO FIELD
# -----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
