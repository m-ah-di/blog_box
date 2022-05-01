from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


# Create your models here.


class Article(models.Model):
    """Title and article for blog post"""
    DoesNotExist = None
    objects = None
    thumbnail_url = models.URLField(blank=True, null=True,
                                    verbose_name="Featured Image URL")
    title = models.CharField(max_length=200)
    text = RichTextField()
    article_tags = TaggableManager(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=20, default='public')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # noinspection PyTypeChecker
        if len(self.title) >= 50:
            return f"{self.title[:50]}..."
        else:
            return f"{self.title}"
