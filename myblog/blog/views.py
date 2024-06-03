from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from rest_framework.generics import GenericAPIView
from blog.models import BlogPost
from blog.api.serializers import PostSerializer
from rest_framework.mixins import ListModelMixin


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
            return redirect('blog_index')
    return render(request, 'blog/register.html', {'register_form': register_form})


def user_logout(request):
    logout(request)
    return redirect('blog_index')


def blog_index(request):
    return render(request, 'blog/index.html')


class PostsViewSet(GenericAPIView, ListModelMixin):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
