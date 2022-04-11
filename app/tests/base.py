from django.test import TestCase
from rest_framework.test import APIClient
from tests.setting import setting


class TestBase(TestCase):
    register_url = '/system/register'
    login_url = '/system/login'
    user_url = '/system/users'
    country_url = '/location/countries'
    location_url = '/location/locations'
    rating_url = '/location/ratings'

    def setUp(self):
        self.client = APIClient()
        self.create_users()
        self.username = setting.AUTH_DATA[self.role][setting.USERNAME_NAME]
        self.email = setting.AUTH_DATA[self.role][setting.EMAIL_NAME]
        self.password = setting.AUTH_DATA[self.role][setting.PASSWORD_NAME]
        self.login(self.email, self.password)

    def create_users(self):
        # region create superuser
        role = setting.Roles.SUPERUSER_ROLE_NAME
        username = setting.AUTH_DATA[role][setting.USERNAME_NAME]
        email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
        password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
        from apps.system.models import User
        User.objects.create_superuser(username=username,
                                      email=email,
                                      password=password)
        # endregion
        # region create normal user one
        role = setting.Roles.NORMAL_USER_ONE_ROLE_NAME
        username = setting.AUTH_DATA[role][setting.USERNAME_NAME]
        email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
        password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
        response = self.client.post(self.register_url,
                                    {'username': username,
                                     'email': email,
                                     'password': password,
                                     'first_name': 'test_first_name',
                                     'last_name': 'test_last_name'})
        # endregion
        # region create normal user two
        role = setting.Roles.NORMAL_USER_TWO_ROLE_NAME
        username = setting.AUTH_DATA[role][setting.USERNAME_NAME]
        email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
        password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
        response = self.client.post(self.register_url,
                                    {'username': username,
                                     'email': email,
                                     'password': password,
                                     'first_name': 'test_first_name',
                                     'last_name': 'test_last_name'})
        # endregion
        # print(response.data)

    def login(self, email, password):
        response = self.client.post(self.login_url, {'email': email, 'password': password})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
