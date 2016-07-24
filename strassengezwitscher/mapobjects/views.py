from rest_framework import generics

from mapobjects.models import MapObject
from mapobjects.serializers import MapObjectSerializer


# class MapObjectList(generics.ListAPIView):
#     queryset = MapObject.objects.all()
#     serializer_class = MapObjectSerializer
#
#
# class MapObjectDetail(generics.RetrieveAPIView):
#     queryset = MapObject.objects.all()
#     serializer_class = MapObjectSerializer
