from django.contrib.auth.models import BaseUserManager
from apps.roles.models import Role
from rent_house_rating_api.enumerations import RoleType


class UserManager(BaseUserManager):
    def create_user(self, email, password, role_name, **extra_fields):
        email = self.normalize_email(email)
        role_id = Role.objects.get(name=role_name).id
        user = self.model(email=email, role_id=role_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, role_name=RoleType.ADMIN, **extra_fields):
        return self.create_user(email, password, role_name, **extra_fields)
