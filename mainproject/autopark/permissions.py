from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'driver')


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'manager')
