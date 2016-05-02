from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def twitter_redirect(request):
    return render(request, 'twitter_redirect.html')
