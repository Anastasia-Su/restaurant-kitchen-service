# Generated by Django 4.2.6 on 2023-11-09 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kitchen", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cook",
            name="years_of_experience",
        ),
        migrations.AddField(
            model_name="cook",
            name="hire_date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
