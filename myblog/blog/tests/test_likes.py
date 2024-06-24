import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import BlogPost, Comment, Like


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='1234')


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def test_post(user):
    return BlogPost.objects.create(title='Test Post', body='Test Body', author=user)


@pytest.fixture
def test_comment(user, test_post):
    return Comment.objects.create(body='Test Comment', blogpost=test_post, user=user)


@pytest.mark.django_db
def test_like_post(client, test_post):
    response = client.post(f'/blog/api/post/{test_post.id}/like/')
    assert response.status_code == status.HTTP_201_CREATED
    assert Like.objects.filter(content_type__model='blogpost', object_id=test_post.id).count() == 1


@pytest.mark.django_db
def test_unlike_post(client, test_post):
    client.post(f'/blog/api/post/{test_post.id}/like/')
    assert Like.objects.filter(content_type__model='blogpost', object_id=test_post.id).exists()
    response = client.post(f'/blog/api/post/{test_post.id}/unlike/')
    assert response.status_code == status.HTTP_200_OK
    assert Like.objects.filter(content_type__model='blogpost', object_id=test_post.id).count() == 0


@pytest.mark.django_db
def test_like_comment(client, test_comment):
    response = client.post(f'/blog/api/comments/{test_comment.id}/like/')
    assert response.status_code == status.HTTP_201_CREATED
    assert Like.objects.filter(content_type__model='comment',
                               object_id=test_comment.id).count() == 1


@pytest.mark.django_db
def test_unlike_comment(client, test_comment):
    client.post(f'/blog/api/comments/{test_comment.id}/like/')
    assert Like.objects.filter(content_type__model='comment', object_id=test_comment.id).exists()
    response = client.post(f'/blog/api/comments/{test_comment.id}/unlike/')
    assert response.status_code == status.HTTP_200_OK
    assert Like.objects.filter(content_type__model='comment',
                               object_id=test_comment.id).count() == 0
