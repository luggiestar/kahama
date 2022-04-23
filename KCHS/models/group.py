from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CourseGroup(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Course Group"
        verbose_name_plural = "Course Group"

    def __str__(self):
        return "{0}".format(self.name)
