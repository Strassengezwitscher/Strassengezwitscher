from rest_framework import generics
from rest_framework.decorators import authentication_classes, api_view, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from base.models import MapObjectFilterBackend
from facebook.models import FacebookPage
from facebook.serializers import FacebookPageSerializer, FacebookPageSerializerShortened, FacebookPageSerializerCreate

from crowdgezwitscher.log import logger
from crowdgezwitscher.auth import CsrfExemptSessionAuthentication


class FacebookPageAPIList(generics.ListAPIView):
    queryset = FacebookPage.objects.filter(active=True)
    serializer_class = FacebookPageSerializerShortened
    filter_backends = (
        MapObjectFilterBackend,
    )


class FacebookPageAPIDetail(generics.RetrieveAPIView):
    queryset = FacebookPage.objects.filter(active=True)
    serializer_class = FacebookPageSerializer

@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@parser_classes((JSONParser,))
def send_form(request):
    serializer = FacebookPageSerializerCreate(data=request.data)
    if not serializer.is_valid():
        return Response({'status': 'error', 'message': 'Fehler beim Speichern der Informationen. \n' + '\n'.join([serializer.errors[msg][0] for msg in serializer.errors])},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        serializer.save()
    except Exception as e:
        return Response({'status': 'error', 'message': 'Fehler beim Speichern der Informationen.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})
