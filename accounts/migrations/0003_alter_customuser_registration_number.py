# Generated by Django 4.2.1 on 2023-06-17 10:24

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_customuser_registration_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="registration_number",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[accounts.models.registration_number_validator],
            ),
        ),
    ]
