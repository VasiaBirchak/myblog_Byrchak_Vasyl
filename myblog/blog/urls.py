from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/post', views.PostViewSet, basename='post')
router.register(r'api/comments', views.CommentViewSet, basename='comment')
urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_reg, name='user_reg'),
    path('logout/', views.user_logout, name='logout'),
    path('', include(router.urls)),
]
