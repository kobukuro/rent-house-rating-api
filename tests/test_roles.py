from tests.setting import setting
from tests.base import TestBase


class SuperUser(TestBase):
    role = setting.Roles().SUPERUSER_ROLE_NAME
