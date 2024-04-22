from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .managers import PublishedVideoPostManager

User = get_user_model()


# Create your models here.
class VideoPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/videos/%Y/%m/%d/')
    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_status = models.BooleanField(default=True)

    objects = models.Manager()
    published = PublishedVideoPostManager()

    class Meta:
        ordering = ('-uploaded',)
        indexes = [models.Index(fields=['-uploaded'])]

    def __str__(self):
        return f'{self.author} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:videos:video_post',
                       kwargs={'year': self.uploaded.year, 'month': self.uploaded.month, 'day': self.uploaded.day,
                               'video_slug': self.slug})
