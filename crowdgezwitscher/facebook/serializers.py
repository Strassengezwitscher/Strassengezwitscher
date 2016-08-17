from rest_framework import serializers

from facebook.models import FacebookPage


class FacebookPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacebookPage
        fields = ('id', 'name', 'location', 'events', 'notes', 'facebook_id')


class FacebookPageSerializerShortened(serializers.ModelSerializer):
    # TODO unify with EventSerializerShortened, issue: Cannot use ModelSerializer with Abstract Models.
    locationLong = serializers.DecimalField(
        source='location_long', max_digits=9, decimal_places=6, coerce_to_string=False)
    locationLat = serializers.DecimalField(
        source='location_lat', max_digits=9, decimal_places=6, coerce_to_string=False)

    class Meta:
        model = FacebookPage
        fields = ('id', 'name', 'locationLong', 'locationLat')
