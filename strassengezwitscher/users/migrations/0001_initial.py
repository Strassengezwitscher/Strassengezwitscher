# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


def forwards_func(apps, schema_editor):
    """Creates the groups "Administratoren" and "Moderatoren" and sets their permissions."""
    # We can't import the models directly as they may be newer versions than this migration expects.
    # We use the historical versions instead.
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Event = apps.get_model('events', 'Event')
    FacebookPage = apps.get_model('facebook', 'FacebookPage')

    db_alias = schema_editor.connection.alias

    # We rely on Permissions to exist. We do not create any, we just assign them to the Groups we create.
    # However, Permissions are created at the end of migrations, too late for us if we start with an empty DB.
    # We therefore emit the "post_migrate" signal. This results in permissions being already created when we need them.
    # Further info: https://code.djangoproject.com/ticket/23422
    # required args seem to change with nearly every Django release...
    emit_post_migrate_signal(verbosity=0, interactive=False, db=db_alias)

    admins = Group.objects.using(db_alias).create(name="Administratoren")
    mods   = Group.objects.using(db_alias).create(name="Moderatoren")

    # grant all privileges on the following models to mods and admins
    for model in [Event, FacebookPage]:
        content_type = ContentType.objects.get_for_model(model)
        perms = Permission.objects.using(db_alias).filter(content_type=content_type)
        mods.permissions.add(*perms)
        admins.permissions.add(*perms)

    # allow admins to add and change users (deletion is forbidden in favor of making users 'inactive')
    user_content_type = ContentType.objects.get_for_model(User)
    perms = Permission.objects.using(db_alias).filter(content_type=user_content_type).exclude(codename__contains='delete')
    admins.permissions.add(*perms)


def reverse_func(apps, schema_editor):
    """Deletes the groups "Administratoren" and "Moderatoren."""
    Group = apps.get_model('auth', 'Group')
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).filter(name="Administratoren").delete()
    Group.objects.using(db_alias).filter(name="Moderatoren").delete()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
