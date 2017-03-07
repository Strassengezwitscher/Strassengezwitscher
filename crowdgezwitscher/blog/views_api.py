from rest_framework import generics

from blog.models import BlogEntry
from blog.serializers import BlogSerializer


class BlogAPIList(generics.ListAPIView):
    queryset = BlogEntry.objects.filter(status=BlogEntry.PUBLISHED)
    serializer_class = BlogSerializer


class BlogAPIDetail(generics.RetrieveAPIView):
    queryset = BlogEntry.objects.filter(status=BlogEntry.PUBLISHED)
    serializer_class = BlogSerializer
