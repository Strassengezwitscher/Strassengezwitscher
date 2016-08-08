from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, api_view

from strassengezwitscher.auth import CsrfExemptSessionAuthentication

from captcha.utils import validate_grecaptcha


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
def validate_captcha(request):
    """
    Receives post data from the Google Recaptcha and verifies it with the Google service.
    """
    verified_response = validate_grecaptcha(request.data['response'])
    if verified_response.get("success") is not True:
        return Response(data={'status': 'error', 'errors': verified_response.get('error-codes', [])},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'success'})
