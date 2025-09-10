from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from authentication.models import Restaurant

class Meal(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="meals",
        verbose_name=_('restaurant')
    )
    name = models.CharField(_('meal name'), max_length=100)
    base_price = models.DecimalField(
        _('base price'),
        max_digits=8,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0.0)]
    )
    preparation_time = models.PositiveIntegerField(
        _('preparation time (seconds)'),
        default=7,
        validators=[MinValueValidator(7)]
    )

    def __str__(self):
        return self.name

class OptionGroup(models.Model):
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name="option_groups",
        verbose_name=_('meal')
    )
    name = models.CharField(_('group name'), max_length=100)
    allow_multiple = models.BooleanField(_('allow multiple choices'), default=False)

    def __str__(self):
        return f"{self.meal.name} - {self.name}"

class Option(models.Model):
    group = models.ForeignKey(
        OptionGroup,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_('option group')
    )
    name = models.CharField(_('option name'), max_length=100)
    extra_price = models.DecimalField(
        _('extra price'),
        max_digits=8,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0)]
    )

    def __str__(self):
        return f"{self.name} (+{self.extra_price})"
