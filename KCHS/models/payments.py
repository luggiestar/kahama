from django.db import models
from django.conf import settings

from .student_registration import *
from .bank_account import *
from ..models import *

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    due = models.DecimalField("remain amount",max_digits=14, decimal_places=2, default=0.00, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)

    class Meta:
        verbose_name = "Registration Payment"
        verbose_name_plural = "Registration Payment"

    def __str__(self):
        return "{0} -{1}".format(self.registration, self.amount)
