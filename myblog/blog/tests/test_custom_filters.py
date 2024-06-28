# tests/test_custom_filters.py
import pytest
from django.contrib.auth.models import User
from blog.models import BlogPost, Comment
from rest_framework.test import APIClient
from freezegun import freeze_time
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='12345')


@pytest.fixture
def authenticate_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def blog_posts(user):
    with freeze_time("2022-01-10"):
        post1 = BlogPost.objects.create(title='Post 1', body='Content 1', author=user)
    with freeze_time("2022-02-15"):
        post2 = BlogPost.objects.create(title='Post 2', body='Content 2', author=user)
    return post1, post2


@pytest.fixture
def comments(user, blog_posts):
    post = blog_posts[0]
    with freeze_time("2022-01-10"):
        comment1 = Comment.objects.create(body='Comment 1', blogpost=post, user=user)
    with freeze_time("2022-02-15"):
        comment2 = Comment.objects.create(body='Comment 2', blogpost=post, user=user)
    return comment1, comment2


@pytest.mark.django_db
def test_filter_created_after(authenticate_client, blog_posts):
    url = reverse('post-list')
    response = authenticate_client.get(url, {'created_after': '2022-01-15'})
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Post 2'


@pytest.mark.django_db
def test_filter_created_before(authenticate_client, blog_posts):
    url = reverse('post-list')
    response = authenticate_client.get(url, {'created_before': '2022-01-31'})
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Post 1'


@pytest.mark.django_db
def test_filter_created_between(authenticate_client, blog_posts):
    url = reverse('post-list')
    response = authenticate_client.get(url, {'created_after': '2022-01-01',
                                             'created_before': '2022-01-31'})
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Post 1'


@pytest.mark.django_db
def test_comment_filter_created_after(authenticate_client, comments):
    url = reverse('comment-list')
    response = authenticate_client.get(url, {'created_after': '2022-01-15'})
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['body'] == 'Comment 2'


@pytest.mark.django_db
def test_comment_filter_created_before(authenticate_client, comments):
    url = reverse('comment-list')
    response = authenticate_client.get(url, {'created_before': '2022-01-31'})
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['body'] == 'Comment 1'


@pytest.mark.django_db
def test_comment_filter_created_between(authenticate_client, comments):
    url = reverse('comment-list')
    response = authenticate_client.get(url, {'created_after': '2022-01-01',
                                             'created_before': '2022-01-31'})
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['body'] == 'Comment 1'
