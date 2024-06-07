from django.urls import path
from . import views
from .views import PostDetailViewSet


urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_reg, name='user_reg'),
    path('logout/', views.user_logout, name='logout'),
    path('api/post/', views.PostsViewSet.as_view(), name='post-list'),
    path('api/post/<int:pk>/', PostDetailViewSet.as_view(), name='post-detail')
]
