from rest_framework import serializers
from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'driver', 'car_model', 'type', 'repair_status', 'fuel_type', 'mileage',
            'number_plate', 'fuel_consumption', 'load_capacity', 'height', 'width', 'length'
        ]


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class FutureOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class LastMonthRefillInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refill
        fields = [
            'type', 'amount', 'price'
        ]


