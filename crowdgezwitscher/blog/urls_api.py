# pylint: disable=invalid-name
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views_api as views

app_name = 'blog_api'
urlpatterns_raw = (
    url(r'^blog/$', views.BlogAPIList.as_view(), name='list'),
    url(r'^blog/(?P<pk>[0-9]+)/$', views.BlogAPIDetail.as_view(), name='detail'),
)
urlpatterns = format_suffix_patterns(urlpatterns_raw, allowed=['json'])
