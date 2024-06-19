from rest_framework import serializers
from blog.models import BlogPost, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tagged_count = serializers.ReadOnlyField()
    last_tag_date = serializers.ReadOnlyField()

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'author', 'img', 'created_at', 'tagged_count', 'last_tag_date')


class PostSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'id')


class CommentGETPatchSerializer(serializers.ModelSerializer):
    blogpost = PostSummarySerializer()

    class Meta:
        model = Comment
        fields = ('id', 'body', 'blogpost', 'blogpost_id', 'user_id', 'created_at')


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'blogpost', 'blogpost_id', 'user_id', 'created_at')
