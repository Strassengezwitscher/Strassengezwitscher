from django.test import TestCase
from rest_framework.exceptions import ValidationError

from strassengezwitscher.models import MapObject


class MapObjectModelTests(TestCase):
    def test_representation(self):
        obj = MapObject(name='Test')
        self.assertEqual(repr(obj), '<MapObject Test>')

    def test_string_representation(self):
        obj = MapObject(name='Test')
        self.assertEqual(str(obj), 'Test')

    ###############################
    # Test is_between_longitudes()
    ###############################

    #
    # Case 1: Min' < 'Max' --> no shift of points
    #

    # 'MO' [left of] 'Min' [left of] 'Max'
    def test_is_between_longitudes_a(self):
        min_long = 100
        location_long = 0
        max_long = 150

        obj = MapObject(location_long=location_long)
        self.assertFalse(obj.is_between_longitudes(min_long=min_long, max_long=max_long))

    # 'Min' [left of] 'MO' [left of] 'Max'
    def test_is_between_longitudes_b(self):
        min_long = 100
        location_long = 130
        max_long = 150

        obj = MapObject(location_long=location_long)
        self.assertTrue(obj.is_between_longitudes(min_long=min_long, max_long=max_long))

    # 'Min' [left of] 'Max' [left of] 'MO'
    def test_is_between_longitudes_c(self):
        min_long = 100
        location_long = 170
        max_long = 150

        obj = MapObject(location_long=location_long)
        self.assertFalse(obj.is_between_longitudes(min_long=min_long, max_long=max_long))

    #
    # Case 2: 'Min' > 'Max'
    # --> 'Min' [left of] +180/-180 [left of] 'Max'
    #

    # 'MO' [left of] 'Min' [left of] +180/-180 [left of] 'Max'
    # --> 'Max' has to be shifted
    def test_is_between_longitudes_d(self):
        min_long = 45
        location_long = 20
        max_long = -160

        obj = MapObject(location_long=location_long)
        self.assertFalse(obj.is_between_longitudes(min_long=min_long, max_long=max_long))

    # 'Min' [left of] 'MO' [left of] +180/-180 [left of] 'Max'
    # --> 'Max' has to be shifted
    def test_is_between_longitudes_e(self):
        min_long = 45
        location_long = 60
        max_long = -160

        obj = MapObject(location_long=location_long)
        self.assertTrue(obj.is_between_longitudes(min_long=min_long, max_long=max_long))

    # 'Min' [left of] +180/-180 [left of] 'MO' [left of] 'Max'
    # --> 'Max' and 'MO' have to be shifted
    def test_is_between_longitudes_f(self):
        min_long = 45
        location_long = -170
        max_long = -160

        obj = MapObject(location_long=location_long)
        self.assertTrue(obj.is_between_longitudes(min_long=min_long, max_long=max_long))

    # 'Min' [left of] +180/-180 [left of] 'Max' [left of] 'MO'
    # --> 'Max' and 'MO' have to be shifted
    def test_is_between_longitudes_g(self):
        min_long = 45
        location_long = -120
        max_long = -160

        obj = MapObject(location_long=location_long)
        self.assertFalse(obj.is_between_longitudes(min_long=min_long, max_long=max_long))

    ###############################
    # Test is_between_latitudes()
    ###############################

    def test_is_between_latitudes_below(self):
        min_lat = 30
        location_lat = 10
        max_lat = 50

        obj = MapObject(location_lat=location_lat)
        self.assertFalse(obj.is_between_latitudes(min_lat=min_lat, max_lat=max_lat))

    def test_is_between_latitudes_inside(self):
        min_lat = 30
        location_lat = 40
        max_lat = 50

        obj = MapObject(location_lat=location_lat)
        self.assertTrue(obj.is_between_latitudes(min_lat=min_lat, max_lat=max_lat))

    def test_is_between_latitudes_above(self):
        min_lat = 30
        location_lat = 60
        max_lat = 50

        obj = MapObject(location_lat=location_lat)
        self.assertFalse(obj.is_between_latitudes(min_lat=min_lat, max_lat=max_lat))

    ###############################
    # Test is_valid_longitude()
    ###############################

    def test_is_valid_longitude_too_high(self):
        longitude = 181
        self.assertFalse(MapObject.is_valid_longitude(longitude))

    def test_is_valid_longitude_too_low(self):
        longitude = -181
        self.assertFalse(MapObject.is_valid_longitude(longitude))

    def test_is_valid_longitude_high_correct(self):
        longitude = 180
        self.assertTrue(MapObject.is_valid_longitude(longitude))

    def test_is_valid_longitude_low_correct(self):
        longitude = -180
        self.assertTrue(MapObject.is_valid_longitude(longitude))

    ###############################
    # Test is_valid_latitude()
    ###############################

    def test_is_valid_latitude_too_high(self):
        latitude = 91
        self.assertFalse(MapObject.is_valid_latitude(latitude))

    def test_is_valid_latitude_too_low(self):
        latitude = -91
        self.assertFalse(MapObject.is_valid_latitude(latitude))

    def test_is_valid_latitude_high_correct(self):
        latitude = 90
        self.assertTrue(MapObject.is_valid_latitude(latitude))

    def test_is_valid_latitude_low_correct(self):
        latitude = -90
        self.assertTrue(MapObject.is_valid_latitude(latitude))

    ###############################
    # Test are_valid_rect_params()
    ###############################

    def test_are_valid_params_incomplete(self):

        rect_params = {
            'min_lat': None,
            'max_lat': '40.0',
            'min_long': '80.0',
            'max_long': '90.0'
        }
        with self.assertRaises(ValidationError):
            MapObject.get_as_decimals(rect_params)

    def test_are_valid_params_no_numeric(self):
        rect_params = {
            'min_lat': 'abcd',
            'max_lat': '40.0',
            'min_long': '80.0',
            'max_long': '90.0'
        }
        with self.assertRaises(ValidationError):
            MapObject.get_as_decimals(rect_params)

    def test_are_valid_params(self):
        rect_params = {
            'min_lat': '30.0',
            'max_lat': '40.0',
            'min_long': '80.0',
            'max_long': '90.0'
        }

        rect_params_decimals = MapObject.get_as_decimals(rect_params)
        self.assertEqual(rect_params_decimals['min_lat'], 30.0)
        self.assertEqual(rect_params_decimals['max_lat'], 40.0)
        self.assertEqual(rect_params_decimals['min_long'], 80.0)
        self.assertEqual(rect_params_decimals['max_long'], 90.0)
