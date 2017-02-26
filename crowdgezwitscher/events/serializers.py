import os

from django.conf import settings
from rest_framework import serializers
import six

from events.models import Event, Attachment


class AttachmentSerializer(serializers.Serializer):
    def to_representation(self, attachment):
        extension_icon_mapping = {
            '.pdf':  'img/icon_pdf.png',
        }
        default_icon = 'img/icon_file.png'

        if attachment.thumbnail:
            thumbnail_url = settings.MEDIA_URL + six.text_type(attachment.thumbnail)
        else:
            extension = os.path.splitext(attachment.name)[1].lower()
            icon_path = extension_icon_mapping.get(extension, default_icon)
            thumbnail_url = settings.STATIC_URL + six.text_type(icon_path)

        return {
            'name': attachment.name,
            'description': attachment.description,
            'url': settings.MEDIA_URL + six.text_type(attachment.attachment),
            'thumbnail_url': thumbnail_url,
        }


class EventSerializer(serializers.ModelSerializer):
    repetitionCycle = serializers.CharField(source='repetition_cycle')
    counterEvent = serializers.BooleanField(source='counter_event')
    attachments = serializers.SerializerMethodField()
    time = serializers.TimeField(format="%H:%M")

    def get_attachments(self, event):
        queryset = Attachment.objects.filter(event=event, public=True)
        serializer = AttachmentSerializer(instance=queryset, many=True)
        return serializer.data

    class Meta:
        model = Event
        fields = ('id', 'name', 'location', 'date', 'time', 'repetitionCycle', 'type', 'url', 'counterEvent',
                  'coverage', 'participants', 'organizer', 'attachments', 'notes')


class EventSerializerShortened(serializers.ModelSerializer):
    # TODO unify with FB-SerializerShortened, issue: Cannot use ModelSerializer with Abstract Models.
    locationLong = serializers.DecimalField(
        source='location_long', max_digits=9, decimal_places=6, coerce_to_string=False)
    locationLat = serializers.DecimalField(
        source='location_lat', max_digits=9, decimal_places=6, coerce_to_string=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'locationLong', 'locationLat', 'date')

class EventSerializerCreate(serializers.ModelSerializer):
    locationLong = serializers.CharField(source='location_long')
    locationLat = serializers.CharField(source='location_lat')
    date = serializers.DateField(input_formats=["%Y-%m-%dT%H:%M"])
    repetitionCycle = serializers.CharField(source='repetition_cycle')
    counterEvent = serializers.CharField(source='counter_event')
    time = serializers.TimeField(input_formats=["%Y-%m-%dT%H:%M"])

    class Meta:
        model = Event
        fields = ('name', 'location', 'locationLong', 'locationLat', 'date', 'participants', 'repetitionCycle',
                  'organizer', 'type', 'url', 'time', 'counterEvent',)

    def create(self, validated_data):
        return Event.objects.create(**validated_data)
