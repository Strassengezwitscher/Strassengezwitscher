# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-03 17:41
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    """Adds the string representing hashtags of events to the hashtag table and connects events with these hashtags"""
    Event = apps.get_model('events', 'Event')
    Hashtag = apps.get_model('twitter', 'Hashtag')

    db_alias = schema_editor.connection.alias

    event_hashtag_dict = {}

    for event in Event.objects.using(db_alias).all():
        event_hashtag_dict[event.id] = []
        for hashtag in event.twitter_hashtags.split(','):
            new_hashtag, _ = Hashtag.objects.using(db_alias).get_or_create(hashtag_text=hashtag)
            event_hashtag_dict[event.id].append(new_hashtag)

    for event_id in event_hashtag_dict:
        for hashtag in event_hashtag_dict[event_id]:
            hashtag.events.add(event_id)


def reverse_func(apps, schema_editor):
    """The reverse of the above"""
    Event = apps.get_model('events', 'Event')
    Hashtag = apps.get_model('twitter', 'Hashtag')

    db_alias = schema_editor.connection.alias

    event_hashtag_dict = {}

    for hashtag in Hashtag.objects.using(db_alias).all():
        for event in hashtag.events.all():
            if not event.id in event_hashtag_dict:
                event_hashtag_dict[event.id] = []
            event_hashtag_dict[event.id].append(hashtag.hashtag_text)

    for event_id in event_hashtag_dict:
        event = Event.objects.using(db_alias).get(id=event_id)
        event.twitter_hashtags =  ','.join(event_hashtag_dict[event_id])
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160919_1550'),
        ('twitter', '0002_hashtag_events'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
