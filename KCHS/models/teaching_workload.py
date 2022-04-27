from django.db import models
from django.conf import settings
from .program_couser_structure import *
User = settings.AUTH_USER_MODEL


class Workload(models.Model):
    course = models.ForeignKey(ProgrammeCourseStructure, on_delete=models.CASCADE, null=False)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together =('course','tutor')
        verbose_name = "Teaching Workload"
        verbose_name_plural = "Teaching Workload"

    def __str__(self):
        return "{0}-{1}".format(self.course, self.tutor)
