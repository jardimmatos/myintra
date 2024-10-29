from rest_framework.permissions import BasePermission, DjangoModelPermissions
from django.utils.translation import gettext as _
from django.http import JsonResponse

# class RegisterRequest(BasePermission):
#     def has_permission(self, request, view):
#         return False
        

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
        

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


# class IsAuthenticated(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user.is_authenticated)


# Permissões baseadas nas regras de ser_permissions (model)
class PermsApi(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
