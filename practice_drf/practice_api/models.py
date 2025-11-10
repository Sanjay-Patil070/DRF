from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username


# Create your models here.
class Employee_2(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    department = models.CharField(max_length=100)
    salary = models.FloatField()

    def __str__(self):
        return self.name

    db_table = "employee_2"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    class Meta:
        db_table = "book"

    def __str__(self):
        return self.title
