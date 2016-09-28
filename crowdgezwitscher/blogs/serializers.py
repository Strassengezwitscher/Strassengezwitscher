from rest_framework import serializers

from blogs.models import BlogEntry


class BlogSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%d.%m.%Y')
    created_by = serializers.ReadOnlyField(source='created_by.get_full_name')

    class Meta:
        model = BlogEntry
        fields = ['title', 'content', 'created_on', 'created_by']
