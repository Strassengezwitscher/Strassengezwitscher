# -*- coding: utf-8 -*-
from django import forms
from extra_views import InlineFormSet

from base.fields import RoundingDecimalField
from base.widgets import (
    SelectizeSelectMultiple, SelectizeCSVInput, AttachmentInput,
    BootstrapDatePicker, ClearableBootstrapDatePicker, ClearableBootstrapTimePicker,
)
from events.models import Event, Attachment
from facebook.models import FacebookPage


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
    location_lat = RoundingDecimalField(
        max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )
    location_long = RoundingDecimalField(
        max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )
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
            'coverage_start', 'coverage_end', 'participants', 'time', 'notes', 'internal_notes',
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
            'twitter_account_names': SelectizeCSVInput(),
            'twitter_hashtags': SelectizeCSVInput(),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.initial['facebook_pages'] = self.instance.facebook_pages.values_list('pk', flat=True)

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
            msg = u'Wird für eine Berichterstattung benötigt'
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
                self.add_error('coverage', u'Nicht alle benötigen Felder wurden ausgefüllt')

    def save(self, *args, **kwargs):
        instance = super(EventForm, self).save(*args, **kwargs)
        if instance.pk:
            instance.facebook_pages.clear()
            instance.facebook_pages.add(*self.cleaned_data['facebook_pages'])
        return instance
