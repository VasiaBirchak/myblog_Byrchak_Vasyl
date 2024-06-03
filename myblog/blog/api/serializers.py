from rest_framework import serializers
from blog.models import BlogPost


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'author')
