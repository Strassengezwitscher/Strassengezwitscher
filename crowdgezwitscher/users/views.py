from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User

from crowdgezwitscher.widgets import SelectizeSelectMultiple
from .mixins import NoStaffMixin


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'groups')
        widgets = {
            'groups': SelectizeSelectMultiple()
        }


class UserListView(PermissionRequiredMixin, NoStaffMixin, ListView):
    permission_required = 'auth.view_user'
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return super(UserListView, self).get_queryset().exclude(is_active=False)


class InactiveUserListView(PermissionRequiredMixin, NoStaffMixin, ListView):
    permission_required = 'auth.view_user'
    model = User
    template_name = 'users/list_inactive.html'
    context_object_name = 'users'

    def get_queryset(self):
        return super(InactiveUserListView, self).get_queryset().exclude(is_active=True)


class UserDetail(PermissionRequiredMixin, NoStaffMixin, DetailView):
    permission_required = 'auth.view_user'
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'user_data'


class UserCreate(PermissionRequiredMixin, NoStaffMixin, CreateView):
    permission_required = 'auth.add_user'
    model = User
    template_name = 'users/form.html'
    form_class = UserForm

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(UserCreate, self).form_valid(form)


class UserUpdate(PermissionRequiredMixin, NoStaffMixin, UpdateView):
    permission_required = 'auth.change_user'
    model = User
    template_name = 'users/form.html'
    context_object_name = 'user_data'
    form_class = UserForm

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(UserUpdate, self).form_valid(form)
