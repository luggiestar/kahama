from django.db import models
from django.conf import settings

from .academic_year import *
from .semester import *

User = settings.AUTH_USER_MODEL


class AcademicSemester(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start = models.DateField(auto_now_add=True)
    end = models.DateField("End Date")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        verbose_name = "Academic Semester"
        verbose_name_plural = "Academic Semester"

    def __str__(self):
        return "{0}-{1}".format(self.semester, self.academic_year)
