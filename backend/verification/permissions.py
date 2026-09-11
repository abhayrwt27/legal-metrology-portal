from rest_framework.permissions import BasePermission

class IsLMOOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_lmo or request.user.is_portal_admin
        )

class IsGATC(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_gatc
