from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Level(models.Model):
    LEVELS = (
        ('NTA-4', 'NTA-LEVEL 4'),
        ('NTA-5', 'NTA-LEVEL 5'),
        ('NTA-6', 'NTA-LEVEL 6'),
    )
    name = models.CharField(choices=LEVELS, max_length=45, null=False, blank=False, unique=True)
    year = models.CharField(max_length=45, null=False, blank=False, unique=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False,null=True)

    def save(self, *args, **kwargs):
        if self.name == "NTA-4":
            self.year = "FIRST YEAR"

        elif self.name == "NTA-5":
            self.year = "SECOND YEAR"
        elif self.name == "NTA-6":
            self.year = "THIRD YEAR"

        return super(Level, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Level"
        verbose_name_plural = "Levels"

    def __str__(self):
        return self.name
