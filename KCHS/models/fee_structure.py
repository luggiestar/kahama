from django.db import models
from django.conf import settings

from .semester import *
from .education_level import *
from .fee_item import *
from .programme import *
from .bank_account import *
# from ..models import *

User = settings.AUTH_USER_MODEL


class FeeStructure(models.Model):
    fee = models.ForeignKey(FeeItem, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)

    class Meta:
        unique_together=('fee','semester','level','account','programme')
        verbose_name = "Fee Structure"
        verbose_name_plural = "Fee Structure"

    def __str__(self):
        return "{0} -{1}".format(self.fee, self.level)
