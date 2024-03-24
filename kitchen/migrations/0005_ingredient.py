# Generated by Django 4.2.6 on 2023-11-11 13:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kitchen", "0004_remove_dishtype_related_dishes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "dishes",
                    models.ManyToManyField(
                        related_name="ingredients", to="kitchen.dish"
                    ),
                ),
            ],
        ),
    ]