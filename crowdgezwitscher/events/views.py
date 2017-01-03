from datetime import timedelta

from TwitterAPI import TwitterAPI, TwitterConnectionError, TwitterRequestError

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm, ModelMultipleChoiceField
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from crowdgezwitscher.models import MapObjectFilter
from crowdgezwitscher.widgets import SelectizeSelectMultiple, SelectizeCSVInput
from crowdgezwitscher.log import logger
from events.filters import DateFilterBackend
from events.models import Event
from events.serializers import EventSerializer, EventSerializerShortened
from facebook.models import FacebookPage
from twitter.models import Hashtag, TwitterAccount

class EventForm(ModelForm):
    facebook_pages = ModelMultipleChoiceField(
        queryset=FacebookPage.objects.all(),
        required=False,
        widget=SelectizeSelectMultiple()
    )

    twitter_hashtags = ModelMultipleChoiceField(
        queryset=Hashtag.objects.all().order_by('hashtag_text'),
        required=False,
        widget=SelectizeSelectMultiple()
    )

    twitter_account_names = ModelMultipleChoiceField(
        queryset=TwitterAccount.objects.all().order_by('name'),
        required=False,
        widget=SelectizeSelectMultiple()
    )

    class Meta:
        model = Event
        fields = (
            'name', 'active', 'location_long', 'location_lat', 'location', 'date', 'repetition_cycle', 'organizer',
            'type', 'url', 'counter_event', 'coverage', 'facebook_pages', 'twitter_account_names', 'twitter_hashtags',
            'coverage_start', 'coverage_end',
        )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['facebook_pages'] = self.instance.facebook_pages.values_list('pk', flat=True)
            self.initial['twitter_hashtags'] = self.instance.hashtags.values_list('pk', flat=True)
            self.initial['twitter_account_names'] = self.instance.twitter_accounts.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super(EventForm, self).save(*args, **kwargs)
        if instance.pk:
            instance.facebook_pages.clear()
            instance.facebook_pages.add(*self.cleaned_data['facebook_pages'])

            instance.hashtags.clear()
            instance.hashtags.add(*self.cleaned_data['twitter_hashtags'])

            instance.twitter_accounts.clear()
            instance.twitter_accounts.add(*self.cleaned_data['twitter_account_names'])
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
