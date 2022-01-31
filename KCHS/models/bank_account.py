from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class BankAccount(models.Model):
    BANKS = {
        ('CRDB', 'CRDB'),
        ('NMB', 'NMB'),
        ('BOA', 'BOA'),
    }
    bank = models.CharField(choices=BANKS, max_length=45, null=False, blank=False, unique=True)
    name = models.CharField(max_length=45, null=False, blank=False)
    number = models.CharField(max_length=45, )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Account"

    def __str__(self):
        return "{0}-{1}".format(self.bank, self.number)
