from django.contrib import admin

from .models import (
    Meal, OptionGroup, Option,
)

# Register your models here.

admin.site.register(Meal)
admin.site.register(OptionGroup)
admin.site.register(Option)
