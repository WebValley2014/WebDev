"""
Django settings for WebDev project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import djcelery
djcelery.setup_loader()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gvvharcz1%!wjyckfsw0@+tfa_k1z!9yx3&#&oojf09*q13pg9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'WebDev',
    'classification',
    'network',
    'preprocess',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'WebDev.urls'

WSGI_APPLICATION = 'WebDev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#DUNNO IF NEEDED
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'WebDev/static'),
)

STATIC_ROOT = ''
STATIC_URL = '/static/'

#Template path
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'WebDev/templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_CLASSIFICATION_ROOT = os.path.join(MEDIA_ROOT, 'classification')
MEDIA_PREPROCESS_ROOT = os.path.join(MEDIA_ROOT, 'preprocess')
MEDIA_NETWORK_ROOT = os.path.join(MEDIA_ROOT, 'network')
MEDIA_URL = '/media/'

# BROKER_URL = 'ampq://localhost:5672/0'
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# List of modules to import when celery starts.
# CELERY_IMPORTS = ('myapp.tasks', )
## Using the database to store task state and results.pip
CELERY_TRACK_STARTED = True
CELERY_RESULT_BACKEND = "amqp"
## CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672//'

CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.


UPLOAD_PATH = '/static/'
