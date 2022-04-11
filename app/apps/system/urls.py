from django.urls import path
from apps.system import views
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from apps.system.views import CustomObtainJSONWebToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users', views.UserList.as_view()),
    path('register', views.RegisterUserView.as_view()),
    # path('login', obtain_jwt_token),
    # path('login', CustomObtainJSONWebToken.as_view()),
    # path('refresh_token', refresh_jwt_token),
    path('login', CustomObtainJSONWebToken.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]