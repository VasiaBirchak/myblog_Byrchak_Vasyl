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
        author=user,
        safe=True
    ) for x in range(1, 5)]


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestPostFilters:
    def test_filter_by_safe(self, client, posts):
        url = reverse('post-list') + '?safe=True'
        response = client.get(url)
        assert response.status_code == 200
        safe_posts_count = BlogPost.objects.filter(safe=True).count()
        assert len(response.data) == safe_posts_count

    def test_filter_by_author(self, client, posts, user):
        url = reverse('post-list') + f'?author__username={user.username}'
        response = client.get(url)
        assert response.status_code == 200
        author_posts_count = BlogPost.objects.filter(author=user).count()
        assert len(response.data) == author_posts_count

    def test_ordering_by_author(self, client, posts):
        url = reverse('post-list') + '?ordering=author'
        response = client.get(url)
        assert response.status_code == 200
        assert "results" in response.data
        authors = [post['author'] for post in response.data["results"]]
        assert authors == sorted(authors)

    def test_search_by_title(self, client, posts):
        search_title = posts[0].title.split()[1]
        url = reverse('post-list') + f'?search={search_title}'
        response = client.get(url)
        assert response.status_code == 200
        search_results = BlogPost.objects.filter(title__icontains=search_title).count()
        assert response.data['count'] == search_results

    def test_search_by_body(self, client, posts):
        search_body = posts[1].body.split()[2]
        url = reverse('post-list') + f'?search={search_body}'
        response = client.get(url)
        assert response.status_code == 200
        search_results = BlogPost.objects.filter(body__icontains=search_body).count()
        assert len(response.data) == search_results

    def test_search_by_author_username(self, client, posts):
        search_username = posts[2].author.username
        url = reverse('post-list') + f'?search={search_username}'
        response = client.get(url)
        assert response.status_code == 200
        search_results = BlogPost.objects.filter(
            author__username__icontains=search_username).count()
        assert len(response.data) == search_results
