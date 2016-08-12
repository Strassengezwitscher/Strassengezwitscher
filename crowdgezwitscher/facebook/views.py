from rest_framework import generics

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from facebook.models import FacebookPage
from facebook.serializers import FacebookPageSerializer


class FacebookPageListView(LoginRequiredMixin, ListView):
    model = FacebookPage
    template_name = 'facebook/list.html'
    context_object_name = 'pages'


class FacebookPageDetail(LoginRequiredMixin, DetailView):
    model = FacebookPage
    template_name = 'facebook/detail.html'
    context_object_name = 'page'


class FacebookPageCreate(LoginRequiredMixin, CreateView):
    model = FacebookPage
    template_name = 'facebook/form.html'
    fields = ['name', 'active', 'location_long', 'location_lat']


class FacebookPageUpdate(LoginRequiredMixin, UpdateView):
    model = FacebookPage
    template_name = 'facebook/form.html'
    fields = ['name', 'active', 'location_long', 'location_lat']


class FacebookPageDelete(LoginRequiredMixin, DeleteView):
    model = FacebookPage
    template_name = 'facebook/delete.html'
    success_url = reverse_lazy('facebook:list')
    context_object_name = 'page'


# API Views
class FacebookPageAPIList(generics.ListAPIView):
    queryset = FacebookPage.objects.all()
    serializer_class = FacebookPageSerializer


class FacebookPageAPIDetail(generics.RetrieveAPIView):
    queryset = FacebookPage.objects.all()
    serializer_class = FacebookPageSerializer
