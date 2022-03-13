from django.db import models
from django.conf import settings

from .student_registration import *
from .bank_account import *
from ..models import *

User = settings.AUTH_USER_MODEL


class PaymentSummary(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    due = models.DecimalField("remain amount",max_digits=14, decimal_places=2, default=0.00,)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Payment Summary"
        verbose_name_plural = "Payment Summary"

    def __str__(self):
        return "{0} -{1}".format(self.registration, self.amount)
