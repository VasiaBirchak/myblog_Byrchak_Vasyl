from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from blog.models import BlogPost, Comment
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestCommentModel(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.post = BlogPost.objects.create(title='Test Post', body='Test Body', author=self.user)

    def test_comment_body_length(self):
        comment = Comment(body='x' * 255, blogpost=self.post, user=self.user)
        try:
            comment.full_clean()
        except ValidationError as e:
            self.fail(f"ValidationError: {e}")
        comment.body = 'x' * 256
        with self.assertRaises(ValidationError):
            comment.full_clean()

    def test_comment_blogpost_mandatory(self):
        comment = Comment(body='x' * 255, blogpost=None, user=self.user)
        with self.assertRaises(ValidationError):
            comment.full_clean()
