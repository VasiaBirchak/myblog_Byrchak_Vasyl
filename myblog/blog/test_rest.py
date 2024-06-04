from django.urls import reverse
import pytest
from rest_framework.test import APITestCase
from .models import BlogPost
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPostEndpoint(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.posts = [BlogPost.objects.create(
            title='Post ' + str(x),
            body='Body of post ' + str(x),
            author=self.user
        ) for x in range(1, 4)]

    def test_get_all_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        posts_count = len(response.data)
        database_posts_count = BlogPost.objects.count()
        self.assertEqual(posts_count, database_posts_count)
