"""crowdgezwitscher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Django admin URLs
    url(r'^admin/', admin.site.urls),

    # API URLs
    url(r'^api/', include('facebook.urls_api', namespace='facebook_api')),
    url(r'^api/', include('events.urls_api', namespace='events_api')),
    url(r'^api/', include('contact.urls')),
    url(r'^api/', include('captcha.urls')),

    # Admin area URLs
    url(r'^intern/facebook/', include('facebook.urls', namespace='facebook')),
    url(r'^intern/events/', include('events.urls', namespace='events')),
    url(r'^intern/users/', include('users.urls', namespace='users')),
    url(r'^intern/$', views.intern_index, name='intern'),
    url(r'^intern/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^intern/logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^intern/mattermost/$', views.intern_mattermost, name='mattermost'),

    # User area URLs
    url(r'^$', views.landingpage, name='landingpage'),
    url(r'^map/$', views.index, name='map'),
    url(r'^contact/$', views.index, name='contact'),
    url(r'^imprint/$', views.index, name='imprint'),
    url(r'^about/$', views.index, name='about'),

    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),
]
