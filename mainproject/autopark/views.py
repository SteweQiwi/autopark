from django.shortcuts import render
from rest_framework import generics

from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleAPIView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# Create your views here.
