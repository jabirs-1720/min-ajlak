from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Meal
from .serializers import MealSerializer

# Create your views here.

class Meals(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
