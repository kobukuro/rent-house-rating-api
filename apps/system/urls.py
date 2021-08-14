from django.urls import path
from apps.system import views
from rest_framework_jwt.views import obtain_jwt_token
from apps.system.views import CustomObtainJSONWebToken

urlpatterns = [
    path('users', views.UserList.as_view()),
    path('register', views.RegisterUserView.as_view()),
    # path('login', obtain_jwt_token),
    path('login', CustomObtainJSONWebToken.as_view()),
]
