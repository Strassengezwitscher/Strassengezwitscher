import os

from .default import *  # noqa


SECRET_KEY = '0($mqx7@9cm@1)wa(k=*gv&6_3--7do0w++7t4jatsd8^+u*d6'  # noqa

DEBUG = True

######################################################################################################
#                                           Email settings
######################################################################################################

# print email messages on console instead of actually sending them
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Email address to use as sender for delivering contact forms
EMAIL_FROM_CONTACT = 'Some Name <user@provider>'
#
# Email addresses to use as recipients for confidential contact forms
EMAIL_TO_CONTACT_CONFIDENTIAL = ['user@provider']
#
# Email addresses to use as recipients for non-confidential contact forms
EMAIL_TO_CONTACT_NON_CONFIDENTIAL = ['user@provider']

######################################################################################################

# set additonal directories for static files
STATICFILES_DIRS += [  # noqa
    os.path.join(BASE_DIR, "static/build"),  # noqa
]

# Create a sensitive_settings.py to override settings with sensible values
# that shall not be checked in to the repository
try:
    from .sensitive_settings import *  # noqa
except ImportError:
    pass
