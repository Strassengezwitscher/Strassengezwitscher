from __future__ import unicode_literals
from decimal import Decimal
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from rest_framework.exceptions import ValidationError
from rest_framework import filters


class MapObjectFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        square_params = {
            'min_lat': request.query_params.get('min_lat'),
            'min_long': request.query_params.get('min_long'),
            'max_lat': request.query_params.get('max_lat'),
            'max_long': request.query_params.get('max_long')
        }

        if square_params['min_lat'] is not None or \
                square_params['min_long'] is not None or\
                square_params['max_lat'] is not None or \
                square_params['max_long'] is not None:

            return queryset.model.get_mapobjects_in_square(square_params)

        return queryset


@python_2_unicode_compatible
class MapObject(models.Model):
    name = models.CharField(max_length=100, default="unbenannt")
    active = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)

    def __repr__(self):
        return '<MapObject %s>' % self.name

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    @classmethod
    def get_mapobjects_in_square(cls, square_params):
        """
        Arguments:
            square_params -- dictionary containing the values 'min_lat', 'max_lat', 'min_long', 'max_long'

        Explanation:
            Return all objects whose latitude and longitude are situated within the square defined
            by square_params.


            The left bottom corner in square is called 'Min' and defined by 'min_lat' and 'min_long'.
            The right top corner is called 'Max' and defined by 'max_lat' and 'max_long'.
            The MapObject to check is called 'MO'.
            'MO' is in the square iff 'MO' is right/above of 'Min' and left/below 'Max'.
            Whenever 'Min' is left of the +180/-180 longitude and 'MO'/'Max' right of it, 'MO'/'Max' get
            shifted by 360 degrees.

             _______.< Max
            |       |
            |  .'MO'|
            ._______|
            ^
            Min
        """
        square_params_decimal = cls.get_as_decimals(square_params)

        if not cls.are_valid_params(square_params_decimal):
            raise ValidationError(
                {
                    'message': ('Please provide latitude values in range [-90, 90] and '
                                'longitude values in range [-180, 180].')
                })

        return [o for o in cls.objects.all() if o.is_in_square(square_params_decimal)]

    @classmethod
    def are_valid_params(cls, square_params):
        return cls.is_valid_latitude(square_params['min_lat']) and \
            cls.is_valid_latitude(square_params['max_lat']) and \
            cls.is_valid_longitude(square_params['min_long']) and \
            cls.is_valid_longitude(square_params['max_long'])

    @classmethod
    def get_as_decimals(cls, square_params):
        try:
            square_params_decimal = {
                'min_lat': Decimal(square_params['min_lat']),
                'max_lat': Decimal(square_params['max_lat']),
                'min_long': Decimal(square_params['min_long']),
                'max_long': Decimal(square_params['max_long'])
            }

            return square_params_decimal
        except:
            raise ValidationError(
                {'message': "Please provide decimal values for 'min_lat', 'max_lat', 'min_long', 'max_long'."})

    @classmethod
    def is_valid_longitude(cls, longitude):
        return -180 <= longitude <= 180

    @classmethod
    def is_valid_latitude(cls, latitude):
        return -90 <= latitude <= 90

    def is_in_square(self, square_params):
        return self.is_between_latitudes(square_params['min_lat'], square_params['max_lat']) and \
            self.is_between_longitudes(
                square_params['min_long'], square_params['max_long'])

    def is_between_longitudes(self, min_long, max_long):
        location_long = self.location_long
        if min_long > max_long:

            # 'Min' [left of] +180/-180 [left of] 'Max'
            # --> shift 'Max'
            max_long += 360

            if location_long < 0:
                # 'Min' [left of] +180/-180 [left of] 'MO'
                # --> shift 'MO'
                location_long += 360

        return min_long <= location_long <= max_long

    def is_between_latitudes(self, min_lat, max_lat):
        return min_lat <= self.location_lat <= max_lat
