# pylint: disable=invalid-name
from django.conf.urls import url

from . import views

app_name = 'blogs'
urlpatterns = [
    url(r'^$', views.BlogListView.as_view(), name='list'),
    url(r'^new/$', views.BlogCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.BlogDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.BlogUpdate.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.BlogDelete.as_view(), name='delete'),
]
