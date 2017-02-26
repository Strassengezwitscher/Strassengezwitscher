from rest_framework import generics
from rest_framework.decorators import authentication_classes, api_view, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from crowdgezwitscher.auth import CsrfExemptSessionAuthentication

from base.fields import RoundingDecimalField
from base.models import MapObjectFilterBackend
from base.widgets import SelectizeSelectMultiple
from facebook.models import FacebookPage
from facebook.serializers import FacebookPageSerializer, FacebookPageSerializerShortened, FacebookPageSerializerCreate


class FacebookPageForm(forms.ModelForm):
    location_lat = RoundingDecimalField(
        max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )
    location_long = RoundingDecimalField(
        max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
    )

    class Meta:
        model = FacebookPage
        fields = ('name', 'active', 'location_long', 'location_lat', 'location', 'notes', 'events')
        widgets = {
            'events': SelectizeSelectMultiple(),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


class FacebookPageListView(PermissionRequiredMixin, ListView):
    permission_required = 'facebook.view_facebookpage'
    model = FacebookPage
    template_name = 'facebook/list.html'
    context_object_name = 'pages'


class FacebookPageDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'facebook.view_facebookpage'
    model = FacebookPage
    template_name = 'facebook/detail.html'
    context_object_name = 'page'


class FacebookPageCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'facebook.add_facebookpage'
    model = FacebookPage
    template_name = 'facebook/form.html'
    form_class = FacebookPageForm


class FacebookPageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'facebook.change_facebookpage'
    model = FacebookPage
    template_name = 'facebook/form.html'
    form_class = FacebookPageForm


class FacebookPageDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'facebook.delete_facebookpage'
    model = FacebookPage
    template_name = 'facebook/delete.html'
    success_url = reverse_lazy('facebook:list')
    context_object_name = 'page'


# API Views
class FacebookPageAPIList(generics.ListAPIView):
    queryset = FacebookPage.objects.filter(active=True)
    serializer_class = FacebookPageSerializerShortened
    filter_backends = (MapObjectFilterBackend,)


class FacebookPageAPIDetail(generics.RetrieveAPIView):
    queryset = FacebookPage.objects.filter(active=True)
    serializer_class = FacebookPageSerializer


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@parser_classes((JSONParser,))
def send_form(request):
    print(request.data)
    serializer = FacebookPageSerializerCreate(data=request.data)
    if not serializer.is_valid():
        return Response({'status': 'error', 'message': 'Fehler beim Speichern der Informationen. \n' + '\n'.join([serializer.errors[msg][0] for msg in serializer.errors])},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        serializer.save()
    except Exception as e:
        return Response({'status': 'error', 'message': 'Fehler beim Speichern der Informationen.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})
