from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

from events.models import Event
from events.forms import EventForm, AttachmentFormSet


class EventListView(PermissionRequiredMixin, ListView):
    permission_required = 'events.view_event'
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    ordering = '-date'


class EventDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'events.view_event'
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'


class EventCreate(PermissionRequiredMixin, CreateWithInlinesView):
    permission_required = 'events.add_event'
    model = Event
    inlines = [AttachmentFormSet]
    template_name = 'events/form.html'
    form_class = EventForm


class EventUpdate(PermissionRequiredMixin, UpdateWithInlinesView):
    permission_required = 'events.change_event'
    model = Event
    inlines = [AttachmentFormSet]
    template_name = 'events/form.html'
    form_class = EventForm


class EventDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'events.delete_event'
    model = Event
    template_name = 'events/delete.html'
    success_url = reverse_lazy('events:list')
    context_object_name = 'event'
