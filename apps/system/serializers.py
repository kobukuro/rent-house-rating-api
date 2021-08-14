from rest_framework import serializers
from apps.system.models import User
from apps.system.models import Role
from rent_house_rating_api.enumerations import RoleType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}  # 加這行，此欄位就不會顯示在response裡
        fields = ['id', 'username', 'password',
                  'first_name', 'last_name', 'email']

    # 要override密碼才會hash
    def create(self, validated_data):
        return User.objects.create_user(role_name=RoleType.NORMAL_USER,
                                        **validated_data)
