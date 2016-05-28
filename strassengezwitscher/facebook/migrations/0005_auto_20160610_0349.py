# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0004_auto_20160528_0229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facebookpage',
            old_name='link_to_facebook',
            new_name='url',
        ),
    ]
