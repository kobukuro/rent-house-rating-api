from tests.setting.setting import Roles
from rest_framework import status


class User(object):

    def test_get_users(self):
        res = self.client.get(self.user_url)
        if self.role == Roles.SUPERUSER_ROLE_NAME:
            if res.status_code != status.HTTP_200_OK and \
                    res.status_code != status.HTTP_204_NO_CONTENT:
                raise Exception(f'回傳status_code:{res.status_code}')
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
