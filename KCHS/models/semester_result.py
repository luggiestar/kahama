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


class SemesterResult(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    programme_course = models.ForeignKey(ProgrammeCourseStructure, on_delete=models.CASCADE)
    ca = models.DecimalField("C A", max_digits=5, decimal_places=2, default=0.00)
    es = models.DecimalField("E S",max_digits=5, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    grade = models.CharField(max_length=1, blank=True, null=True)
    remark = models.CharField(max_length=90, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.es:

            self.total = decimal.Decimal(self.ca) + decimal.Decimal(self.es)
            if self.total:
                if 101.0 >= self.total >= 75.0:
                    self.grade = "A"
                    self.remark = "PASS"
                    # self.point = 1

                elif 74.9 >= self.total >= 65.0:
                    self.grade = "B"
                    self.remark = "PASS"
                    # self.point = 2
                elif 64.9 >= self.total >= 45.0:
                    self.grade = "C"
                    self.remark = "PASS"
                    # self.point = 3
                elif 44.9 >= self.total >= 30.0:
                    self.grade = "D"
                    self.remark = "SUPPLEMENTARY"
                    # self.point = 4
                elif 29.9 >= self.total >= 0:
                    self.grade = "F"
                    self.remark = "SUPPLEMENTARY"
                    # self.point = 5

        return super(SemesterResult, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('academic_semester', 'programme_course', 'registration')
        verbose_name = "Academic Semester Result"
        verbose_name_plural = "Academic Semester Result"

    def __str__(self):
        return "{0} -{1}".format(self.registration, self.total)
