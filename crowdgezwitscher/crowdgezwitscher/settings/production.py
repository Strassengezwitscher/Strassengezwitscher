import os

from .default import *  # noqa


# Override in sensitive_settings.py
SECRET_KEY = '0($mqx7@9cm@1)wa(k=*gv&6_3--7do0w++7t4jatsd8^+u*d6'  # noqa

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, "static/")  # noqa


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


######################################################################################################
#                                           Email settings
######################################################################################################
EMAIL_USE_TLS = True  # port 587
EMAIL_TIMEOUT = 10  # timeout in seconds for blocking operations like the connection attempt
# EMAIL_PORT = 587  # use when running in an environment where default port 25 is blocked

#
# Override the following email-related settings in sensitive_settings.py
#
# list of all the people who get code error notifications
ADMINS = [('Name1', 'email_address1'), ('Name2', 'email_address2')]
#
# Default email address to use for various automated correspondence; not for error reporting
DEFAULT_FROM_EMAIL = 'user@provider'
#
# email address that error messages come from
SERVER_EMAIL = 'user@provider'
#
# Email address to use as sender for delivering contact forms
EMAIL_FROM_CONTACT = 'Some Name <user@provider>'
#
# Email addresses to use as recipients for confidential contact forms
EMAIL_TO_CONTACT_CONFIDENTIAL = ['user@provider']
#
# Email addresses to use as recipients for non-confidential contact forms
EMAIL_TO_CONTACT_NON_CONFIDENTIAL = ['user@provider']
#
# Your email provider's host and your credentials
EMAIL_HOST = 'provider'
EMAIL_HOST_USER = 'user@provider'
EMAIL_HOST_PASSWORD = 'password'  # noqa

######################################################################################################

# set additonal directories for static files
STATICFILES_DIRS += [
    os.path.join(BASE_DIR, "static/dist"),  # noqa
]

# REST Framework
# http://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    # differs from default settings as it does not include
    # 'rest_framework.authentication.BasicAuthentication'
    # which would interfere with the deployed develop branch's BasicAuth
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    # disable debug/developer mode
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

LOGGING['loggers']['crowdgezwitscher']['level'] = 'INFO'  # noqa

# Create a sensitive_settings.py to override settings with sensible values
# that shall not be checked in to the repository
try:
    from .sensitive_settings import *  # noqa
except ImportError:
    pass
