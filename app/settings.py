import os
from urllib.parse import urlparse, parse_qsl
from decouple import config

# SECURITY
SECRET_KEY = 'demo-secret-key'
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']  # Solo para desarrollo

# Parsear la URL de la base de datos
database_url = config('DATABASE_URL')  # Se asegura que sea str
parsed_url = urlparse(database_url)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed_url.path.lstrip('/'),  # elimina el primer /
        'USER': parsed_url.username,
        'PASSWORD': parsed_url.password,
        'HOST': parsed_url.hostname,
        'PORT': parsed_url.port or 5432,  # puerto por defecto 5432
        # sslmode y channel_binding
        'OPTIONS': dict(parse_qsl(parsed_url.query)),
    }
}

# APPS
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
    'usuarios',
    'inventario',
    'venta',
    'cliente',
    'corsheaders'
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLS
ROOT_URLCONF = 'app.urls'

# TEMPLATES
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
WSGI_APPLICATION = 'app.wsgi.application'

# PASSWORD VALIDATION (solo dev)
# AUTH_PASSWORD_VALIDATORS = []

# I18N
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Comentamos o eliminamos las que no quieres
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # Opcional: si quieres usar JWT de DRF
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # se usará con tu TokenRequiredPermission
        'rest_framework.permissions.IsAuthenticated',
    ],
}
