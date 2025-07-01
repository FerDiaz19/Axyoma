from django.db import models

class Company(models.Model):
    pk_company  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    creation_date = models.DateField()

class Role(models.Model):
    pk_role  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

class User(models.Model):
    pk_user = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    registration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    plant = models.ForeignKey("employees.Plant", on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)