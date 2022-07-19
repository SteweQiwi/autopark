from rest_framework import serializers

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'driver', 'car_model', 'type', 'repair_status', 'fuel_type', 'mileage',
            'number_plate', 'fuel_consumption', 'load_capacity', 'height', 'width', 'length'
        ]

