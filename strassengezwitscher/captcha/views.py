import requests

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, api_view, parser_classes

from strassengezwitscher.log import logger
from strassengezwitscher.auth import CsrfExemptSessionAuthentication

@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
def validate_captcha(request):
    """
    Receives data from a contact form and creates a GPG-encrypted email including that data.
    Depending on the data's given confidentiality the email is sent to pre-defined receivers.
    """
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': request.data['response']
    }
    verify_rs = requests.get(url, params=params, verify=True).json()
    if verify_rs.get("success") is not True:
        return Response({'status': 'error', 'errors': verify_rs.get('error-codes', [])},
                            status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'success'})
    
