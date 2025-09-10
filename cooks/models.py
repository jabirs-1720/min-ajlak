from django.db import models
from django.utils.translation import gettext_lazy as _

from meals.models import Meal

# Create your models here.

class Order(models.Model):
    number = models.IntegerField(_('number'), default=1)
    meals = models.ManyToManyField(Meal, verbose_name=_('meals'))
    ordered_at = models.DateTimeField(_('ordered at'), auto_now_add=True)

    def __str__(self):
        return f'#{self.number}'
