from tests.setting.setting import Roles
from rest_framework import status


class Country(object):
    country_url = '/location/countries'

    def test_get_countries(self):
        res = self.client.get(self.country_url)
        if res.status_code != status.HTTP_200_OK and \
                res.status_code != status.HTTP_204_NO_CONTENT:
            raise Exception(f'回傳status_code:{res.status_code}')

    def test_create_country(self):
        country_name = 'Japan'
        res = self.client.post(self.country_url,
                               {'name': country_name})
        if self.role == Roles.SUPERUSER_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
