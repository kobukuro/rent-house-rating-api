from rest_framework import serializers
from apps.location.models import Country, Location, Rating


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']  # response的欄位


class LocationSerializer(serializers.ModelSerializer):
    # response顯示哪一個欄位的設定(顯示country table的country_name)
    # 記得fields裡面也要有
    country_name = serializers.ReadOnlyField(source='country.country_name')
    country_id = serializers.IntegerField()

    class Meta:
        model = Location
        fields = ['id', 'address', 'country_id', 'country_name', 'owner_name', 'lat', 'lng']


#     def update(self, instance, validated_data):
#         # dict.get(arg1, arg2) 第二個參數為預設值 沒有的話會帶這個
#         instance.country_id = validated_data.get('country_id',
#                                                  instance.country_id)
#         instance.address_full_text = validated_data.get('address_full_text',
#                                                         instance.address_full_text)
#         instance.save()
#         return instance

class RatingSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField()  # 加在這裡serializer才會檢查

    class Meta:
        model = Rating
        fields = ['id', 'rating', 'comment', 'location_id']
