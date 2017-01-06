from django.contrib import admin

from events.models import Event, Attachment


class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('thumbnail',)

admin.site.register(Event)
admin.site.register(Attachment, AttachmentAdmin)
