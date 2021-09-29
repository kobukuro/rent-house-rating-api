from rest_framework.views import APIView
from apps.location.models import Country, Location, Rating
from apps.system.models import User
from apps.location.serializers import CountrySerializer, LocationSerializer, RatingSerializer
from rest_framework.response import Response
from rest_framework import status
from rent_house_rating_api.permission_class import CustomPermissionClass
from django.http import Http404
from django.db import IntegrityError


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


class CountryDetail(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]

    def get_object(self, pk):
        try:
            return Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    def put(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        country = self.get_object(pk)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationList(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                country_id = request.data['country_id']
                serializer.save(country_id=country_id, created_by=user)
            except IntegrityError as e:
                serializer.error_messages = str(e)
                return Response(serializer.error_messages,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetail(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]

    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    # 假如這個location底下有不是自己的rating，就不能改，
    # 回傳412
    def put(self, request, pk):
        location = self.get_object(pk)
        # Rating.objects.get(location_i)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingList(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]

    def get(self, request):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(location_id=request.data['location_id'], created_by=user)
            except IntegrityError as e:
                serializer.error_messages = str(e)
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingDetail(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]

    def get_object(self, pk):
        try:
            return Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        rating = self.get_object(pk)
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    def put(self, request, pk):
        rating = self.get_object(pk)
        if request.user.is_superuser:
            serializer = RatingSerializer(rating, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 只能改自己寫的rating資料
            if rating.created_by.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = RatingSerializer(rating, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
