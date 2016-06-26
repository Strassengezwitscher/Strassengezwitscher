# pylint: disable=invalid-name
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'mapobjects'
urlpatterns_raw = (
    url(r'^$', views.MapObjectList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.MapObjectDetail.as_view(), name='detail'),
)
urlpatterns = format_suffix_patterns(urlpatterns_raw, allowed=['json'])
