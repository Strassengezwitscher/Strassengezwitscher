from django import forms
from extra_views import InlineFormSet

from events.models import Event, Attachment
from facebook.models import FacebookPage
from crowdgezwitscher.widgets import SelectizeSelectMultiple, SelectizeCSVInput, BootstrapDatepicker, AttachmentInput


class AttachmentForm(forms.ModelForm):
    class Meta:
        fields = ('attachment', 'description')
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'attachment': AttachmentInput(),
        }

    class Media:
        js = ('django-formset/dist/django-formset.js',)


class AttachmentFormSet(InlineFormSet):
    model = Attachment
    extra = 1
    form_class = AttachmentForm


class EventForm(forms.ModelForm):
    facebook_pages = forms.ModelMultipleChoiceField(
        queryset=FacebookPage.objects.all(),
        required=False,
        widget=SelectizeSelectMultiple()
    )

    class Meta:
        model = Event
        fields = (
            'name', 'active', 'location_long', 'location_lat', 'location', 'date', 'repetition_cycle', 'organizer',
            'type', 'url', 'counter_event', 'coverage', 'facebook_pages', 'twitter_account_names', 'twitter_hashtags',
            'coverage_start', 'coverage_end', 'participants',
        )
        widgets = {
            'coverage_start': BootstrapDatepicker(),
            'coverage_end': BootstrapDatepicker(),
            'date': BootstrapDatepicker(),
            'location_long': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'location_lat': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'participants': forms.TextInput(attrs={'class': 'form-control'}),
            'organizer': forms.TextInput(attrs={'class': 'form-control'}),
            'repetition_cycle': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_account_names': SelectizeCSVInput(),
            'twitter_hashtags': SelectizeCSVInput(),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
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
