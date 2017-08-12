# -*- coding: utf-8 -*-
from django import forms
from extra_views import InlineFormSet

from base.fields import ModelMultipleChoiceImplicitCreationField, RoundingDecimalField
from base.widgets import (
    SelectizeSelectMultiple, AttachmentInput,
    BootstrapDatePicker, ClearableBootstrapDatePicker, ClearableBootstrapTimePicker,
)
from events.models import Event, Attachment
from facebook.models import FacebookPage
from twitter.models import Hashtag, TwitterAccount


class AttachmentForm(forms.ModelForm):
    class Meta:
        fields = (
            'attachment',
            'description',
            'public',
        )
        widgets = {
            'attachment': AttachmentInput(),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    class Media:
        js = (
            'django-formset/dist/django-formset.js',
        )


class AttachmentFormSet(InlineFormSet):
    model = Attachment
    extra = 1
    form_class = AttachmentForm


class EventForm(forms.ModelForm):
    location_lat = RoundingDecimalField(
        max_digits=9,
        decimal_places=6,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )
    location_long = RoundingDecimalField(
        max_digits=9,
        decimal_places=6,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )
    facebook_pages = forms.ModelMultipleChoiceField(
        queryset=FacebookPage.objects.all(),
        required=False,
        widget=SelectizeSelectMultiple()
    )

    twitter_hashtags = ModelMultipleChoiceImplicitCreationField(
        queryset=Hashtag.objects.all().order_by('hashtag_text'),
        prefix='__new_hashtag__',
        attr_name='hashtag_text',
        required=False
    )

    twitter_account_names = ModelMultipleChoiceImplicitCreationField(
        queryset=TwitterAccount.objects.all().order_by('name'),
        prefix='__new_account__',
        attr_name='name',
        required=False,
    )

    class Meta:
        model = Event
        fields = (
            'active',
            'counter_event',
            'coverage',
            'coverage_end',
            'coverage_start',
            'date',
            'facebook_pages',
            'internal_notes',
            'location',
            'location_lat',
            'location_long',
            'name',
            'notes',
            'organizer',
            'participants',
            'repetition_cycle',
            'type',
            'twitter_account_names',
            'twitter_hashtags',
            'url',
            'time',
        )
        widgets = {
            'coverage_start': ClearableBootstrapDatePicker(),
            'coverage_end': ClearableBootstrapDatePicker(),
            'date': BootstrapDatePicker(),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'participants': forms.TextInput(attrs={'class': 'form-control'}),
            'organizer': forms.TextInput(attrs={'class': 'form-control'}),
            'repetition_cycle': forms.TextInput(attrs={'class': 'form-control'}),
            'time': ClearableBootstrapTimePicker(),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.initial['facebook_pages'] = self.instance.facebook_pages.values_list('pk', flat=True)
            self.initial['twitter_hashtags'] = self.instance.hashtags.values_list('pk', flat=True)
            self.initial['twitter_account_names'] = self.instance.twitter_accounts.values_list('pk', flat=True)

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        coverage = cleaned_data.get('coverage')
        twitter_account_names = cleaned_data.get('twitter_account_names')
        coverage_start = cleaned_data.get('coverage_start')
        coverage_end = cleaned_data.get('coverage_end')

        # coverage dates must be in correct order
        if coverage_start is not None and coverage_end is not None:
            if coverage_end < coverage_start:
                msg = "'coverage_start' muss vor 'coverage_end' liegen"
                self.add_error('coverage_start', msg)
                self.add_error('coverage_end', msg)

        # for activating a coverage all required parameters must be set
        if coverage:
            msg = "Wird für eine Berichterstattung benötigt"
            errors = []
            if coverage_start is None:
                errors.append(('coverage_start', msg))
            if coverage_end is None:
                errors.append(('coverage_end', msg))
            if twitter_account_names is None or len(twitter_account_names) == 0:
                errors.append(('twitter_account_names', msg))
            if errors:
                for error in errors:
                    self.add_error(*error)
                self.add_error('coverage', "Nicht alle benötigen Felder wurden ausgefüllt")

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
