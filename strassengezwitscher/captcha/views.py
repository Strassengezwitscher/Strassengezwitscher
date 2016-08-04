from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, api_view

from strassengezwitscher.auth import CsrfExemptSessionAuthentication

from captcha.utils import validate_grecaptcha


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
def validate_captcha(request):
    """
    Receives data from a contact form and creates a GPG-encrypted email including that data.
    Depending on the data's given confidentiality the email is sent to pre-defined receivers.
    """
    verified_reponse = validate_grecaptcha(request.data['response'])
    if verified_reponse.get("success") is not True:
        return Response(data={'status': 'error', 'errors': verified_reponse.get('error-codes', [])},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'success'})
