from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'frontend.html')


@login_required
def intern_index(request):
    return render(request, 'admin.html')
