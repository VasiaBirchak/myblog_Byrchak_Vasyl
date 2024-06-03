from django.urls import reverse
import pytest
from rest_framework.test import APITestCase
from .models import BlogPost
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPostEndpoint(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234')
        BlogPost.objects.create(title='Post 1', body='Body of post 1', author=self.user)
        BlogPost.objects.create(title='Post 2', body='Body of post 2', author=self.user)
        BlogPost.objects.create(title='Post 3', body='Body of post 3', author=self.user)

    def test_get_all_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        posts_count = len(response.data)
        database_posts_count = BlogPost.objects.count()
        self.assertEqual(posts_count, database_posts_count)
