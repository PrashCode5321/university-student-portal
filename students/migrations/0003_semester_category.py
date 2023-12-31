# Generated by Django 4.2.1 on 2023-06-02 09:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0002_alter_exams_subject"),
    ]

    operations = [
        migrations.AddField(
            model_name="semester",
            name="category",
            field=models.CharField(
                choices=[("C", "Current"), ("R", "Re-Registered"), ("D", "Completed")],
                default="C",
                max_length=1,
            ),
        ),
    ]
