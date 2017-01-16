from rest_framework import generics

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from base.models import MapObjectFilterBackend
from facebook.forms import FacebookPageForm
from facebook.models import FacebookPage
from facebook.serializers import FacebookPageSerializer, FacebookPageSerializerShortened


class FacebookPageListView(PermissionRequiredMixin, ListView):
    permission_required = 'facebook.view_facebookpage'
    model = FacebookPage
    template_name = 'facebook/list.html'
    context_object_name = 'pages'


class FacebookPageDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'facebook.view_facebookpage'
    model = FacebookPage
    template_name = 'facebook/detail.html'
    context_object_name = 'page'


class FacebookPageCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'facebook.add_facebookpage'
    model = FacebookPage
    template_name = 'facebook/form.html'
    form_class = FacebookPageForm


class FacebookPageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'facebook.change_facebookpage'
    model = FacebookPage
    template_name = 'facebook/form.html'
    form_class = FacebookPageForm


class FacebookPageDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'facebook.delete_facebookpage'
    model = FacebookPage
    template_name = 'facebook/delete.html'
    success_url = reverse_lazy('facebook:list')
    context_object_name = 'page'


# API Views
class FacebookPageAPIList(generics.ListAPIView):
    queryset = FacebookPage.objects.filter(active=True)
    serializer_class = FacebookPageSerializerShortened
    filter_backends = (MapObjectFilterBackend,)


class FacebookPageAPIDetail(generics.RetrieveAPIView):
    queryset = FacebookPage.objects.filter(active=True)
    serializer_class = FacebookPageSerializer
