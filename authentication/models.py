from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(_('name'), max_length=100)
    accepts_orders = models.BooleanField(_('accepts orders'), default=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    restaurant = models.OneToOneField(
        Restaurant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('restaurant')
    )

    def __str__(self):
        return self.get_full_name()
