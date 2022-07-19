"""mainproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from autopark.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/vehicle-list/', VehicleAPIView.as_view()),
    path('api/v1/future-order/', FutureOrderAPIView.as_view()),
    path('api/v1/last-month-refill-info/', LastMonthRefillInfoAPIView.as_view()),
    path('api/v1/drivers-vehicle-on-repair/', DriversVehicleOnRepairAPIView.as_view()),
    path('api/v1/drivers-who-ride-on-vehicle/', DriversWhoRideOnVehicleAPIView.as_view()),
    path('api/v1/managers-driver/', ManagersDriverAPIView.as_view()),
    path('api/v1/drivers-manager-by-mileage/', DriversManagerByMileageAPIView.as_view()),
    path('api/v1/vehicle-by-special-parameters/', VehicleBySpecialParametersAPIView.as_view()),
]
