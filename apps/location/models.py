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
    created_by = models.ForeignKey(User, related_name='locations', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # fields順序很重要！
            models.UniqueConstraint(fields=['address', 'country'], name='unique_address_country'),
        ]
