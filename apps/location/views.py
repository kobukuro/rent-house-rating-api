from rest_framework.views import APIView
from apps.location.models import Country, Location, Rating
from apps.system.models import User
from apps.location.serializers import CountrySerializer, LocationSerializer, RatingSerializer
from rest_framework.response import Response
from rest_framework import status
from rent_house_rating_api.permission_class import CustomPermissionClass
from django.http import Http404
from django.db import IntegrityError
from django_filters import rest_framework as filters


class CountryList(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['name']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request):
        countries = Country.objects.all()
        filtered_qs = self.filter_queryset(countries)
        serializer = CountrySerializer(filtered_qs, many=True)
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

    def put(self, request, pk):
        location = self.get_object(pk)
        if request.user.is_superuser:
            serializer = LocationSerializer(location, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if location.created_by_id != request.user.id:
                return Response({'detail': 'You can not modify the location which is not created by you.'},
                                status=status.HTTP_403_FORBIDDEN)
            # ??????location??????????????????????????????rating
            ratings = Rating.objects.filter(location_id=pk).exclude(created_by=request.user.id)
            if ratings:  # ??????location????????????????????????rating
                return Response(
                    {'detail': 'There is rating of other people under this location, so you can not modify.'},
                    status=status.HTTP_412_PRECONDITION_FAILED)
            else:  # ??????location???????????????????????????rating
                serializer = LocationSerializer(location, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        location = self.get_object(pk)
        if request.user.is_superuser:
            serializer = LocationSerializer(location, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if location.created_by_id != request.user.id:
                return Response({'detail': 'You can not modify the location which is not created by you.'},
                                status=status.HTTP_403_FORBIDDEN)
            # ??????location??????????????????????????????rating
            ratings = Rating.objects.filter(location_id=pk).exclude(created_by=request.user.id)
            if ratings:  # ??????location????????????????????????rating
                return Response(
                    {'detail': 'There is rating of other people under this location, so you can not modify.'},
                    status=status.HTTP_412_PRECONDITION_FAILED)
            else:  # ??????location???????????????????????????rating
                serializer = LocationSerializer(location, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = self.get_object(pk)
        if request.user.is_superuser:
            location.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            if location.created_by_id != request.user.id:
                return Response({'detail': 'You can not delete the location which is not created by you.'},
                                status=status.HTTP_403_FORBIDDEN)
            # ??????location??????????????????????????????rating
            ratings = Rating.objects.filter(location_id=pk).exclude(created_by=request.user.id)
            if ratings:  # ??????location????????????????????????rating
                return Response(
                    {'detail': 'There is rating of other people under this location, so you can not delete.'},
                    status=status.HTTP_412_PRECONDITION_FAILED)
            else:  # ??????location???????????????????????????rating
                location.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


class RatingList(APIView):
    permission_classes = [CustomPermissionClass(api_name=__qualname__)]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['location_id', 'created_by']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request):
        ratings = Rating.objects.all()
        filtered_qs = self.filter_queryset(ratings)
        serializer = RatingSerializer(filtered_qs, many=True)
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
            # ?????????????????????rating??????
            if rating.created_by.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = RatingSerializer(rating, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        rating = self.get_object(pk)
        if request.user.is_superuser:
            serializer = RatingSerializer(rating, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # ?????????????????????rating??????
            if rating.created_by.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = RatingSerializer(rating, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rating = self.get_object(pk)
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
