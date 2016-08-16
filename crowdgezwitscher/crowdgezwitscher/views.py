from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from facebook.models import FacebookPage
from events.models import Event


def index(request):
    return render(request, 'frontend.html')


@login_required
def intern_index(request):
    return render(request, 'dashboard.html', {
        'facebook_page_count': FacebookPage.objects.count(),
        'event_count': Event.objects.count(),
        'active_user_count': User.objects.exclude(is_staff=True, is_active=False).count(),
        'inactive_user_count': User.objects.exclude(is_staff=True, is_active=True).count(),
    })
