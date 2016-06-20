from django.conf.urls import url

from . import views

app_name = 'facebook'
urlpatterns = [
    url(r'^$', views.FacebookPageListView.as_view(), name='list'),
    url(r'^new/$', views.FacebookPageCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.FacebookPageDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.FacebookPageUpdate.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.FacebookPageDelete.as_view(), name='delete'),
]
