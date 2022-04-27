
from .region import *


class District(models.Model):

    name = models.CharField(max_length=40, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "District"

    def __str__(self):
        return "{0}".format(self.name)
