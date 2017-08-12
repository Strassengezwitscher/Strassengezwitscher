# -*- coding: utf-8 -*-
from django import forms

from twitter.models import TwitterAccount


class TwitterAccountForm(forms.ModelForm):

    class Meta:
        model = TwitterAccount
        fields = (
            'name',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
