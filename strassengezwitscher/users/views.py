from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.contrib.auth.models import User


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.exclude(is_staff=True)


class UserDetail(DetailView):
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'user'


class UserCreate(CreateView):
    model = User
    template_name = 'users/form.html'
    fields = ['username', 'email', 'password', 'groups']

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(UserCreate, self).form_valid(form)


class UserUpdate(UpdateView):
    model = User
    template_name = 'users/form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'groups']

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(UserUpdate, self).form_valid(form)
