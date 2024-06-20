from rest_framework import serializers
from blog.models import BlogPost, Comment, UserTag, Like
from django.contrib.auth.models import User


class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = ['user', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'content_type', 'object_id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    last_tag_date = serializers.SerializerMethodField()
    tagged_users = UserTagSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ('title',
                  'body',
                  'author',
                  'img',
                  'created_at',
                  'tagged_users',
                  'tagged_count',
                  'last_tag_date',
                  'likes')

    def get_last_tag_date(self, obj):
        last_tag = UserTag.objects.filter(post=obj).order_by('-created_at').first()
        return last_tag.created_at.isoformat() if last_tag else None


class PostCreateSerializer(serializers.ModelSerializer):
    tagged_users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True)

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'img', 'created_at', 'safe', 'tagged_users')

    def create(self, validated_data):
        tagged_users = validated_data.pop('tagged_users')
        post = BlogPost.objects.create(**validated_data)
        for user in tagged_users:
            UserTag.objects.create(post=post, user=user)
        return post

    def update(self, instance, validated_data):
        tagged_users = validated_data.pop('tagged_users', None)
        instance = super().update(instance, validated_data)
        if tagged_users is not None:
            instance.tagged_users.all().delete()
            for user in tagged_users:
                UserTag.objects.create(post=instance, user=user)
        return instance


class PostSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'id')


class CommentGETPatchSerializer(serializers.ModelSerializer):
    blogpost = PostSummarySerializer()
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'blogpost', 'blogpost_id', 'user_id', 'created_at', 'likes')


class CommentPostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'blogpost', 'blogpost_id', 'user_id', 'created_at', 'likes')
