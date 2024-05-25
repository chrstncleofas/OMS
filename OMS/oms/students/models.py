from django.db import models
from django.conf import settings

class StudentTable(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    StudentID = models.CharField(max_length=10, unique=True)
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Course = models.CharField(max_length=100)
    Year = models.IntegerField()
    Username = models.CharField(max_length=100, unique=True)
    Password = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Firstname} {self.Lastname}"