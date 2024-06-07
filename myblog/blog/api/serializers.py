from rest_framework import serializers
from blog.models import BlogPost, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'author')


class PostSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'id')


class CommentGETPatchSerializer(serializers.ModelSerializer):
    blogpost = PostSummarySerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
