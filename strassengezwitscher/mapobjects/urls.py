from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^mapobjects/$', views.MapObjectList.as_view(), name='list'),
    url(r'^mapobjects/(?P<pk>[0-9]+)/$', views.MapObjectDetail.as_view(), name='detail'),
]

