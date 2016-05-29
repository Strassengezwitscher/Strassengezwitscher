from rest_framework import serializers
from mapobjects.models import MapObject


class MapObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapObject
        fields = ('id', 'name', 'active', 'location_long', 'location_lat')