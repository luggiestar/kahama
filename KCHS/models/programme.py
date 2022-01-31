from .region import *


class Programme(models.Model):
    # TYPES = (
    #     ('DIPLOMA', 'DIPLOMA'),
    #     ('CERTIFICATE', 'CERTIFICATE'),
    # )

    name = models.CharField(max_length=40)
    # type = models.CharField(choices=TYPES, max_length=40)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ('name',)
        verbose_name = "Programme"
        verbose_name_plural = "Programme"

    def __str__(self):
        return "{0}".format(self.name)
