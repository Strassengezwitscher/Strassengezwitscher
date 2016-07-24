from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    locationLong = serializers.DecimalField(source='location_long', max_digits=9, decimal_places=6)
    locationLat = serializers.DecimalField(source='location_lat', max_digits=9, decimal_places=6)

    class Meta:
        model = Event
        fields = ('id', 'name', 'active', 'location', 'locationLong', 'locationLat')
