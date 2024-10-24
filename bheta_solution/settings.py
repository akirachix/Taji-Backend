import dj_database_url
"""
Django settings for bheta_solution project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
import json
import base64


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3b%wy40!(7c#)-kp0g1s#l_p&-flki&5i4%k!agj0gc(k4hcea'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


CRONJOBS = [
('50 15 */5 * *', 'cron_jobs.cron.cron_scrape_and_save')
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
    'pharmacies',
    'image__upload',
    'recall_drugs',
    'corsheaders',
    'django_crontab',
    'user',
    'django.contrib.sites',
    "allauth",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'allauth.account.middleware.AccountMiddleware',
]


CORS_ORIGIN_ALLOW_ALL = True

SITE_ID = 1



ROOT_URLCONF = 'bheta_solution.urls'

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

WSGI_APPLICATION = 'bheta_solution.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASE_URL = os.getenv("DATABASE_URL")
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

# Fallback for local development and test environments
if not os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"




load_dotenv()


DEFAULT_GOOGLE_VISION_CREDENTIALS = '{}'


GOOGLE_VISION_CREDENTIALS = os.getenv('GOOGLE_VISION_CREDENTIALS', DEFAULT_GOOGLE_VISION_CREDENTIALS)


try:
    GOOGLE_VISION_CREDENTIALS = json.loads(GOOGLE_VISION_CREDENTIALS)
except json.JSONDecodeError as e:
    print(f"Error decoding GOOGLE_VISION_CREDENTIALS: {e}")
    GOOGLE_VISION_CREDENTIALS = None  

if GOOGLE_VISION_CREDENTIALS:
    print("Google Vision API credentials loaded successfully.")
else:
    print("Failed to load Google Vision API credentials. Check your .env configuration.")




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


