# pylint: disable=invalid-name
from django.conf.urls import url

from . import views

app_name = 'twitter'
urlpatterns = [
    url(r'^$', views.TwitterAccountListView.as_view(), name='list'),
    url(r'^new/$', views.TwitterAccountCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.TwitterAccountDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.TwitterAccountDelete.as_view(), name='delete'),
    url(r'^(?P<pk>[0-9]+)/fetch/$', views.fetch_tweets, name='fetch_tweets'),
]
