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

class Supplier(models.Model):
    gln = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class Drugs(models.Model):
    gtin = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    domain = models.PositiveIntegerField(null=True)
    legal = models.BooleanField(null=True)
    marketing = models.BooleanField(null=True)
    drugStatus = models.BooleanField(null=True)
    importable = models.BooleanField(null=True)
    exportable = models.BooleanField(null=True)
    registrationNumber = models.CharField(max_length=256)
    genericName = models.CharField(max_length=256,null=True)
    price = models.DecimalField(max_digits=256,decimal_places=3,null=True)
    dosage = models.CharField(max_length=256,null=True)
    packageSize = models.CharField(max_length=256,null=True)
    packageType = models.CharField(max_length=256,null=True)
    strength = models.CharField(max_length=256,null=True)
    unitStrength = models.CharField(max_length=256,null=True)
    volume = models.CharField(max_length=256,null=True)
    volumeUnit = models.CharField(max_length=256,null=True)
    suppliers = models.ManyToManyField(Supplier,null=True)
    def __str__(self):
        return self.name
