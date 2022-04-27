from django.db import models
from django.conf import settings

from .assessment_item import *
from .group import *
from .fee_item import *
from .programme import *

# from .bank_account import *
# from ..models import *

User = settings.AUTH_USER_MODEL


class GroupAssessment(models.Model):
    CATEGORIES = (
        ('CA', 'Continuous Assessment'),
        ('ES', 'End of Semester'),
    )
    item = models.ForeignKey(AssessmentItem, on_delete=models.CASCADE)
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=CATEGORIES, default="CA")
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    passmark = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)

    class Meta:
        unique_together = ('item', 'category', 'group',)
        verbose_name = "course Group Assessment"
        verbose_name_plural = "course Group Assessment"

    def __str__(self):
        return "{0} -{1}-{2}".format(self.item, self.group, self.weight)
