from rest_framework import generics

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from events.models import Event
from events.serializers import EventSerializer


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/form.html'
    fields = [
        'name', 'active', 'location_long', 'location_lat', 'date', 'repetition_cycle', 'organizer',
        'type', 'url', 'counter_event', 'coverage'
    ]


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/form.html'
    fields = [
        'name', 'active', 'location_long', 'location_lat', 'date', 'repetition_cycle', 'organizer',
        'type', 'url', 'counter_event', 'coverage'
    ]


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/delete.html'
    success_url = reverse_lazy('events:list')
    context_object_name = 'event'


# API Views
class EventAPIList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventAPIDetail(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
