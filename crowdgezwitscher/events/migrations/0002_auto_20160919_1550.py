# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-19 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='coverage_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='coverage_start',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='twitter_account_names',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='event',
            name='twitter_hashtags',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
