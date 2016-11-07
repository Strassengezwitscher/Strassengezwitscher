from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
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


class TwitterAccountDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'twitter.delete_twitteraccount'
    model = TwitterAccount
    template_name = 'twitter/delete.html'
    success_url = reverse_lazy('twitter:list')
    context_object_name = 'account'


@require_POST
def fetch_initial_tweets(request, pk):
    twitter_account = get_object_or_404(TwitterAccount, pk=pk)
    twitter_account.fetch_initial_tweets()

    return HttpResponse()
