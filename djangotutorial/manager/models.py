from django.db import models
from django.conf import settings

class Application(models.Model):
    name = models.CharField(max_length=200, unique=True)
    namespace = models.SlugField(max_length=200, unique=True)
    icon = models.CharField(max_length=200)
    comment = models.CharField(max_length=600, default="", blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="UserApplication",
        related_name="applications",
        blank=True,
    )

    def __str__(self):
        return self.name


class UserApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "application"], name="unique_user_application"),
        ]

    def __str__(self):
        return f"{self.user} – {self.application} ({'actif' if self.status else 'inactif'})"


