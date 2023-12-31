from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # if request.method == 'GET':
        if request.method in SAFE_METHODS:
            return True
        else:
            if bool(request.user and request.user.is_staff):
                return True

class FullDjangoModelPermissions(DjangoModelPermissions):

    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
    

class ViewCustomerHistoryPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('store.view_history'))