from django.conf import settings
from django.db import models
from .student import *
from .intake import *
from .education_level import *
from .status import *
from .academic_semester import *
from ..models import *
from ..models import *

User = settings.AUTH_USER_MODEL


class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    intake = models.ForeignKey(Intake, on_delete=models.CASCADE, null=True,blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    is_registered = models.BooleanField("Registration Status", default=False)
    is_active = models.BooleanField(default=False)
    semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    registerer = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)

    class Meta:
        unique_together=('student','semester','level')
        verbose_name = "Registration"
        verbose_name_plural = "Registration"

    def __str__(self):
        return "{0} -{1}".format(self.student, self.status)
