from django.db.models import Sum, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from django.utils import timezone
from .models import *
from .serializers import *


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class FutureOrderViewSet(viewsets.ModelViewSet):
    serializer_class = FutureOrderSerializer

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']
        return Order.objects.filter(driver_id=driver_id, deadline__gt=timezone.now())


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


class LastMonthRefillInfoViewSet(viewsets.ModelViewSet):
    serializer_class = LastMonthRefillInfoSerializer

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']
        return Refill.objects.filter(created__gt=timezone.now() - timezone.timedelta(days=30), driver_id=driver_id)


class DriversVehicleOnRepairAPIView(generics.ListAPIView):
    queryset = Driver.objects.filter(vehicle__repair_status=Vehicle.NOT_READY).distinct()
    serializer_class = DriverSerializer


class DriversVehicleOnRepairViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.filter(vehicle__repair_status=Vehicle.NOT_READY).distinct()
    serializer_class = DriverSerializer


class DriversWhoRideOnVehicleAPIView(generics.ListCreateAPIView):
    serializer_class = DriverSerializer

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        return Driver.objects.filter(order__vehicle_id=vehicle_id).distinct()


class DriversWhoRideOnVehicleViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        return Driver.objects.filter(order__vehicle_id=vehicle_id).distinct()


class ManagerByDriverAPIView(generics.ListAPIView):
    serializer_class = ManagerSerializer

    def get_queryset(self):
        driver_id = self.kwargs["driver_id"]
        return Manager.objects.filter(order__driver_id=driver_id).distinct()


class ManagerByDriverViewSet(viewsets.ModelViewSet):
    serializer_class = ManagerSerializer

    def get_queryset(self):
        driver_id = self.kwargs["driver_id"]
        return Manager.objects.filter(order__driver_id=driver_id).distinct()


class DriverByManagerSortMileageAPIView(generics.ListAPIView):
    serializer_class = DriverSerializer

    def get_queryset(self):
        manager_id = self.kwargs['manager_id']
        return Driver.objects.filter(
            order__manager_id=manager_id
        ).annotate(sum=Sum('order__road_distance')).distinct().order_by('-sum')


class DriverByManagerSortMileageViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer

    def get_queryset(self):
        manager_id = self.kwargs['manager_id']
        return Driver.objects.filter(
            order__manager_id=manager_id
        ).annotate(sum=Sum('order__road_distance')).distinct().order_by('-sum')


class VehicleBySpecialParametersAPIView(generics.ListAPIView):
    queryset = Vehicle.objects.annotate(
        volume=F('length') * F('width') * F('height')
    ).filter(
        Q(volume__gte=6) & Q(length__gte=3) | Q(width__gte=3) | Q(height__gte=3),
        load_capacity__gte=400, repair_status=Vehicle.READY
    ).exclude(order__deadline__range=["2022-7-20", "2023-7-20"]).order_by("load_capacity")
    serializer_class = VehicleSerializer


# Create your views here.
