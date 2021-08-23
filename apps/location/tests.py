from tests.setting.setting import Roles
from rest_framework import status
from tests.setting import setting


class Country(object):

    def create_country(self):
        # region create country using superuser
        country_name = 'Japan'
        role = setting.Roles.SUPERUSER_ROLE_NAME
        superuser_email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
        superuser_password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
        self.login(superuser_email, superuser_password)
        res = self.client.post(self.country_url,
                               {'name': country_name})
        # endregion
        # login again with original user
        self.login(self.email, self.password)
        return res.data['id']

    def test_get_all_countries(self):
        res = self.client.get(self.country_url)
        if res.status_code != status.HTTP_200_OK and \
                res.status_code != status.HTTP_204_NO_CONTENT:
            raise Exception(f'回傳status_code:{res.status_code}')

    def test_get_specific_country(self):
        country_id = self.create_country()
        res = self.client.get(f'{self.country_url}/{country_id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_modify_country(self):
        country_id = self.create_country()
        new_country_name = 'Korea'
        res = self.client.put(f'{self.country_url}/{country_id}',
                              {'name': new_country_name})
        if self.role == Roles.SUPERUSER_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            res = self.client.get(f'{self.country_url}/{country_id}')
            if res.data['name'] != new_country_name:
                raise Exception(f'expected country_name:{new_country_name}, '
                                f'actual country_name:{res.data["name"]}')
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_country(self):
        country_name = 'Japan'
        res = self.client.post(self.country_url,
                               {'name': country_name})
        if self.role == Roles.SUPERUSER_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_country(self):
        country_id = self.create_country()
        res = self.client.delete(f'{self.country_url}/{country_id}')
        if self.role == Roles.SUPERUSER_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
            res = self.client.get(f'{self.country_url}/{country_id}')
            self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class Location(object):
    def test_get_all_locations(self):
        res = self.client.get(self.location_url)
        if res.status_code != status.HTTP_200_OK and \
                res.status_code != status.HTTP_204_NO_CONTENT:
            raise Exception(f'回傳status_code:{res.status_code}')

    def test_create_location(self):
        country_id = self.create_country()
        res = self.client.post(self.location_url,
                               {'country_id': country_id,
                                'address': '東京都墨田区押上1丁目1−2'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_specific_location(self):
        country_id = self.create_country()
        res = self.client.post(self.location_url,
                               {'country_id': country_id,
                                'address': '東京都墨田区押上1丁目1−2'})
        location_id = res.data['id']
        res = self.client.get(f'{self.location_url}/{location_id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
