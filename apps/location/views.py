from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.system.serializers import UserSerializer
from rest_framework_jwt.views import ObtainJSONWebTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.system.models import User
from rent_house_rating_api.permission_class import CustomPermissionClass


class RegisterUserView(APIView):
    # 此view不需要Authorization 因為是註冊 還沒有辦法登入
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomObtainJSONWebToken(ObtainJSONWebTokenView):
#     def post(self, request, *args, **kwargs):
#         parent_result = super().post(request, *args, **kwargs)
#         parent_result_status_code = super().post(request, *args, **kwargs).status_code
#         # 成功登入要update users_user table的last_login欄位
#         if parent_result_status_code == status.HTTP_201_CREATED:
#             user = User.objects.get(email=request.data['email'])
#             from django.utils import timezone
#             user.last_login = timezone.now()
#             user.save()
#             parent_result.data['username'] = user.username
#         return parent_result

class CustomObtainJSONWebToken(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        parent_result = super().post(request, *args, **kwargs)
        parent_result_status_code = super().post(request, *args, **kwargs).status_code
        # 成功登入要update users_user table的last_login欄位
        if parent_result_status_code == status.HTTP_200_OK:
            user = User.objects.get(email=request.data['email'])
            from django.utils import timezone
            user.last_login = timezone.now()
            user.save()
            parent_result.data['username'] = user.username
        return parent_result

class UserList(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)