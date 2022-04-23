from django.db import models
from django.conf import settings

from .semester import *
from .education_level import *
from .group import *
from .programme import *
from .Course import *

# from ..models import *

User = settings.AUTH_USER_MODEL


class ProgrammeCourseStructure(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    credit=models.IntegerField(default=0, null=True)

    class Meta:
        unique_together = ('semester', 'level', 'programme', 'group', 'course')
        verbose_name = "Programme Course Structure"
        verbose_name_plural = "Programme Course Structure"

    def __str__(self):
        return "{0} -{1}".format(self.programme, self.course)
