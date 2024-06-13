from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from blog.models import BlogPost
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='1234')


@pytest.fixture
def posts(user):
    return [BlogPost.objects.create(
        title=f'Post {x}',
        body=f'Body of post {x}',
        author=user
    ) for x in range(1, 4)]


@pytest.fixture
def url():
    def _url(post_id):
        return reverse('post-detail', args=[post_id])
    return _url


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestPostEndpoint:
    def test_get_all_posts(self, client):
        url = reverse('post-list')
        response = client.get(url)
        assert response.status_code == 200
        posts_count = len(response.data)
        database_posts_count = BlogPost.objects.count()
        assert posts_count == database_posts_count

    def test_create_post(self, client, posts):
        data = {'title': 'Test Post', 'body': 'Test Body'}
        url = reverse('post-list')
        response = client.post(url, data)
        assert response.status_code == 201
        assert BlogPost.objects.count() == 4
        assert BlogPost.objects.get(title='Test Post').body == 'Test Body'


@pytest.mark.django_db
class TestPostDetailEndpoint:
    def test_get_post(self, client, posts, url):
        response = client.get(url(posts[0].id))
        assert response.status_code == 200
        assert response.data['title'] == posts[0].title

    def test_patch_post(self, client, posts, url):
        data = {'title': 'Updated Title'}
        response = client.patch(url(posts[0].id), data)
        assert response.status_code == 200
        posts[0].refresh_from_db()
        assert posts[0].title == 'Updated Title'

    def test_delete_post(self, client, posts, url):
        response = client.delete(url(posts[0].id))
        assert response.status_code == 204
        assert not BlogPost.objects.filter(id=posts[0].id).exists()
