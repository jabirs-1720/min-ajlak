from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Meal
from .serializers import MealSerializer

# Create your views here.

class Meals(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    # Filtering
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['restaurant']
