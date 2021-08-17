from tests.setting import setting
from tests.base import TestBase


class SuperUser(TestBase):
    role = setting.Roles().SUPERUSER_ROLE_NAME


class NormalUserOne(TestBase):
    role = setting.Roles().NORMAL_USER_ONE_ROLE_NAME

