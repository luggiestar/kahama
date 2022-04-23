from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class AssessmentItem(models.Model):
    name = models.CharField(max_length=80, unique=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Assessment Item"
        verbose_name_plural = "Assessment Item"

    def __str__(self):
        return "{0}".format(self.name)
