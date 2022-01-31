from django.db import models
from django.conf import settings

from .semester import *
from .education_level import *
from .fee_item import *
from .programme import *
from .bank_account import *
# from ..models import *

User = settings.AUTH_USER_MODEL


class PaymentStructure(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    minimum = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    class Meta:
        unique_together=('semester','level','programme','account')
        verbose_name = "Programme Payment Structure"
        verbose_name_plural = "Programme Payment Structure"

    def __str__(self):
        return "{0} -{1}".format(self.programme, self.amount)
