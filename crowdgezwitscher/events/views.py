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
from crowdgezwitscher.widgets import SelectizeSelectMultiple, SelectizeCSVInput, BootstrapDatepicker
from crowdgezwitscher.log import logger
from events.filters import DateFilterBackend
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
            'name', 'active', 'location_long', 'location_lat', 'location', 'date', 'repetition_cycle', 'organizer',
            'type', 'url', 'counter_event', 'coverage', 'facebook_pages', 'twitter_account_names', 'twitter_hashtags',
            'coverage_start', 'coverage_end',
        )
        widgets = {
            'coverage_start': BootstrapDatepicker(),
            'coverage_end': BootstrapDatepicker(),
            'date': BootstrapDatepicker(),
            'twitter_account_names': SelectizeCSVInput(),
            'twitter_hashtags': SelectizeCSVInput(),
        }

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
    ordering = '-date'


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

    Searches for tweets matching the Event's registered hashtags, accounts and dates. The dates form an open interval.
    Modify TWITTER_TWEET_COUNT to change the maximum number of returned tweet IDs.
    """
    event = get_object_or_404(Event, pk=pk)
    if not event.coverage:
        return Response([])
    query = event.build_twitter_search_query()
    if not query:
        return Response({'status': 'error', 'errors': 'Twitter not or improperly configured for this event.'},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)
    since = event.coverage_start.strftime('%Y-%m-%d')
    until = (event.coverage_end + timedelta(days=1)).strftime('%Y-%m-%d')  # to get tweets including coverage_end
    twitter = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                         settings.TWITTER_CONSUMER_SECRET,
                         auth_type='oAuth2')
    try:
        tweets = twitter.request('search/tweets', {'q': query,
                                                   'count': settings.TWITTER_TWEET_COUNT,
                                                   'since': since,
                                                   'until': until})
    except TwitterConnectionError:
        logger.warning("Could not connect to Twitter.")
        return Response([])
    res = []
    try:
        for tweet in tweets:
            try:
                res.append(tweet['id_str'])
            except KeyError:
                logger.warning("Got tweet without expected fields.")
                continue
    except TwitterRequestError as e:
        if e.status_code == 429:
            logger.warning("Twitter rate limit exhausted")
        else:
            logger.warning("TwitterRequestError, status code: %d", e.status_code)
    return Response(res)
