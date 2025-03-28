from ckeditor.widgets import CKEditorWidget
from django import forms

from base.widgets import SelectizeSelect
from blog.models import BlogEntry


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        exclude = (
            'created_by',
            'created_on',
        )
        widgets = {
            'content': CKEditorWidget(),
            'status': SelectizeSelect(),
        }
