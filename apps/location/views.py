from rest_framework.views import APIView
from apps.location.models import Country
from apps.location.serializers import CountrySerializer
from rest_framework.response import Response
from rest_framework import status
from rent_house_rating_api.permission_class import CustomPermissionClass


class CountryList(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        if not serializer.data:
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.data)

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
