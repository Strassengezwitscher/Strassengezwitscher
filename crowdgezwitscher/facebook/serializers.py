from rest_framework import serializers

from facebook.models import FacebookPage


class FacebookPageSerializer(serializers.ModelSerializer):
    facebookId = serializers.CharField(source='facebook_id')

    class Meta:
        model = FacebookPage
        fields = ('id', 'name', 'location', 'notes', 'facebookId')


class FacebookPageSerializerShortened(serializers.ModelSerializer):
    # TODO unify with EventSerializerShortened, issue: Cannot use ModelSerializer with Abstract Models.
    locationLong = serializers.DecimalField(
        source='location_long', max_digits=9, decimal_places=6, coerce_to_string=False)
    locationLat = serializers.DecimalField(
        source='location_lat', max_digits=9, decimal_places=6, coerce_to_string=False)

    class Meta:
        model = FacebookPage
        fields = ('id', 'name', 'locationLong', 'locationLat')


class FacebookPageSerializerCreate(serializers.ModelSerializer):
    locationLong = serializers.CharField(source='location_long')
    locationLat = serializers.CharField(source='location_lat')
    facebookId = serializers.CharField(source='facebook_id')

    class Meta:
        model = FacebookPage
        fields = ('id', 'name', 'location', 'notes', 'locationLong', 'locationLat', 'facebookId')

    def create(self, validated_data):
        return FacebookPage.objects.create(**validated_data)
