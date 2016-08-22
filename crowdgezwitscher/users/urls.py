# pylint: disable=invalid-name
from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='list'),
    url(r'^new/$', views.UserCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.UserUpdate.as_view(), name='update'),
    url(r'^inactive$', views.InactiveUserListView.as_view(), name='list_inactive'),
]
