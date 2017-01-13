"""
Django settings for crowdgezwitscher project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import sys

import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

INTERNAL_IPS = (
    '127.0.0.1',
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base.apps.BaseConfig',
    'users.apps.UsersConfig',
    'facebook.apps.FacebookConfig',
    'events.apps.EventsConfig',
    'contact.apps.ContactConfig',
    'captcha.apps.CaptchaConfig',
    'blog.apps.BlogConfig',
    'rest_framework',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crowdgezwitscher.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'crowdgezwitscher.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


FIXTURE_DIRS = [os.path.join(BASE_DIR, 'crowdgezwitscher', 'initial')]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS_DEFAULT = [
    os.path.join(BASE_DIR, "static/shared"),
]

MEDIA_URL = '/media/'


# Set absolute URLs
ABSOLUTE_URL_OVERRIDES = {
    # Since we use auth.User to represent our users,
    # we have to provide an absolute URL for the User model.
    'auth.user': lambda u: '/intern/users/%s/' % u.id,
}

GMAPS_API_KEY = 'AIzaSyBtW6fS3wUIW5onDDkOmnLtHaYZFdRjLfA'

######################################################################################################
#                                           Recaptcha settings
######################################################################################################

# This is the default key, for which all verification requests will pass.
RECAPTCHA_SECRET_KEY = ['6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe']
######################################################################################################


######################################################################################################
#                                           Twitter settings
######################################################################################################
# number of tweets to request from Twitter's REST API
TWITTER_TWEET_COUNT = 50

# override Twitter settings with sane values in sensitive_settings.py
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''  # noqa
######################################################################################################

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'intern'

# According to http://12factor.net/logs we always log to stdout/stderr and do not manage log files.
# Production log files are managed by the production execution environment, never Django itself.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'crowdgezwitscher': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


TESTING = 'test' in sys.argv

# speed up tests
if TESTING:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}  # use sqlite
    logging.disable(logging.CRITICAL)

INSECURE = '--insecure' in sys.argv
