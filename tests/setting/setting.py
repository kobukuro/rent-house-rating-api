IS_EXECUTE_ALL_TEST = True


class Roles(object):
    SUPERUSER_ROLE_NAME = 'superuser'
    NORMAL_USER_ONE_ROLE_NAME = 'normal_user_1'
    NORMAL_USER_TWO_ROLE_NAME = 'normal_user_2'


USERNAME_NAME = 'username'
EMAIL_NAME = 'email'
PASSWORD_NAME = 'password'

# region 各role的帳密
AUTH_DATA = {
    Roles().SUPERUSER_ROLE_NAME: {
        USERNAME_NAME: 'superuser',
        EMAIL_NAME: 'superuser@superuser.com',
        PASSWORD_NAME: 'superuser'
    },
    Roles().NORMAL_USER_ONE_ROLE_NAME: {
        USERNAME_NAME: 'normal_user',
        EMAIL_NAME: 'normal_user@normaluser.com',
        PASSWORD_NAME: 'normal_user'
    },
    Roles().NORMAL_USER_TWO_ROLE_NAME: {
        USERNAME_NAME: 'normal_user2',
        EMAIL_NAME: 'normal_user2@normaluser2.com',
        PASSWORD_NAME: 'normal_user2'
    }
}
