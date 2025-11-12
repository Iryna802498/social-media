from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Allows to update/partial-update/delete only the owner of the property."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
