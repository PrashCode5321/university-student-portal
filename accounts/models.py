from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import exceptions
from django.utils.translation import gettext_lazy


def registration_number_validator(value):
    if len(str(value)) != 9:
        raise exceptions.ValidationError(
            gettext_lazy(
                "Registration number must be a nine digit number. Please enter a valid registration number!"
            ),
            params={"value": value},
        )


# Create your models here.
class CustomUser(AbstractUser):
    registration_number = models.IntegerField(
        validators=[registration_number_validator], blank=True, null=True
    )
