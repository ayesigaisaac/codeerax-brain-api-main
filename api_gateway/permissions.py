from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission: only owners can edit; others can read.
    Assumes model instance has `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.user == request.user


class IsAuthenticatedCustom(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)