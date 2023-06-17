# Generated by Django 4.2.1 on 2023-06-16 10:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0006_alter_student_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="applications",
            name="name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="image",
            field=models.ImageField(
                blank=True,
                default="students/default.png",
                null=True,
                upload_to="students",
            ),
        ),
    ]
