"""
Custom permission: only admins/staff can write; everyone can read.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allow GET, HEAD, OPTIONS for any user.
    Restrict POST, PUT, PATCH, DELETE to staff/admin users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff
