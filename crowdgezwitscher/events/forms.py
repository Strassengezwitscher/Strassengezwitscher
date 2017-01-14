from django import forms
from extra_views import InlineFormSet

from base.widgets import (
    SelectizeSelectMultiple, SelectizeSelectMultipleCSVInput, AttachmentInput,
    BootstrapDatePicker, ClearableBootstrapDatePicker, ClearableBootstrapTimePicker,
)
from events.models import Event, Attachment
from facebook.models import FacebookPage
from twitter.models import Hashtag, TwitterAccount


class AttachmentForm(forms.ModelForm):
    class Meta:
        fields = ('attachment', 'description', 'public')
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

    twitter_hashtags = forms.ModelMultipleChoiceField(
        queryset=Hashtag.objects.all().order_by('hashtag_text'),
        required=False,
        widget=SelectizeSelectMultipleCSVInput()
    )

    twitter_account_names = forms.ModelMultipleChoiceField(
        queryset=TwitterAccount.objects.all().order_by('name'),
        required=False,
        widget=SelectizeSelectMultiple()
    )

    class Meta:
        model = Event
        fields = (
            'name', 'active', 'location_long', 'location_lat', 'location', 'date', 'repetition_cycle', 'organizer',
            'type', 'url', 'counter_event', 'coverage', 'facebook_pages', 'twitter_account_names', 'twitter_hashtags',
            'coverage_start', 'coverage_end', 'participants', 'time', 'notes',
        )
        widgets = {
            'coverage_start': ClearableBootstrapDatePicker(),
            'coverage_end': ClearableBootstrapDatePicker(),
            'date': BootstrapDatePicker(),
            'time': ClearableBootstrapTimePicker(),
            'location_long': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'location_lat': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'participants': forms.TextInput(attrs={'class': 'form-control'}),
            'organizer': forms.TextInput(attrs={'class': 'form-control'}),
            'repetition_cycle': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.initial['facebook_pages'] = self.instance.facebook_pages.values_list('pk', flat=True)
            self.initial['twitter_hashtags'] = self.instance.hashtags.values_list('pk', flat=True)
            self.initial['twitter_account_names'] = self.instance.twitter_accounts.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super(EventForm, self).save(*args, **kwargs)
        if instance.pk:
            instance.facebook_pages.clear()
            instance.facebook_pages.add(*self.cleaned_data['facebook_pages'])

            instance.hashtags.clear()
            instance.hashtags.add(*self.cleaned_data['twitter_hashtags'])

            instance.twitter_accounts.clear()
            instance.twitter_accounts.add(*self.cleaned_data['twitter_account_names'])
        return instance

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        cleaned_hashtags = []

        for hashtag in self['twitter_hashtags'].value():
            if hashtag.startswith("__new_hashtag__"):
                hashtag_db, _ = Hashtag.objects.get_or_create(hashtag_text=hashtag.split("__new_hashtag__")[1])
                cleaned_hashtags.append(hashtag_db)
            else:
                cleaned_hashtags.append(Hashtag.objects.get(pk=int(hashtag)))

        if 'twitter_hashtags' in self.errors:
            del self.errors['twitter_hashtags']
        self.cleaned_data['twitter_hashtags'] = cleaned_hashtags
        return cleaned_data
