from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

# Create your models here.


class Paste(models.Model):

    paste_name = models.CharField(max_length=200)
    type_content_paste = models.CharField(max_length=200)
    content_paste = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=0)
    short_link = models.SlugField(max_length=255, unique=True)
    user_own = models.CharField(max_length=200)
    class Meta:
        ordering = ['-time_create']
    def __str__(self):
        return self.paste_name

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = get_random_string(length=10)
        super().save()