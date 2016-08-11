from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=50)
    email = forms.EmailField(required=False)
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    journalist = forms.BooleanField(required=False)
    confidential = forms.BooleanField(required=False)
    files = forms.FileField(required=False, max_length=50, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    @classmethod
    def files_are_valid(cls, request):
        """Takes a request and returns True if the uploaded files are valid. Otherwise returns found errors."""
        uploaded_files = request.FILES.getlist('files')
        if len(uploaded_files) >= 2:
            # Django's validation does only work for a single file. When uploading multiple files only the last one gets
            # checked for validity. We could subclass FileField to suit our needs. Somebody did that already:
            # https://github.com/Chive/django-multiupload
            # However, the pain of the following workaround is not strong enough to add another dependency.
            # As we have multiple files we create a new form with the same data but only a single file for each file
            # and check the new form's validity.
            # Another alternative would be not relying on Django's automatic FileField validation at all and just do
            # that tiny bit of validation ourselves for all files in request.FILES.
            for uploaded_file in uploaded_files:
                request.FILES['files'] = uploaded_file
                temp_form = cls(request.POST, request.FILES)
                if not temp_form.is_valid():
                    return temp_form.errors
        return True
