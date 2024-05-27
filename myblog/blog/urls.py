from django.urls import path
# from . import views
from .views import blog_index

urlpatterns = [
    path('', blog_index, name='blog_index'),
]
