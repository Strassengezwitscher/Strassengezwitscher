from django.contrib import admin

from events.models import Event, Attachment


admin.site.register(Event)
admin.site.register(Attachment)
