from rest_framework import serializers
from mapobjects.models import MapObject


class MapObjectSerializer(serializers.ModelSerializer):
    locationLong = serializers.DecimalField(source='location_long', max_digits=9, decimal_places=6)
    locationLat = serializers.DecimalField(source='location_lat', max_digits=9, decimal_places=6)

    class Meta:
        model = MapObject
        fields = ('id', 'name', 'active', 'location', 'locationLong', 'locationLat')
