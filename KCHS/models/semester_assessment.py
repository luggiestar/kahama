import decimal

from django.db import models
from django.conf import settings

from .semester import *
from .education_level import *
from .fee_item import *
from .programme import *
from .bank_account import *
from .academic_semester import *
from .program_couser_structure import *
from .course_group_assement import *
from .student_registration import *

User = settings.AUTH_USER_MODEL


class SemesterAssessment(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    programme_course = models.ForeignKey(ProgrammeCourseStructure, on_delete=models.CASCADE)
    assessment_group = models.ForeignKey(GroupAssessment, on_delete=models.CASCADE)
    marks = models.DecimalField("Marks/(100)", max_digits=5, decimal_places=2, default=0.00)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.marks:
            get_group_weight = self.assessment_group.weight
            get_weight = (self.marks / decimal.Decimal(100)) * decimal.Decimal(get_group_weight)
            self.weight = get_weight

        return super(SemesterAssessment, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('academic_semester', 'programme_course', 'assessment_group', 'registration')
        verbose_name = "Academic Semester Assessment"
        verbose_name_plural = "Academic Semester Assessment"

    def __str__(self):
        return "{0} -{1}".format(self.registration, self.weight)
