from rest_framework.permissions import BasePermission

class GuestOnly(BasePermission):
    """
    Custom permission to only allow unauthenticated users to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is not authenticated
        return not request.user.is_authenticated
