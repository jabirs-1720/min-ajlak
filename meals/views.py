from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Meal
from .permissions import IsMealRestaurantOwner
from .serializers import MealSerializer

# Create your views here.

class Meals(ModelViewSet):
    permission_classes = [IsMealRestaurantOwner]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    # Filtering
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant']
