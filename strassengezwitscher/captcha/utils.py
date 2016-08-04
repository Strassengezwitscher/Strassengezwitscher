import requests
from django.conf import settings


def validate_grecaptcha(response):
    """
    Takes a value of 'g-captcha-reponse' and validates the google recaptcha.
    """

    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': response
    }
    return requests.get(url, params=params, verify=True).json()
