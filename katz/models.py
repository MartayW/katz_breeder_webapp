import os
from datetime import datetime
from django.db import models
from pathlib import Path
# Create your models/classes/db tables here.
# https://docs.djangoproject.com/en/4.1/topics/db/models/
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import auth

# Create your models here.


class User(AbstractUser):
    #is_breeder = models.BooleanField(default=True)
    #user = models.OneToOneField(auth.models.User, null=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=40, null=True)




#This class may need to be integrated with the built-in django.contrib.auth app
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    #Allowing password to be NULL is for development purposes only
    #Do not use in production
    password = models.CharField(max_length=20, null=True, blank=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)


class Breeder(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    breeder_name = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    cattery = models.CharField(max_length=60, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    def __str__(self):
        return self.firstname
class Cat(models.Model):
        #id = models.AutoField(primary_key=True)
        breederId = models.ForeignKey(Breeder, on_delete=models.CASCADE, default=0)
        name = models.CharField(max_length=50, null=True, blank=True)
        birthdate = models.DateTimeField(null=True, blank=True)
        color = models.CharField(max_length=20, null=True, blank=True)
        catType = models.CharField(max_length=10, default="breeder")
        status = models.CharField(max_length=10, default="breeder")
        pattern = models.CharField(max_length=20, null=True, blank=True)
        gender = models.CharField(max_length=1, null=True, blank=True)
        mother = models.IntegerField(null=True, blank=True)
        father = models.IntegerField(null=True, blank=True)
        images = models.ImageField(null=True, blank=True)
        personality = models.TextField(null=True, blank=True)
        #This value will remain NULL until the kitten's status changes to reserved or sold
        #purchaser = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    customerID = models.ForeignKey(Customer, on_delete=models.CASCADE, default=0)
    catID = models.ForeignKey(Cat, on_delete=models.CASCADE, default=0)
    type = models.CharField(max_length=15, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    image_file = models.ImageField(null=True, blank=True)

class CatTest(models.Model):
    owner = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    color = models.CharField(max_length=15, null=True, blank=True)
    personality = models.CharField(max_length=15, null=True, blank=True)
    price = models.CharField(max_length=15, null=True, blank=True)
    mother = models.CharField(max_length=15, null=True, blank=True)
    father = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
#upload_to='cat_pics',
    def __str__(self):
        return self.name

