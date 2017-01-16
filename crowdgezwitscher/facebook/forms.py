# -*- coding: utf-8 -*-
from django import forms

from base.fields import RoundingDecimalField
from base.widgets import SelectizeSelectMultiple
from facebook.models import FacebookPage


class FacebookPageForm(forms.ModelForm):
    location_lat = RoundingDecimalField(
        max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )
    location_long = RoundingDecimalField(
        max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )

    class Meta:
        model = FacebookPage
        fields = ('name', 'active', 'location_long', 'location_lat', 'location', 'facebook_id', 'notes', 'events')
        widgets = {
            'events': SelectizeSelectMultiple(),
            'facebook_id': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
