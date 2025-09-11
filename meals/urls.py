from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import Meals

app_name = 'items'

router = DefaultRouter()
router.register('', Meals, 'meals')

urlpatterns = router.urls
