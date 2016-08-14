from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User

from .mixins import NoStaffMixin


class UserListView(PermissionRequiredMixin, NoStaffMixin, ListView):
    permission_required = 'auth.view_user'
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserDetail(PermissionRequiredMixin, NoStaffMixin, DetailView):
    permission_required = 'auth.view_user'
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'user_data'


class UserCreate(PermissionRequiredMixin, NoStaffMixin, CreateView):
    permission_required = 'auth.add_user'
    model = User
    template_name = 'users/form.html'
    fields = ['username', 'email', 'password', 'groups']

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(UserCreate, self).form_valid(form)


class UserUpdate(PermissionRequiredMixin, NoStaffMixin, UpdateView):
    permission_required = 'auth.change_user'
    model = User
    template_name = 'users/form.html'
    context_object_name = 'user_data'
    fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'groups']

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(UserUpdate, self).form_valid(form)
