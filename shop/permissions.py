from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user



class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение на просмотр объекта только для владельца или администратора.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешения предоставляются только владельцу объекта или администратору.
        is_admin = request.user.is_staff
        is_owner = obj.user == request.user
        return is_admin or is_owner