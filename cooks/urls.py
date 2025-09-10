from rest_framework.routers import DefaultRouter

from .views import Orders

app_name = 'cooks'

router = DefaultRouter()
router.register('orders', Orders, 'orders')

urlpatterns = router.urls
