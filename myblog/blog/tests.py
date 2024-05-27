import pytest
from django.forms import ValidationError
from django.contrib.auth.models import User
from blog.models import BlogPost


@pytest.mark.django_db
class TestPostModel:
    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        self.user = User.objects.create_user(username="testuser", password="1234")

    def test_title_cannot_be_empty(self):
        post = BlogPost(title='', body='Some body text', author=self.user)
        with pytest.raises(ValidationError):
            post.full_clean()  # This will run the model's clean methods

    def test_body_cannot_be_empty(self):
        post = BlogPost(title='Some title', body='', author=self.user)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_title_max_length(self):
        post = BlogPost(title='a' * 101, body='Some body text', author=self.user)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_body_max_length(self):
        post = BlogPost(title='Some title for test', body='X' * 256, author=self.user)
        with pytest.raises(ValidationError):
            post.full_clean()
