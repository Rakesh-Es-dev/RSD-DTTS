from django.db import models
from django.contrib import auth
# Create your models here.

class User(auth.models.User,auth.models.PermissionsMixin):
    def __str__(self):
        return self.username

class Region(models.Model):
    regionId = models.PositiveIntegerField()
    region = models.CharField(max_length=256)
    def __str__(self):
        return self.region

class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE,related_name="resides")
    cityId = models.PositiveIntegerField()
    city = models.CharField(max_length=256)
    def __str__(self):
        return self.city

