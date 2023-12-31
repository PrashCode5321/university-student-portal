# Generated by Django 4.2.1 on 2023-06-17 09:18

from django.db import migrations, models
import students.models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0007_applications_name_alter_student_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=students.models.path_and_rename
            ),
        ),
    ]
