from django.conf.urls import url
from . import views

app_name = 'mapobjects'
urlpatterns = [
    url(r'^$', views.MapObjectList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.MapObjectDetail.as_view(), name='detail'),
]
