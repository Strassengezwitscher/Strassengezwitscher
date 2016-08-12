from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from gnupg import GPG

from contact.models import Key
from contact.utils import TemporaryDirectory


class KeyAdminForm(forms.ModelForm):

    class Meta:
        model = Key
        fields = ['key']

    def clean_key(self):
        """
        Raises ValidationError if the entered key is invalid or includes a GPG private key.
        """
        data = self.cleaned_data['key']
        with TemporaryDirectory() as temp_dir:
            gpg_keychain = GPG(gnupghome=temp_dir)
            res = gpg_keychain.import_keys(data)
            if not res:
                errors = [forms.ValidationError(_("Invalid key."), code='invalid')]
                for attr in ['status', 'stderr']:  # not all fields are always present
                    if hasattr(res, attr):
                        errors.append(forms.ValidationError("%(name)s: %(value)s",
                                                            params={'name': attr, 'value': getattr(res, attr)},
                                                            code=attr))
                raise forms.ValidationError(errors)

            if len(gpg_keychain.list_keys(True)) > 0:  # check existance of private keys
                raise forms.ValidationError(_("Import public keys only, no private keys! "
                                              "You should consider the private key(s) compromised."),
                                            code='private_key')
        return data


class KeyAdmin(admin.ModelAdmin):
    form = KeyAdminForm

admin.site.register(Key, KeyAdmin)
