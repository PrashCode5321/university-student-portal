# Generated by Django 4.2.1 on 2023-06-17 10:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_customuser_registration_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="registration_number",
        ),
    ]