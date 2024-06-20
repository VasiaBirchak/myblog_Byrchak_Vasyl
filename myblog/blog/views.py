from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from blog.models import BlogPost, Comment, Like
from blog.api.serializers import (
    PostSerializer,
    CommentGETPatchSerializer,
    PostCreateSerializer,
    PostSummarySerializer
)
from rest_framework.viewsets import ModelViewSet
from blog.api.serializers import CommentPostSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType


def user_login(request):
    login_form = AuthenticationForm()
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog_index')
    return render(request, 'blog/login.html', {'login_form': login_form})


def user_reg(request):
    register_form = SignUpForm()
    if request.method == 'POST':
        register_form = SignUpForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('blog_index')
    return render(request, 'blog/register.html', {'register_form': register_form})


def user_logout(request):
    logout(request)
    return redirect('blog_index')


def blog_index(request):
    return render(request, 'blog/index.html')


class PostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['author__username', 'safe']
    ordering_fields = ['author', 'safe']
    search_fields = ['title', 'body', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'my_tags':
            return PostSummarySerializer
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'my_tags':
            return queryset.filter(tagged_users__user=self.request.user)
        return queryset

    def my_tags(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(post)
        like, created = Like.objects.get_or_create(user=user,
                                                   content_type=content_type,
                                                   object_id=post.id)
        if created:
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(post)
        Like.objects.filter(user=user, content_type=content_type, object_id=post.id).delete()
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return CommentPostSerializer
        return CommentGETPatchSerializer

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(post)
        like, created = Like.objects.get_or_create(user=user,
                                                   content_type=content_type,
                                                   object_id=post.id)
        if created:
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(post)
        Like.objects.filter(user=user, content_type=content_type, object_id=post.id).delete()
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
