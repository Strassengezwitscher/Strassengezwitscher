from datetime import timedelta

from TwitterAPI import TwitterAPI, TwitterConnectionError, TwitterRequestError

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, api_view, parser_classes
from rest_framework.parsers import JSONParser

from django.conf import settings
from django.shortcuts import get_object_or_404

from base.models import MapObjectFilterBackend
from crowdgezwitscher.log import logger
from crowdgezwitscher.auth import CsrfExemptSessionAuthentication
from events.filters import DateFilterBackend
from events.models import Event
from events.serializers import EventSerializer, EventSerializerShortened, EventSerializerCreate


class EventAPIList(generics.ListAPIView):
    queryset = Event.objects.filter(active=True)
    serializer_class = EventSerializerShortened
    filter_backends = (
        DateFilterBackend,
        MapObjectFilterBackend,
    )


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

@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@parser_classes((JSONParser,))
def send_form(request):
    serializer = EventSerializerCreate(data=request.data)
    if not serializer.is_valid():
        return Response({'status': 'error', 'message': 'Fehler beim Speichern der Informationen. \n' + '\n'.join([serializer.errors[msg][0] for msg in serializer.errors])},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        serializer.save()
    except Exception as e:
        return Response({'status': 'error', 'message': 'Fehler beim Speichern der Informationen.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})
