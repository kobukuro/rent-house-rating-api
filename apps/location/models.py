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
    country = models.ForeignKey(Country, related_name='locations', on_delete=models.CASCADE, null=False)
    # 房東名字，可不填
    owner_name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='locations', on_delete=models.CASCADE, null=False,
                                   # 指定column name(不會因為ForeignKey，在後面加上column name)
                                   db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # fields順序很重要！
            models.UniqueConstraint(fields=['address', 'country', 'owner_name'], name='unique_address_country'),
        ]
