from tests.setting.setting import Roles


class User(object):
    user_url = '/system/users'

    def test_get_users(self):
        res = self.client.get(self.user_url)
        if self.role == Roles.SUPERUSER_ROLE_NAME:
            if res.status_code != 200 and res.status_code != 204:
                raise Exception(f'回傳status_code:{res.status_code}')
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            self.assertEqual(res.status_code, 403)
