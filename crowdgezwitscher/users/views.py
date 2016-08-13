from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'users.view_user'
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.exclude(is_staff=True)


class UserDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'users.view_user'
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'user_data'


class UserCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'users.add_user'
    model = User
    template_name = 'users/form.html'
    fields = ['username', 'email', 'password', 'groups']

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(UserCreate, self).form_valid(form)


class UserUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'users.change_user'
    model = User
    template_name = 'users/form.html'
    context_object_name = 'user_data'
    fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'groups']

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(UserUpdate, self).form_valid(form)
