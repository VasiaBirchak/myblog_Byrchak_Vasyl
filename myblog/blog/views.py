from django.shortcuts import render


def blog_index(request):
    return render(request, 'blog/index.html')
