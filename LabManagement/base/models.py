from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class LabAdmin(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20)
    def __str__(self):
        return str(self.name)

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    age = models.IntegerField(default=20)
    last_login = models.DateField(null=True)

    
    def __str__(self):
        return str(self.name)
    
    def is_authenticated(self):
        pass

class Tests(models.Model):
    test_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.name


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    total_tests_cost = models.DecimalField(max_digits=10, decimal_places=2)


class VisitDetails(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    test_cost = models.DecimalField(max_digits=8, decimal_places=2)