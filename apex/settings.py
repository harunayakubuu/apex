import os
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


# SECRET KEY
SECRET_KEY = config('SECRET_KEY')

# DEBUG = True
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['www.apexproperties.ng', 'apexproperties.ng', 'localhost', '127.0.0.1', 'web-production-7b2f.up.railway.app']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Whitenoise App
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party Apps
    'widget_tweaks',
    'crispy_forms',
    'django_htmx',
    'phonenumber_field',
    'import_export',
    'ckeditor',
    'django_filters',

    'storages',

    # My Apps
    'accounts',
    'agencies',
    'agents',
    'blog',
    'clients',
    'contacts',
    'enquiries',
    'faqs',
    'invoices',
    'listings',
    'pages',
    'reports',
    'sales',
]

SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', #WhiteNoise Middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout', # Auto Logout Middleware
    'django_htmx.middleware.HtmxMiddleware', # HTMX MiddleWare
]

ROOT_URLCONF = 'apex.urls'


# Auto Logout Config
from datetime import timedelta
AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(hours=1),
    'SESSION_TIME': timedelta(hours=6),
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
    'MESSAGE': 'This session has expaired. Please login again to continue.'
} # Logs out after 1 hour of idleness after the last login


# Templates Config
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
                'django_auto_logout.context_processors.auto_logout_client' # Auto logout
            ],
        },
    },
]


WSGI_APPLICATION = 'apex.wsgi.application'


# Custom User Model Config
AUTH_USER_MODEL = 'accounts.User'


# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


import dj_database_url

DATABASE_URL = config('DATABASE_URL')
DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT')
#     }
# }


# Email Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_TIMEOUT = config('EMAIL_TIMEOUT', cast=int)


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True


# Static Config
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# AWS Config
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = config('AWS_S3_FILE_OVERWRITE')
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Crispy Forms Config
CRISPY_TEMPLATE_PACK = "bootstrap4"


# Phone number Config
PHONENUMBER_DEFAULT_REGION = "NG"


# Messages Config
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGIN_URL = 'login/'
LOGOUT_REDIRECT_URL = '/'


# ADMINS = env('ADMIN_EMAIL')