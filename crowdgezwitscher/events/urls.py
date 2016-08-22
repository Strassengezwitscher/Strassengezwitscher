# pylint: disable=invalid-name
from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    url(r'^$', views.EventListView.as_view(), name='list'),
    url(r'^new/$', views.EventCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.EventDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.EventUpdate.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.EventDelete.as_view(), name='delete'),
]
