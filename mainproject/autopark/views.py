from django.db.models import Sum, Q
from django.shortcuts import render
from rest_framework import generics
from django.utils import timezone
from .models import *
from .serializers import *


class VehicleAPIView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class FutureOrderAPIView(generics.ListAPIView):
    queryset = Order.objects.filter(driver__id=1, deadline__gt=timezone.now())
    serializer_class = FutureOrderSerializer


class LastMonthRefillInfoAPIView(generics.ListAPIView):
    queryset = Refill.objects.filter(created__gt=timezone.now() - timezone.timedelta(days=30), driver__id=1)
    serializer_class = LastMonthRefillInfoSerializer


class DriversVehicleOnRepairAPIView(generics.ListAPIView):
    queryset = Driver.objects.filter(vehicle__repair_status=2).distinct()
    serializer_class = DriverSerializer


class DriversWhoRideOnVehicleAPIView(generics.ListAPIView):
    queryset = Driver.objects.filter(order__vehicle=7).distinct()
    serializer_class = DriverSerializer


class ManagersDriverAPIView(generics.ListAPIView):
    queryset = Manager.objects.filter(order__driver=1).distinct()
    serializer_class = ManagerSerializer


class DriversManagerByMileageAPIView(generics.ListAPIView):
    queryset = Driver.objects.filter(order__manager__id=2)\
        .annotate(sum=Sum('order__road_distance')).distinct().order_by('-sum')
    serializer_class = DriverSerializer


class VehicleBySpecialParametersAPIView(generics.ListAPIView):
    queryset = Vehicle.objects\
        .annotate(volume=F('length')*F('width')*F('height'))\
        .filter(
            Q(volume__gte=6) & Q(length__gte=3) | Q(width__gte=3) | Q(height__gte=3),
            load_capacity__gte=400, repair_status=1
        )\
        .exclude(order__deadline__range=["2022-7-20", "2023-7-20"])\
        .order_by("load_capacity")
    serializer_class = VehicleSerializer


# Create your views here.
