from datetime import datetime, timedelta

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

from base.models import MapObjectFilterBackend
from events.filters import DateFilterBackend
from events.models import Event
from events.serializers import EventSerializer, EventSerializerShortened
from events.forms import EventForm, AttachmentFormSet
from twitter.models import Tweet


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
    filter_backends = (MapObjectFilterBackend, DateFilterBackend)


class EventAPIDetail(generics.RetrieveAPIView):
    queryset = Event.objects.filter(active=True)
    serializer_class = EventSerializer


class EventAPIGetTweets(APIView):
    def get(self, request, pk, format=None):
        """Get tweets for Event with primary key pk.

        Searches for saved tweets matching the Event's registered hashtags, accounts and dates.
        The dates form an open interval.
        """
        event = get_object_or_404(Event, pk=pk, active=True)
        if not event.coverage:
            return Response([])

        event_hashtag_ids = [hashtag.id for hashtag in event.hashtags.all()]

        # Convert event coverage dates to datetimes as they will be compared to Tweets' creation datetimes.
        # The time part will be set to 00:00:00.
        # tweets_till would therefore be the earliest possible datetime for coverage_end. As we want to includes dates from
        # that date, we add another day to tweets_till.
        tweets_from = timezone.make_aware(datetime(
            event.coverage_start.year,
            event.coverage_start.month,
            event.coverage_start.day
        ))
        tweets_till = timezone.make_aware(datetime(
            event.coverage_end.year,
            event.coverage_end.month,
            event.coverage_end.day
        )) + timedelta(days=1)

        # It would be possible also use the __date field lookup of created_at before using __range.
        # This would allow using coverage_start and coverage_end, so no need for tweets_from and tweets_till.
        # However, this would nearly double the processing time.
        tweets = Tweet.objects.filter(
            account__in=event.twitter_accounts.all(),
            created_at__range=(tweets_from, tweets_till),
        )
        # If the event specifies hashtags, each tweet needs to include at least one of them.
        # Otherwise, there are no restrictions on tweets' hashtags.
        if event_hashtag_ids:
            tweets = tweets.filter(hashtags__in=event_hashtag_ids)

        # If a tweet and the event have multiple hashtags in common, the tweet is included multiple times.
        # We therefore need to call distinct().
        return Response([tweet.tweet_id for tweet in tweets.distinct()])
