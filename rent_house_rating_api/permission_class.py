from rest_framework.permissions import BasePermission
from apps.system.models import Api, Role, ApiPrivileges
from rent_house_rating_api.enumerations import MethodPrivilege


class CustomPermissionClass(BasePermission):
    def __init__(self, api_name):
        super().__init__()
        self.api_name = api_name

    def __call__(self):
        return self

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            try:
                api_id = Api.objects.get(name=self.api_name).id
            except Api.DoesNotExist:
                return False
            role_id = request.user.role.id
            privilege = ApiPrivileges.objects.get(api_id=api_id,
                                                  role_id=role_id).privilege
            if request.method == 'GET' and privilege & MethodPrivilege.GET:
                return True
            elif request.method == 'POST' and privilege & MethodPrivilege.POST:
                return True
            elif request.method == 'PUT' and privilege & MethodPrivilege.PUT:
                return True
            elif request.method == 'PATCH' and privilege & MethodPrivilege.PATCH:
                return True
            elif request.method == 'DELETE' and privilege & MethodPrivilege.DELETE:
                return True
            else:
                return False
