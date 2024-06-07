from django.urls import include, path
from . import views
from .views import PostViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'api/post', PostViewSet, basename='post')

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_reg, name='user_reg'),
    path('logout/', views.user_logout, name='logout'),
    path('', include(router.urls)),
]
