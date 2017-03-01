from rest_framework import generics

from base.models import MapObjectFilterBackend
from facebook.models import FacebookPage
from facebook.serializers import FacebookPageSerializer, FacebookPageSerializerShortened


class FacebookPageAPIList(generics.ListAPIView):
    queryset = FacebookPage.objects.filter(active=True)
    serializer_class = FacebookPageSerializerShortened
    filter_backends = (MapObjectFilterBackend,)


class FacebookPageAPIDetail(generics.RetrieveAPIView):
    queryset = FacebookPage.objects.filter(active=True)
    serializer_class = FacebookPageSerializer
