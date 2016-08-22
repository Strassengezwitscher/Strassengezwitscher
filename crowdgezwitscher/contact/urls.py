# pylint: disable=invalid-name
from django.conf.urls import url

from . import views

app_name = 'contact'
urlpatterns = [
    url(r'^contact/$', views.send_form, name='send_form'),
]
