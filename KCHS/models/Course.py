from .region import *


class Course(models.Model):
    code = models.CharField(max_length=15, unique=True)

    name = models.CharField(max_length=90)

    class Meta:
        # unique_together = ('name', 'type')
        verbose_name = "Course"
        verbose_name_plural = "Course"

    def __str__(self):
        return "{0}".format(self.code)
