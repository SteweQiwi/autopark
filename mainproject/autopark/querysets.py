from django.db.models import Count, Q, F
from django.utils import timezone
from autopark.models import *

# QuerySet 1


q1 = Order.objects.filter(driver__id=1, deadline__gt=timezone.now())


# QuerySet 2

q2 = Refill.objects.filter(created__gt=timezone.now()-timezone.timedelta(days=30), driver__id=1)


# QuerySet 3

q3 = Driver.objects.filter(vehicle__repair_status=2).distinct()


# QuerySet 4

q4 = Driver.objects.filter(order__vehicle=7)


# QuerySet 5

q5 = Manager.objects.filter(order__driver=1)


# QuerySet 6

q6 = Driver.objects.filter(order__manager=1).order_by("order__vehicle__mileage")


# QuerySet 7

q7 = Vehicle.objects\
    .annotate(volume=F('length')*F('width')*F('height'))\
    .filter(
        Q(volume__gte=6) & Q(length__gte=3) | Q(width__gte=3) | Q(height__gte=3),
        load_capacity__gte=400, repair_status=1
    )\
    .exclude(order__deadline__range=["2022-7-20", "2023-7-20"])\
    .order_by("load_capacity")
