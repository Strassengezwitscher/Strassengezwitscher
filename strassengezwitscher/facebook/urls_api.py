# pylint: disable=invalid-name
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'facebook_api'
urlpatterns_raw = (
    url(r'^facebook/$', views.FacebookPageAPIList.as_view(), name='list'),
    url(r'^facebook/(?P<pk>[0-9]+)/$', views.FacebookPageAPIDetail.as_view(), name='detail'),
)
urlpatterns = format_suffix_patterns(urlpatterns_raw, allowed=['json'])
