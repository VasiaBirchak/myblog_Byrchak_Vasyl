import pytest
from django.forms import ValidationError
from django.contrib.auth.models import User
from blog.models import BlogPost


@pytest.mark.django_db
class TestPostModel:
    @pytest.fixture()
    def user(self, db):
        return User.objects.create_user(username="testuser", password="1234")


    def test_title_cannot_be_empty(self, user):
        post = BlogPost(title='', body='body', author=user)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_body_cannot_be_empty(self, user):
        post = BlogPost(title='title', body='', author=user)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_title_max_length(self, user):
        post = BlogPost(title='a' * 101, body='body', author=user)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_body_max_length(self, user):
        post = BlogPost(title='title', body='X' * 256, author=user)
        with pytest.raises(ValidationError):
            post.full_clean()

