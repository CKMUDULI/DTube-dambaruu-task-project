from django.db import models


class PublishedVideoPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publish_status=True)
