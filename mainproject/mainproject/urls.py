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
from django.urls import path, include, re_path
from rest_framework import routers
from autopark.views import *

router = routers.DefaultRouter()
router.register('vehicle', VehicleViewSet)
router.register('order', OrderViewSet)
router.register('driver', DriverViewSet)
router.register('manager', ManagerViewSet)
router.register('repair', RepairViewSet)
router.register('refill', RefillViewSet)
router.register('driver-order-update', DriverOrderUpdateViewSet, basename='OrderUpdate')
router.register(r'future-order/(?P<driver_id>[^/.]+)', FutureOrderViewSet, basename='FutureOrder')
router.register('future-order', FutureOrderForDriverViewSet, basename='FutureOrderForDriver')
router.register(
    r'last-month-refill-info/(?P<driver_id>[^/.]+)',
    LastMonthRefillInfoViewSet, basename='LastMonthRefillInfo'
)
router.register(r'drivers-vehicle-on-repair', DriversVehicleOnRepairViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/refill-create/', RefillCreateAPIView.as_view()),
    path('api/v1/drivers-who-ride-on-vehicle/<int:vehicle_id>/', DriversWhoRideOnVehicleAPIView.as_view()),
    path('api/v1/managers-driver/<int:order__driver>', ManagerByDriverAPIView.as_view()),
    path('api/v1/drivers-manager-sort-by-mileage/<int:order__manager>/', DriverByManagerSortMileageAPIView.as_view()),
    path('api/v1/vehicle-by-special-parameters/', VehicleBySpecialParametersAPIView.as_view()),
]
