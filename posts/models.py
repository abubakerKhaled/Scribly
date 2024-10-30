from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import Author
from taggit.managers import TaggableManager
import uuid


class PublishedManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status=Post.Status.PUBLISHED)
        return queryset


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, unique_for_date='publish')
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    body = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    tags = TaggableManager()

    objects = models.Manager() # the default manager.
    published = PublishedManager() # our custom manager.

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self) -> str:
        return self.title[:50] + ("..." if len(self.title) > 50 else "")
    
    def get_absolute_url(self):
        return reverse("posts:post_detail", args=[self.uuid])
    

class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'