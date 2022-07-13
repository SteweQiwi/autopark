from django.utils import timezone
from mainproject.autopark.models import *



# QuerySet 1

q1 = Order.objects.filter(driver__id="1", deadline__gt=timezone.now())


# QuerySet 2

q2 = Refill.objects.filter(created__gt=timezone.now()-timezone.timedelta(days=30), driver__id="1")


# QuerySet 3

q3 = Driver.objects.filter(vehicle__repair_status=2).distinct()


# QuerySet 4

q4 = Driver.objects.filter(order__vehicle=7)


# QuerySet 5

q5 = Manager.objects.filter(order__driver=1)


# QuerySet 6

q6 = Driver.objects.filter(order__manager=1)