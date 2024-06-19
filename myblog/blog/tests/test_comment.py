import pytest
from django.contrib.auth.models import User
from blog.models import BlogPost, Comment
from django.core.exceptions import ValidationError


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='testuser', password='1234')
    return user


@pytest.fixture
def create_post(create_user):
    post = BlogPost.objects.create(title='Test Post', body='Test Body', author=create_user)
    return post


@pytest.mark.django_db
class TestCommentModel:
    @pytest.fixture(autouse=True)
    def set_up(self, create_user, create_post):
        self.user = create_user
        self.post = create_post

    def test_comment_body_length(self):
        comment = Comment(body='x' * 255, blogpost=self.post, user=self.user)
        try:
            comment.full_clean()
        except ValidationError as e:
            pytest.fail(f"ValidationError: {e}")
        comment.body = 'x' * 256
        with pytest.raises(ValidationError):
            comment.full_clean()

    def test_comment_blogpost_mandatory(self):
        comment = Comment(body='x' * 255, blogpost=None, user=self.user)
        with pytest.raises(ValidationError):
            comment.full_clean()

    def test_comments_count(self):
        Comment.objects.create(blogpost=self.post, body='Comment 1', user=self.user)
        Comment.objects.create(blogpost=self.post, body='Comment 2', user=self.user)
        assert self.post.comments_count == 2
