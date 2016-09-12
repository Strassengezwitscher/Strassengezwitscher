from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    repetitionCycle = serializers.CharField(source='repetition_cycle')
    counterEvent = serializers.BooleanField(source='counter_event')

    class Meta:
        model = Event
        fields = ('id', 'name', 'location', 'date', 'repetitionCycle', 'type', 'url', 'counterEvent',
                  'coverage', 'participants')


class EventSerializerShortened(serializers.ModelSerializer):
    # TODO unify with FB-SerializerShortened, issue: Cannot use ModelSerializer with Abstract Models.
    locationLong = serializers.DecimalField(
        source='location_long', max_digits=9, decimal_places=6, coerce_to_string=False)
    locationLat = serializers.DecimalField(
        source='location_lat', max_digits=9, decimal_places=6, coerce_to_string=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'locationLong', 'locationLat', 'date')
