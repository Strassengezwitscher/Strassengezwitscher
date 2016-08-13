# pylint: disable=invalid-name
from django.conf.urls import url

from . import views

app_name = 'captcha'
urlpatterns = [
    url(r'^captcha/$', views.validate_captcha, name='validate_captcha'),
]
