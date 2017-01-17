from rest_framework import generics

from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from base.fields import RoundingDecimalField
from base.models import MapObjectFilterBackend
from base.widgets import SelectizeSelectMultiple
from facebook.models import FacebookPage
from facebook.serializers import FacebookPageSerializer, FacebookPageSerializerShortened


class FacebookPageForm(forms.ModelForm):
    location_lat = RoundingDecimalField(
        max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )
    location_long = RoundingDecimalField(
        max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )

    class Meta:
        model = FacebookPage
        fields = ('name', 'active', 'location_long', 'location_lat', 'location', 'notes', 'events', 'internal_notes',)
        widgets = {
            'events': SelectizeSelectMultiple(),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


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
