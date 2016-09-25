from rest_framework import generics

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from events.models import Event
from events.serializers import EventSerializer, EventSerializerShortened
from crowdgezwitscher.models import MapObjectFilter


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
    fields = [
        'name', 'active', 'location_long', 'location_lat', 'date', 'repetition_cycle', 'organizer',
        'type', 'url', 'counter_event', 'coverage', 'twitter_account_names', 'twitter_hashtags',
        'coverage_start', 'coverage_end'
    ]


class EventUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'events.change_event'
    model = Event
    template_name = 'events/form.html'
    fields = [
        'name', 'active', 'location_long', 'location_lat', 'date', 'repetition_cycle', 'organizer',
        'type', 'url', 'counter_event', 'coverage', 'twitter_account_names', 'twitter_hashtags',
        'coverage_start', 'coverage_end'
    ]


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
