from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Order
from .serializers import OrderSerializer

# Create your views here.

class Orders(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
