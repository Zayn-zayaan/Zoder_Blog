"""
Django settings for Zoder project.

Generated by 'django-admin startproject' using Django 3.1rc1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from pathlib import Path, os
from django.contrib.messages import constants as messages
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'msel$7^*%fjg3!m4ky$g!d2_nhstow&+chi9(b2y$(xx!(_(wg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['localhost','127.0.0.1']
ALLOWED_HOSTS = ['localhost','127.0.0.1','zoderbook.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'blog',
    'home',
    'ckeditor',
    'django_email_verification',
    'django_queue_mailer',
    'Zoder',
    'django_cleanup.apps.CleanupConfig',
    # 'django_crontab',
]

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

ROOT_URLCONF = 'Zoder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Zoder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': "auto",
    },
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-in'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

import socket
socket.getaddrinfo('smtp.gmail.com', 587)
# EMAIL_BACKEND
 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = socket.gethostbyname('smtp.sendgrid.net')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your email'
EMAIL_HOST_PASSWORD = 'your password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Zoder Team <zoderadmn781@gmail.com>'

#email verification

def verified_callback(user):
    user.is_active = True

EMAIL_ACTIVE_FIELD = 'is_active'
EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_TOKEN_LIFE = 60 * 6
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_ADDRESS = 'your email'
EMAIL_FROM_ADDRESS = 'Zoder Team <noreply@zoderadmin.com>'
EMAIL_PASSWORD = 'your password'
EMAIL_MAIL_SUBJECT = 'Zoder admin: Confirm Email'
EMAIL_MAIL_HTML = 'verify/mail_body.html'
EMAIL_MAIL_PLAIN = 'verify/mail_body.txt'
EMAIL_PAGE_TEMPLATE = 'verify/confirm_template.html'
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/'

# CRONJOBS = [
#     ('*/1 * * * *','home.cron.verifyuser')
# ]
