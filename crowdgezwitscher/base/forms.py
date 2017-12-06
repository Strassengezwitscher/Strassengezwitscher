from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class BootstrapPasswordChangeForm(PasswordChangeForm):
     def __init__(self, *args, **kwargs):
        super(BootstrapPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.success = False
