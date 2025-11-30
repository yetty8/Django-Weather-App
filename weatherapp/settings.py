from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# SECURITY
# ---------------------------
SECRET_KEY = 'django-insecure-xxxxxx'   # Replace in production!
DEBUG = False                           # Turn ON locally, OFF in production
ALLOWED_HOSTS = ['*']                   # Add your domain when you have one


# ---------------------------
# APPLICATIONS
# ---------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your App
    'weather',
]


# ---------------------------
# MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise for static file serving
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ---------------------------
# URLS + WSGI
# ---------------------------
ROOT_URLCONF = 'weatherapp.urls'
WSGI_APPLICATION = 'weatherapp.wsgi.application'


# ---------------------------
# TEMPLATES
# ---------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Main templates folder
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
# LOCALIZATION / TIMEZONE
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---------------------------
# STATIC FILES
# ---------------------------
STATIC_URL = '/static/'

# Folder where your local static files are stored
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Folder where Django collects static files for deployment
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Enable WhiteNoise compressed/static file storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ---------------------------
# AUTO FIELD
# ---------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
