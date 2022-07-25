from django.contrib.auth.models import User
from django.db import models


class OneTimeCode(models.Model):
    code = models.CharField(max_length=30, null=True, verbose_name="Код")
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name="Код")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Временный код'
        verbose_name_plural = 'Временные коды'