# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160426_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='link_to_event',
            new_name='url',
        ),
    ]
