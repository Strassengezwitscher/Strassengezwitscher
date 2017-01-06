from datetime import timedelta

from TwitterAPI import TwitterAPI, TwitterConnectionError, TwitterRequestError

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

from crowdgezwitscher.models import MapObjectFilter
from crowdgezwitscher.log import logger
from events.filters import DateFilterBackend
from events.models import Event
from events.serializers import EventSerializer, EventSerializerShortened
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


# API Views
class EventAPIList(generics.ListAPIView):
    queryset = Event.objects.filter(active=True)
    serializer_class = EventSerializerShortened
    filter_backends = (MapObjectFilter, DateFilterBackend)


class EventAPIDetail(generics.RetrieveAPIView):
    queryset = Event.objects.filter(active=True)
    serializer_class = EventSerializer


@api_view(['GET'])
def get_tweets(request, pk, format=None):
    """Get tweets for Event with primary key pk.

    Searches for saved tweets matching the Event's registered hashtags, accounts and dates.
    The dates form an open interval.
    """
    event = get_object_or_404(Event, pk=pk)
    if not event.coverage:
        return Response([])

    tweets_ids = []

    for account in event.twitter_accounts.all():
        for tweet in account.tweet_set.all():
            if event.coverage_start <= tweet.created_at.date() <= event.coverage_end:
                if tweet.account in event.twitter_accounts.all():
                    event_hashtags = event.hashtags.all()
                    twitter_hashtags = tweet.hashtags.all()
                    if event_hashtags:
                        if any([hashtag in twitter_hashtags for hashtag in event_hashtags]):
                            tweets_ids.append(tweet.tweet_id)
                    else:
                        tweets_ids.append(tweet.tweet_id)

    return Response(tweets_ids)
