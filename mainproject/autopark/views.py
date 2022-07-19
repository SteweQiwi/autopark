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
    serializer_class = FutureOrderSerializer

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']
        return Order.objects.filter(driver_id=driver_id, deadline__gt=timezone.now())


class LastMonthRefillInfoAPIView(generics.ListAPIView):
    serializer_class = LastMonthRefillInfoSerializer

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']
        return Refill.objects.filter(created__gt=timezone.now() - timezone.timedelta(days=30), driver_id=driver_id)


class DriversVehicleOnRepairAPIView(generics.ListAPIView):
    queryset = Driver.objects.filter(vehicle__repair_status=2).distinct()
    serializer_class = DriverSerializer


class DriversWhoRideOnVehicleAPIView(generics.ListAPIView):
    serializer_class = DriverSerializer

    def get_queryset(self):
        order__vehicle = self.kwargs['order__vehicle']
        return Driver.objects.filter(order__vehicle=order__vehicle).distinct()


class ManagerByDriverAPIView(generics.ListAPIView):
    serializer_class = ManagerSerializer

    def get_queryset(self):
        order__driver = self.kwargs["order__driver"]
        return Manager.objects.filter(order__driver=order__driver).distinct()


class DriverByManagerSortMileageAPIView(generics.ListAPIView):
    serializer_class = DriverSerializer

    def get_queryset(self):
        order__manager = self.kwargs['order__manager']
        return Driver.objects.filter(order__manager=order__manager)\
            .annotate(sum=Sum('order__road_distance')).distinct().order_by('-sum')


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
