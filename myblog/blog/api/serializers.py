from rest_framework import serializers
from blog.models import BlogPost


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'author')
