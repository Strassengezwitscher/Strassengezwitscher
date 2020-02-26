# pylint: disable=invalid-name
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views_api as views

app_name = 'events_api'
urlpatterns_raw = (
    url(r'^events/$', views.EventAPIList.as_view(), name='list'),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventAPIDetail.as_view(), name='detail'),
    url(r'^events/(?P<pk>[0-9]+)/tweets$', views.EventAPIGetTweets.as_view(), name='tweets'),
    url(r'^events/new/$', views.send_form, name='send_form'),
    url(r'^events/years/$', views.EventAPIYears.as_view(), name='years'),
)
urlpatterns = format_suffix_patterns(urlpatterns_raw, allowed=['json'])
