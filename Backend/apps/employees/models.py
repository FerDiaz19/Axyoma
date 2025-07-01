from django.db import models
from apps.users.models import Company

class Plant(models.Model):
    pk_plant = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    creation_date = models.DateField()
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE)

class Department(models.Model):
    pk_department = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

class Position(models.Model):
    pk_position = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class Employee(models.Model):
    pk_employee = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    registration_date = models.DateField()
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    plant = models.ForeignKey(Plant, on_delete=models.SET_NULL, null=True)