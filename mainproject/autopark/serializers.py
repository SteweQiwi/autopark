from rest_framework import serializers
from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'driver', 'car_model', 'type', 'repair_status', 'fuel_type', 'mileage',
            'number_plate', 'fuel_consumption', 'load_capacity', 'height', 'width', 'length', 'id'
        ]
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'manager', 'driver', 'client_name', 'vehicle', 'details', 'deadline', 'status', 'road_distance', 'length', 'width',
            'height', 'weight', 'id'
        ]
        read_only_fields = ['id']


class DriverSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Driver
        fields = ['name', 'user', 'license']


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['user']


class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['breakdown', 'cost', 'vehicle', 'deadline']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'manager', 'client_name', 'vehicle', 'details', 'deadline', 'status', 'road_distance', 'length', 'width',
            'height', 'weight', 'driver', 'id'
        ]
        read_only_fields = [
            'manager', 'client_name', 'vehicle', 'details', 'deadline', 'road_distance', 'length', 'width',
            'height', 'weight', 'driver', 'id'
        ]


class RefillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refill
        fields = [
            'type', 'price', 'amount', 'car', 'driver'
        ]


class LastMonthRefillInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refill
        fields = [
            'type', 'amount', 'price', 'id'
        ]
        read_only_fields = ['id']




