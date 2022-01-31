from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Semester(models.Model):
    NUMBERS = (
        ('SEMESTER ONE', 'SEMESTER ONE'),
        ('SEMESTER TWO', 'SEMESTER TWO'),
        ('SEMESTER THREE', 'SEMESTER THREE'),
    )
    name = models.CharField(choices=NUMBERS, max_length=45, null=False, blank=False, unique=True)
    number = models.CharField(max_length=45, null=False, blank=False, unique=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)

    def save(self, *args, **kwargs):
        if self.name == "SEMESTER ONE":
            self.number = "1"

        elif self.name == "SEMESTER TWO":
            self.number = "2"
        elif self.name == "SEMESTER THREE":
            self.number = "3"

        return super(Semester, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semester"

    def __str__(self):
        return self.name
