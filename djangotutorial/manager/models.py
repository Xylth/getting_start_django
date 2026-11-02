from django.db import models
from django.conf import settings

class Application(models.Model):
    name = models.CharField(max_length=200, unique=True)
    namespace = models.SlugField(max_length=200, unique=True)
    icon = models.CharField(max_length=200)
    comment = models.CharField(max_length=600, default="", blank=True)
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="applications",
        blank=True,
    )

    def __str__(self):
        return self.name



