from rest_framework import permissions

class IsMealRestaurantOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated and getattr(request.user, 'restaurant', None) is not None:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.restaurant == getattr(request.user, 'restaurant', None)
