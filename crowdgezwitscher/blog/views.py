from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from blog.forms import BlogForm
from blog.models import BlogEntry


class BlogListView(PermissionRequiredMixin, ListView):
    permission_required = 'blog.view_blogentry'
    model = BlogEntry
    template_name = 'blog/list.html'
    context_object_name = 'blogentries'
    ordering = '-created_on'


class BlogDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'blog.view_blogentry'
    model = BlogEntry
    template_name = 'blog/detail.html'
    context_object_name = 'blogentry'


class BlogCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_blogentry'
    model = BlogEntry
    template_name = 'blog/form.html'
    form_class = BlogForm

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.created_by = User.objects.get(pk=self.request.user.id)
        blog.save()
        return super(BlogCreate, self).form_valid(form)


class BlogUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.change_blogentry'
    model = BlogEntry
    template_name = 'blog/form.html'
    form_class = BlogForm


class BlogDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_blogentry'
    model = BlogEntry
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('blog:list')
    context_object_name = 'blogentry'
