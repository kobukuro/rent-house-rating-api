from apps.system.models import User
from tests.setting import setting


def create_users():
    pass
    # roles = setting.Roles()
    # role = roles.SUPERUSER_ROLE_NAME
    # username = setting.AUTH_DATA[role][setting.USERNAME_NAME]
    # email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
    # password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
    # response = self.client.post(self.login_url, {'email': email, 'password': password})


    # User.objects.create_superuser(username=username,
    #                               email=email,
    #                               password=password)
    # role = roles.NORMAL_USER_ONE_ROLE_NAME
    # username = setting.AUTH_DATA[role][setting.USERNAME_NAME]
    # email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
    # password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
    # User.objects.create_user(username=username,
    #                          email=email,
    #                          password=password)
    # role = roles.NORMAL_USER_TWO_ROLE_NAME
    # username = setting.AUTH_DATA[role][setting.USERNAME_NAME]
    # email = setting.AUTH_DATA[role][setting.EMAIL_NAME]
    # password = setting.AUTH_DATA[role][setting.PASSWORD_NAME]
    # User.objects.create_user(username=username,
    #                          email='example@abc.com',
    #                          password=password)
