from datetime import datetime, timedelta
from django.db.models import Sum, Q
from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from django.utils import timezone
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import *
from .permissions import IsAdminOrReadOnly, IsOwner, IsManager, IsDriver
from .serializers import *


# all vehicles
class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager | IsOwner]
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


# all orders
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager | IsOwner]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# all drivers
class DriverViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


# all managers
class ManagerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


# all repairs
class RepairViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager | IsOwner]
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer


# add refills
class RefillCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsOwner | IsDriver]
    queryset = Refill.objects.all()
    serializer_class = RefillSerializer


# all refills
class RefillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Refill.objects.all()
    serializer_class = RefillSerializer


# if driver = retrieve order and update status for his orders(user_id)
class DriverOrderUpdateViewSet(
    viewsets.mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = [IsManager | IsOwner | IsDriver]
    serializer_class = UpdateOrderSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'driver'):
            return Order.objects.filter(driver__user_id=self.request.user.pk).order_by('-id')
        return Order.objects.all().order_by('-id')


# for Managers and Owners on future orders by driver id
class FutureOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager | IsOwner]
    serializer_class = OrderSerializer

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']
        return Order.objects.filter(driver_id=driver_id, deadline__gt=timezone.now())


# Shows future orders for driver by user
class FutureOrderForDriverViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsManager | IsOwner | IsDriver]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'driver'):
            return Order.objects.filter(driver__user_id=self.request.user.pk, deadline__gt=timezone.now())


# Refills by driver id last 30d days
class LastMonthRefillInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = LastMonthRefillInfoSerializer

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']
        return Refill.objects.filter(created__gt=timezone.now() - timezone.timedelta(days=30), driver_id=driver_id)


# Drivers, who's vehicles on repair
class DriversVehicleOnRepairViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Driver.objects.filter(vehicle__repair_status=Vehicle.NOT_READY).distinct()
    serializer_class = DriverSerializer


# Drivers, who ride on vehicle
class DriversWhoRideOnVehicleAPIView(generics.ListCreateAPIView):
    permission_classes = [IsOwner]
    serializer_class = DriverSerializer

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        return Driver.objects.filter(order__vehicle_id=vehicle_id).distinct()


# Managers, who put orders for some driver
class ManagerByDriverAPIView(generics.ListAPIView):
    permission_classes = [IsOwner]
    serializer_class = ManagerSerializer

    def get_queryset(self):
        driver_id = self.kwargs["driver_id"]
        return Manager.objects.filter(order__driver_id=driver_id).distinct()


# Drivers, who takes orders from some manager
class DriverByManagerSortMileageAPIView(generics.ListAPIView):
    permission_classes = [IsOwner]
    serializer_class = DriverSerializer

    def get_queryset(self):
        manager_id = self.kwargs['manager_id']
        return Driver.objects.filter(
            order__manager_id=manager_id
        ).annotate(sum=Sum('order__road_distance')).distinct().order_by('-sum')


# Find vehicle by volume, max_side, and load_capacity
class VehicleBySpecialParametersAPIView(generics.ListAPIView):
    permission_classes = [IsOwner | IsManager]
    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = Vehicle.objects.annotate(
            volume=F('length') * F('width') * F('height')
        ).filter(repair_status=Vehicle.READY).order_by('load_capacity')
        max_side = self.request.query_params.get('max_side')
        volume = self.request.query_params.get('volume')
        load_capacity = self.request.query_params.get('load_capacity')

        if volume:
            queryset = queryset.filter(volume__gte=volume)

        if max_side:
            queryset = queryset.filter(Q(length__gte=max_side) | Q(width__gte=max_side) | Q(height__gte=max_side))

        elif load_capacity:
            queryset = queryset.filter(load_capacity__gte=load_capacity)

        return queryset
