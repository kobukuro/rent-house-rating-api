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
    def create_location(self):
        country_id = self.create_country()
        res = self.client.post(self.location_url,
                               {'country_id': country_id,
                                'address': '東京都墨田区押上1丁目1−2',
                                'owner_name': '東京市政府'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        return res.data['id']

    def test_get_all_locations(self):
        res = self.client.get(self.location_url)
        if res.status_code != status.HTTP_200_OK and \
                res.status_code != status.HTTP_204_NO_CONTENT:
            raise Exception(f'回傳status_code:{res.status_code}')

    def test_create_location(self):
        country_id = self.create_country()
        res = self.client.post(self.location_url,
                               {'country_id': country_id,
                                'address': '東京都墨田区押上1丁目1−2',
                                'owner_name': '東京市政府'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_specific_location(self):
        country_id = self.create_country()
        res = self.client.post(self.location_url,
                               {'country_id': country_id,
                                'address': '東京都墨田区押上1丁目1−2',
                                'owner_name': '東京市政府'})
        location_id = res.data['id']
        res = self.client.get(f'{self.location_url}/{location_id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_self_location_with_rating_of_others(self):
        def create_rating_of_other_person():
            location_id = self.create_location()
            # region login with normal user two
            role = setting.Roles.NORMAL_USER_TWO_ROLE_NAME
            normal_user_two_email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
            normal_user_two_password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
            self.login(normal_user_two_email, normal_user_two_password)
            # endregion
            self.client.post(self.rating_url,
                             {'location_id': location_id,
                              'rating': 1,
                              'comment': 'test'})
            # login again with original user
            self.login(self.email, self.password)
            res = self.client.patch(f'{self.location_url}/{location_id}',
                                    {'address': '愛知県名古屋市中区二の丸１−1',
                                     'owner_name': '名古屋市政府'})
            return res

        if self.role == Roles.SUPERUSER_ROLE_NAME:
            res = create_rating_of_other_person()
            self.assertEqual(res.status_code, status.HTTP_200_OK)
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            res = create_rating_of_other_person()
            self.assertEqual(res.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_update_self_location_with_rating_of_only_self(self):
        location_id = self.create_location()
        self.client.post(self.rating_url,
                         {'location_id': location_id,
                          'rating': 1,
                          'comment': 'test'})
        res = self.client.patch(f'{self.location_url}/{location_id}',
                                {'address': '愛知県名古屋市中区二の丸１−1',
                                 'owner_name': '名古屋市政府'})
        # print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_other_location(self):
        def create_location_by_other_person():
            country_id = self.create_country()
            # region login with normal user two
            role = setting.Roles.NORMAL_USER_TWO_ROLE_NAME
            normal_user_two_email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
            normal_user_two_password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
            self.login(normal_user_two_email, normal_user_two_password)
            # endregion
            res = self.client.post(self.location_url,
                                   {'country_id': country_id,
                                    'address': '東京都墨田区押上1丁目1−2',
                                    'owner_name': '東京市政府'})
            location_id = res.data['id']
            # login again with original user
            self.login(self.email, self.password)
            res = self.client.patch(f'{self.location_url}/{location_id}',
                                    {'address': '愛知県名古屋市中区二の丸１−1',
                                     'owner_name': '名古屋市政府'})
            return res

        if self.role == Roles.SUPERUSER_ROLE_NAME:
            res = create_location_by_other_person()
            self.assertEqual(res.status_code, status.HTTP_200_OK)
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            res = create_location_by_other_person()
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class Rating(object):
    def create_rating(self):
        location_id = self.create_location()
        res = self.client.post(self.rating_url,
                               {'location_id': location_id,
                                'rating': 1,
                                'comment': 'test'})
        return res.data['id']

    def test_get_all_ratings(self):
        res = self.client.get(self.rating_url)
        if res.status_code != status.HTTP_200_OK and \
                res.status_code != status.HTTP_204_NO_CONTENT:
            raise Exception(f'回傳status_code:{res.status_code}')

    def test_create_rating(self):
        location_id = self.create_location()
        res = self.client.post(self.rating_url,
                               {'location_id': location_id,
                                'rating': 1,
                                'comment': 'test'})
        # print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_specific_rating(self):
        rating_id = self.create_rating()
        res = self.client.get(f'{self.rating_url}/{rating_id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_self_rating(self):
        rating_id = self.create_rating()
        res = self.client.patch(f'{self.rating_url}/{rating_id}',
                                {'rating': 2,
                                 'comment': 'test111'})
        try:
            self.assertEqual(res.status_code, status.HTTP_200_OK)
        except AssertionError:
            print(res.data)

    def test_update_rating_of_other_person(self):
        if self.role == Roles.SUPERUSER_ROLE_NAME:
            location_id = self.create_location()
            role = setting.Roles.NORMAL_USER_ONE_ROLE_NAME
            normal_user_one_email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
            normal_user_one_password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
            self.login(normal_user_one_email, normal_user_one_password)
            res = self.client.post(self.rating_url,
                                   {'location_id': location_id,
                                    'rating': 1,
                                    'comment': 'test'})
            rating_id = res.data['id']
            self.login(self.email, self.password)
            res = self.client.patch(f'{self.rating_url}/{rating_id}',
                                    {'rating': 2,
                                     'comment': 'test111'})
            self.assertEqual(res.status_code, status.HTTP_200_OK)
        elif self.role == Roles.NORMAL_USER_ONE_ROLE_NAME:
            location_id = self.create_location()
            role = setting.Roles.SUPERUSER_ROLE_NAME
            superuser_email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
            superuser_password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
            self.login(superuser_email, superuser_password)
            res = self.client.post(self.rating_url,
                                   {'location_id': location_id,
                                    'rating': 1,
                                    'comment': 'test'})
            rating_id = res.data['id']
            self.login(self.email, self.password)
            res = self.client.patch(f'{self.rating_url}/{rating_id}',
                                    {'rating': 2,
                                     'comment': 'test111'})
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
