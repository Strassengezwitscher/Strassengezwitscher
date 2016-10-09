from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from twitter.models import TwitterAccount


# class TwitterAccountForm(ModelForm):
#     # class Meta:
#     model = TwitterAccount
#     permission_required = 'twitter..add_user'
#     template_name = 'users/form.html'
#     fields = ['username', 'email', 'password', 'groups']
#         # fields = ('name', 'active', 'location_long', 'location_lat', 'location', 'notes', 'events')


class TwitterAccountListView(PermissionRequiredMixin, ListView):
    permission_required = 'twitter.view_twitteraccount'
    model = TwitterAccount
    template_name = 'twitter/list.html'
    context_object_name = 'accounts'


class TwitterAccountDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'twitter.view_twitteraccount'
    model = TwitterAccount
    template_name = 'twitter/detail.html'
    context_object_name = 'account'


class TwitterAccountCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'twitter.add_twitteraccount'
    model = TwitterAccount
    template_name = 'twitter/form.html'
    fields = ['name']
    # form_class = TwitterAccountForm


class TwitterAccountUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'twitter.change_twitteraccount'
    model = TwitterAccount
    template_name = 'twitter/form.html'
    fields = ['name']
    # form_class = TwitterAccountForm


class TwitterAccountDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'twitter.delete_twitteraccount'
    model = TwitterAccount
    template_name = 'twitter/delete.html'
    success_url = reverse_lazy('twitter:list')
    context_object_name = 'account'