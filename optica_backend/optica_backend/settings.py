"""
Django settings for optica_backend project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5m&$w=r02_hf1zls&34s*fgw56+#1(_h^rj7yyz=3)a)y3t^@^'

# SECURITY WARNING: don't run with debug turned on in production!
# En la nube lo ideal es False, pero déjalo en True un momento para ver errores si salen.
DEBUG = True

# IMPORTANTE: El asterisco permite que PythonAnywhere (la nube) muestre tu sitio
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Tus aplicaciones
    'corsheaders',
    'api.apps.ApiConfig', 
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # <-- ESTE DEBE IR ARRIBA
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'optica_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # AQUÍ ESTABA EL ERROR: Ahora le decimos que busque en la carpeta 'templates'
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'optica_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-mx' # Lo cambié a español de una vez

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES DEL SITIO) ---
STATIC_URL = '/static/'

# Esto le dice a Django: "Busca los estilos y scripts en la carpeta 'static' que creamos"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Esto es para cuando subas a la nube: Django reunirá todo aquí
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# --- CONFIGURACIÓN PARA SUBIR FOTOS (MEDIA) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Permite que CUALQUIER origen (incluyendo 'file://') haga peticiones.
CORS_ALLOW_ALL_ORIGINS = True