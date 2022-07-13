from django.utils import timezone
from mainproject.autopark.models import Order, Refill, Repair, Vehicle
import datetime


# QuerySet 1

q1 = Order.objects.filter(driver__id="1", deadline__gt=timezone.now())


# QuerySet 2

q2 = Refill.objects.filter(created__gt=datetime.datetime.today() - datetime.timedelta(days=30)).values('type', 'price', 'amount')
# Refill.objects.filter(created__gt=timezone.now()-dateutil.relativedelta(months=1))


# QuerySet 3

q3 = Repair.objects.values_list('vehicle__driver__name', flat=True).distinct()
# q3 = Vehicle.objects.filter(repair_status=2).values_list('driver__name', flat=True).distinct()


