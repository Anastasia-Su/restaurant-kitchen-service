from django.db import models
from users.models import Cook


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    cooks = models.ManyToManyField(Cook, related_name="dishes")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    dishes = models.ManyToManyField(Dish, related_name="ingredients")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
