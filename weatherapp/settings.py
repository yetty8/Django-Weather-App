from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# DEBUG / ENV
# ---------------------------
DEBUG = os.getenv("DEBUG", "False") == "True"

# ---------------------------
# API KEYS (from environment variables)
# ---------------------------
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

if not WEATHER_API_KEY or not UNSPLASH_ACCESS_KEY:
    # Warning instead of exit to allow local dev
    print("WARNING: Missing WEATHER_API_KEY or UNSPLASH_ACCESS_KEY environment variables!")
    WEATHER_API_KEY = WEATHER_API_KEY or "dummy_weather_key"
    UNSPLASH_ACCESS_KEY = UNSPLASH_ACCESS_KEY or "dummy_unsplash_key"

# ---------------------------
# SECURITY
# ---------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-placeholder")
ALLOWED_HOSTS = ["*"]

# ---------------------------
# INSTALLED APPS
# ---------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'weather',
]

# ---------------------------
# MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------
# URL + WSGI
# ---------------------------
ROOT_URLCONF = 'weatherapp.urls'
WSGI_APPLICATION = 'weatherapp.wsgi.application'

# ---------------------------
# TEMPLATES
# ---------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ---------------------------
# DATABASE
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------
# LOCALIZATION
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------
# STATIC FILES
# ---------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------
# AUTO FIELD
# ---------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
