from rest_framework.views import APIView
from apps.users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken
from apps.users.models import User


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


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        parent_result = super().post(request, *args, **kwargs)
        parent_result_status_code = super().post(request, *args, **kwargs).status_code
        # 成功登入要update users_user table的last_login欄位
        if parent_result_status_code == status.HTTP_200_OK:
            user = User.objects.get(email=request.data['email'])
            import datetime
            user.last_login = datetime.datetime.now()
            user.save()
        return parent_result