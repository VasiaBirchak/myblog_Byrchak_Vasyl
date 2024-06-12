from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(validators=[MaxLengthValidator(255)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='uploads/images/%Y/%m/%d/', blank=True, null=True)  # Поле для зображення
    safe = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    body = models.TextField(validators=[MaxLengthValidator(255)])
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
