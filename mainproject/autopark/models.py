from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel


class Vehicle(models.Model):
    LIGHT = 1
    FREIGHT = 2
    BUS = 3

    READY = 1
    NOT_READY = 2

    GAS = 1
    OILER = 2
    PETROL = 3

    VEHICLE_TYPE = (
        (LIGHT, 'Lightweight'),
        (FREIGHT, 'Freight'),
        (BUS, 'Bus'),
    )
    REPAIR_STATUS = (
        (READY, 'Ready to ride'),
        (NOT_READY, 'Under repair'),
    )
    FUEL_TYPE = (
        (GAS, 'Gas'),
        (OILER, 'Oiler'),
        (PETROL, 'Petrol'),
    )
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    type = models.IntegerField(choices=VEHICLE_TYPE)
    car_model = models.CharField(max_length=50)
    repair_status = models.IntegerField(choices=REPAIR_STATUS)
    fuel_type = models.IntegerField(choices=FUEL_TYPE)
    mileage = models.PositiveIntegerField(default=1)
    number_plate = models.CharField(max_length=8)
    fuel_consumption = models.PositiveIntegerField()
    length = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    width = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    height = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    load_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.car_model} {self.length} {self.width} {self.height} {self.get_repair_status_display()}'


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    license = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.name}'


class Order(TimeStampedModel):
    ORDERED = 1
    ACCEPTED = 2
    ON_THE_WAY = 3
    DELIVERED = 4
    STATUS = (
        (ORDERED, 'Ordered'),
        (ACCEPTED, 'Accepted'),
        (ON_THE_WAY, 'On the way'),
        (DELIVERED, 'Delivered'),
    )
    manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
    details = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    status = models.IntegerField(choices=STATUS)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    client_name = models.CharField(max_length=50)
    road_distance = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    length = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    width = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    height = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return f'{self.details} {self.driver}  {self.vehicle} {self.get_status_display()}'


class Refill(TimeStampedModel):
    GAS = 1
    OILER = 2
    PETROL = 3
    FUEL_TYPE = (
        (GAS, 'Gas'),
        (OILER, 'Oiler'),
        (PETROL, 'Petrol'),
    )
    type = models.IntegerField(choices=FUEL_TYPE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    car = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.driver} {self.get_type_display()} {self.price}$ {self.price_per_liter}$/L'

    @property
    def price_per_liter(self):
        return self.price / self.amount


class Repair(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    breakdown = models.CharField(max_length=100)
    deadline = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.vehicle} {self.breakdown} {self.deadline }'


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'
