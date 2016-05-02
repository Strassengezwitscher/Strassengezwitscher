from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.twitter_redirect, name='twitter_redirect'),
    url(r'^map$', views.index, name='index'),
]