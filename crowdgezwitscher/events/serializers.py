from django.conf import settings
from rest_framework import serializers

from events.models import Event


class AttachmentField(serializers.Field):
    """Responsible for serialization of attachments refering to an event."""
    def to_representation(self, attachments):
        return [
            {'name': att.name,
             'description': att.description,
             'url': settings.MEDIA_URL + str(att.attachment), } for att in attachments
        ]


class EventSerializer(serializers.ModelSerializer):
    repetitionCycle = serializers.CharField(source='repetition_cycle')
    counterEvent = serializers.BooleanField(source='counter_event')
    attachments = AttachmentField(source='attachments.all')

    class Meta:
        model = Event
        fields = ('id', 'name', 'location', 'date', 'repetitionCycle', 'type', 'url', 'counterEvent',
                  'coverage', 'participants', 'organizer', 'attachments')


class EventSerializerShortened(serializers.ModelSerializer):
    # TODO unify with FB-SerializerShortened, issue: Cannot use ModelSerializer with Abstract Models.
    locationLong = serializers.DecimalField(
        source='location_long', max_digits=9, decimal_places=6, coerce_to_string=False)
    locationLat = serializers.DecimalField(
        source='location_lat', max_digits=9, decimal_places=6, coerce_to_string=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'locationLong', 'locationLat', 'date')
