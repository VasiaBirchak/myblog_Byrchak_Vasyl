from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user',
                                            'content_type',
                                            'object_id'], name='unique_like')
        ]


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(validators=[MaxLengthValidator(255)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to='uploads/images/%Y/%m/%d/', blank=True, null=True)
    safe = models.BooleanField(default=True)
    likes = GenericRelation(Like)

    @property
    def tagged_count(self):
        return self.tagged_users.count()

    @property
    def last_tag_date(self):
        last_tag = self.usertag_set.order_by('-created_at').first()
        return last_tag.created_at.isoformat() if last_tag else None

    @property
    def comments_count(self):
        return self.comments.all().count()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    body = models.TextField(validators=[MaxLengthValidator(255)])
    blogpost = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)


class UserTag(models.Model):
    post = models.ForeignKey(BlogPost, related_name='tagged_users', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
