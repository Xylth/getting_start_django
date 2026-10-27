from django.db import models


class Checklist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Action(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="actions")
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=600, default="", blank=True)
    status = models.BooleanField(default=False)
    rank = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["checklist", "name"],
                name="unique_action_per_checklist",
            )
        ]

    def __str__(self):
        return self.name
