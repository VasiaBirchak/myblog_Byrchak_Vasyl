from django.urls import reverse
import pytest
from rest_framework.test import APITestCase
from blog.models import BlogPost
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
        self.client.force_authenticate(user=self.user)
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        posts_count = len(response.data)
        database_posts_count = BlogPost.objects.count()
        self.assertEqual(posts_count, database_posts_count)

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Test Post', 'body': 'Test Body'}
        url = reverse('post-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BlogPost.objects.count(), 4)
        self.assertEqual(BlogPost.objects.get(title='Test Post').body, 'Test Body')


@pytest.mark.django_db
class TestPostDetailEndpoint(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.post = BlogPost.objects.create(
            title='Post 1',
            body='Body of post 1',
            author=self.user
        )
        self.url = reverse('post-detail', args=[self.post.id])

    def test_get_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.post.title)

    def test_patch_post(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_delete_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(BlogPost.objects.filter(id=self.post.id).exists())
