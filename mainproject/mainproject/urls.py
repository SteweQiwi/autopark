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
from rest_framework import routers

from autopark.views import *

router = routers.DefaultRouter()
router.register('vehicle', VehicleViewSet)
router.register(r'future-order/(?P<driver_id>[^/.]+)', FutureOrderViewSet, basename='FutureOrder')
router.register(
    r'last-month-refill-info/(?P<driver_id>[^/.]+)',
    LastMonthRefillInfoViewSet, basename='LastMonthRefillInfo'
)
router.register(r'drivers-vehicle-on-repair', DriversVehicleOnRepairViewSet)
router.register(
    r'drivers-who-ride-on-vehicle/(?P<vehicle_id>[^/.]+)',
    DriversWhoRideOnVehicleViewSet, basename='DriverWhoRideOnVehicle'
)
router.register(
    r'manager-by-driver/(?P<driver_id>[^/.]+)',
    ManagerByDriverViewSet, basename='ManagerByDriver'
)
router.register(
    r'driver-by-manager/(?P<manager_id>[^/.]+)',
    DriverByManagerSortMileageViewSet, basename='DriverByManagerSortMileage'
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    # path('api/v1/vehicle-list/', VehicleViewSet.as_view({'get': 'list'})),
    # path('api/v1/vehicle-list/<int:pk>', VehicleViewSet.as_view({'put': 'update'})),
    path('api/v1/future-order/<int:driver_id>/', FutureOrderAPIView.as_view()),
    path('api/v1/last-month-refill-info/<int:driver_id>/', LastMonthRefillInfoAPIView.as_view()),
    path('api/v1/drivers-vehicle-on-repair/', DriversVehicleOnRepairAPIView.as_view()),
    path('api/v1/drivers-who-ride-on-vehicle/<int:vehicle_id>/', DriversWhoRideOnVehicleAPIView.as_view()),
    path('api/v1/managers-driver/<int:order__driver>', ManagerByDriverAPIView.as_view()),
    path('api/v1/drivers-manager-sortby-mileage/<int:order__manager>/', DriverByManagerSortMileageAPIView.as_view()),
    path('api/v1/vehicle-by-special-parameters/', VehicleBySpecialParametersAPIView.as_view()),
]
