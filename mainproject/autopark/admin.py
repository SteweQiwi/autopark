from django.contrib import admin
from .models import Vehicle
from .models import Driver
from .models import Order
from .models import Refill
from .models import Repair
from .models import Manager


class MyAdminSite(admin.AdminSite):
    site_header = "Autopark administration"


admin_site = MyAdminSite(name="myadmin")
admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Order)
admin.site.register(Refill)
admin.site.register(Repair)
admin.site.register(Manager)
