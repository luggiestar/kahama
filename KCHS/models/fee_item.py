from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class FeeItem(models.Model):
    name = models.CharField(max_length=80, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,editable=False)

    class Meta:
        verbose_name = "Fee Item"
        verbose_name_plural = "Fee Item"

    def __str__(self):
        return "{0}".format(self.name)
