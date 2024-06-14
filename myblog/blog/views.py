from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from blog.models import BlogPost, Comment
from blog.api.serializers import PostSerializer, CommentGETPatchSerializer
from rest_framework.viewsets import ModelViewSet
from blog.api.serializers import CommentPostSerializer


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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return CommentPostSerializer
        return CommentGETPatchSerializer
