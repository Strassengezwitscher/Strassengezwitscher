# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-31 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
