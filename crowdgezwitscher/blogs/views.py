from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from rest_framework import generics

from blogs.models import BlogEntry
from blogs.serializers import BlogSerializer


class BlogForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = BlogEntry
        exclude = ['created_on', 'created_by']


class BlogListView(PermissionRequiredMixin, ListView):
    permission_required = 'blogs.view_blogentry'
    model = BlogEntry
    template_name = 'blogs/list.html'
    context_object_name = 'blogs'


class BlogDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'blogs.view_blogentry'
    model = BlogEntry
    template_name = 'blogs/detail.html'
    context_object_name = 'blog'


class BlogCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'blogs.add_blogentry'
    model = BlogEntry
    template_name = 'blogs/form.html'
    form_class = BlogForm

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.created_by = User.objects.get(pk=self.request.user.id)
        blog.save()
        return super(BlogCreate, self).form_valid(form)


class BlogUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'blogs.change_blogentry'
    model = BlogEntry
    template_name = 'blogs/form.html'
    form_class = BlogForm


class BlogDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'blogs.delete_blogentry'
    model = BlogEntry
    template_name = 'blogs/delete.html'
    success_url = reverse_lazy('blogs:list')
    context_object_name = 'blog'


# API Views
class BlogAPIList(generics.ListAPIView):
    queryset = BlogEntry.objects.filter(status=BlogEntry.PUBLISHED)
    serializer_class = BlogSerializer


class BlogAPIDetail(generics.RetrieveAPIView):
    queryset = BlogEntry.objects.filter(status=BlogEntry.PUBLISHED)
    serializer_class = BlogSerializer
