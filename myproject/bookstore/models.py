from django.db import models

# Create your models here.
class Book(models.Model):
    type = models.CharField(max_length = 20)
    name = models.CharField(max_length = 200)
    location = models.CharField(max_length = 10)
    price = models.FloatField()
    thumbnail = models.TextField()
    publishDay = models.DateField(null = True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True)

class Author(models.Model):
    name = models.CharField(max_length = 30)
    nickName = models.CharField(max_length = 30, null = True)
    gender = models.CharField(max_length = 1, null = True)
    birthday = models.DateField(null = True)
    address = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 20, null = True)
    mobile = models.CharField(max_length = 11, null = True)
    email = models.EmailField()

class Publisher(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 20, null = True)
    email = models.EmailField(null = True)
