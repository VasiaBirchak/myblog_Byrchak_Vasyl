from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length = 100,)
    body = models.TextField(validators = [MaxLengthValidator(255)])
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.title #return the title of the post as a display of the model
    
    def clean(self):
        if not self.title:
            raise ValidationError("Title can't be empty")
        if not self.body:
            raise ValidationError("Body can't be empty") #Implement the following validations: title and body cannot be empty (But they cannot be empty anyway)
        
    class Meta:
        verbose_name = 'Post'  
        verbose_name_plural = 'Posts'  