from rest_framework import generics

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm, ModelMultipleChoiceField
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from crowdgezwitscher.models import MapObjectFilter
from crowdgezwitscher.widgets import SelectizeSelectMultiple
from events.models import Event
from events.serializers import EventSerializer, EventSerializerShortened
from facebook.models import FacebookPage


class EventForm(ModelForm):
    facebook_pages = ModelMultipleChoiceField(
        queryset=FacebookPage.objects.all(),
        required=False,
        widget=SelectizeSelectMultiple()
    )

    class Meta:
        model = Event
        fields = (
            'name', 'active', 'location_long', 'location_lat', 'date', 'repetition_cycle', 'organizer',
            'type', 'url', 'counter_event', 'coverage', 'facebook_pages'
        )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['facebook_pages'] = self.instance.facebook_pages.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super(EventForm, self).save(*args, **kwargs)
        if instance.pk:
            instance.facebook_pages.clear()
            instance.facebook_pages.add(*self.cleaned_data['facebook_pages'])
        return instance


class EventListView(PermissionRequiredMixin, ListView):
    permission_required = 'events.view_event'
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'


class EventDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'events.view_event'
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'


class EventCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'events.add_event'
    model = Event
    template_name = 'events/form.html'
    form_class = EventForm


class EventUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'events.change_event'
    model = Event
    template_name = 'events/form.html'
    form_class = EventForm


class EventDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'events.delete_event'
    model = Event
    template_name = 'events/delete.html'
    success_url = reverse_lazy('events:list')
    context_object_name = 'event'


# API Views
class EventAPIList(generics.ListAPIView):
    queryset = Event.objects.filter(active=True)
    serializer_class = EventSerializerShortened
    filter_backends = (MapObjectFilter,)


class EventAPIDetail(generics.RetrieveAPIView):
    queryset = Event.objects.filter(active=True)
    serializer_class = EventSerializer
