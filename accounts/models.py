from django.db import models
from django.contrib.auth.models import AbstractUser
from students.models import Student


# Create your models here.
class CustomUser(AbstractUser):
    # registration_number = models.IntegerField()
    pass
