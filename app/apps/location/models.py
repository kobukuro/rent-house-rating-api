from django.db import models
from apps.system.models import User


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # created_by = models.ForeignKey(User, related_name='countries', on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['id']  # 回傳資料的排序從這裡控制


class Location(models.Model):
    address = models.TextField(blank=False)
    country = models.ForeignKey(Country, related_name='locations', on_delete=models.CASCADE,
                                blank=False)  # blank=False serializer才會去檢查
    # 房東名字，前端要設計，不填的話帶None
    owner_name = models.CharField(max_length=100, blank=False)
    created_by = models.ForeignKey(User, related_name='locations', on_delete=models.CASCADE, null=False,
                                   # 指定column name(不會因為ForeignKey，在後面加上column name)
                                   db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    lat = models.FloatField(blank=False)
    lng = models.FloatField(blank=False)

    class Meta:
        constraints = [
            # fields順序很重要！
            models.UniqueConstraint(fields=['address', 'country', 'owner_name'], name='unique_address_country'),
        ]


class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    location = models.ForeignKey(Location, related_name='ratings', on_delete=models.CASCADE,
                                 blank=False)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=False)
    comment = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE, null=False,
                                   db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'rating', 'created_by'], name='unique_location_rating'),
        ]
