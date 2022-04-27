from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Status(models.Model):
    STATUS = {
        ('FULL PAID', 'COMPLETE'),
        ('PARTIAL PAID', 'PARTIAL PAID'),
        ('NOT PAID', 'NOT PAID'),
        ('PASS', 'PASS'),
        ('SUPPLEMENTARY', 'SUPPLEMENTARY'),
    }

    code = models.CharField(choices=STATUS, max_length=30, unique=True, default="NOT PAID")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"

    def __str__(self):
        return "{0}".format(self.code)
