import random
import string

from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings

from ..models import *

User = settings.AUTH_USER_MODEL


def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Student(models.Model):
    phone_regex = RegexValidator(regex=r'[0][6-9][0-9]{8}', message="Phone number must be entered in the format: "
                                                                    "'0.....'. Up to 10 digits allowed.")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    dob = models.DateField("Date of Birth", blank=True, null=True)  # validators should be a list
    parent_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    residency = models.ForeignKey('District', on_delete=models.CASCADE, null=True, blank=True)
    programme = models.ForeignKey('Programme', on_delete=models.CASCADE, null=False)
    entry_level = models.ForeignKey('Level', on_delete=models.CASCADE, null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Student Entry"
        verbose_name_plural = "Student Entry"

    def __str__(self):
        return "{0}-{1}".format(self.user,self.programme)
