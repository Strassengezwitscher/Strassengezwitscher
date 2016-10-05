from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from django.utils.safestring import mark_safe

from facebook.models import FacebookPage
from events.models import Event
from blog.models import BlogEntry


def index(request):
    key_param = '&key=%s' % settings.GMAPS_API_KEY if not settings.DEBUG and not settings.INSECURE else ''
    return render(request, 'frontend.html', {'key_param': mark_safe(key_param)})


def landingpage(request):
    return render(request, 'landingpage.html')


@login_required
def intern_index(request):
    return render(request, 'dashboard.html', {
        'blogentry_count': BlogEntry.objects.count(),
        'facebook_page_count': FacebookPage.objects.count(),
        'event_count': Event.objects.count(),
        'active_user_count': User.objects.exclude(is_staff=True, is_active=False).count(),
        'inactive_user_count': User.objects.exclude(is_staff=True, is_active=True).count(),
    })


@login_required
def intern_mattermost(request):
    return render(request, 'mattermost.html')
