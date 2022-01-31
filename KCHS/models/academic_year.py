from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class AcademicYear(models.Model):
    financial_year = models.CharField(max_length=20, null=False, blank=False, unique=True)
    year = models.IntegerField(null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        unique_together = ('financial_year', 'year',)
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"

    def __str__(self):
        return self.financial_year
