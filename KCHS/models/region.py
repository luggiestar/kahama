from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Region(models.Model):
    name = models.CharField(max_length=40, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, editable=False)

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "region"

    def __str__(self):
        return "{0}".format(self.name)
