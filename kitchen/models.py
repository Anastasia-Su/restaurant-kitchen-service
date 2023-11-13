import math
from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    hire_date = models.DateField(default=date.today)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})

    def get_years_of_experience(self):
        return math.floor((date.today().year - self.hire_date.year))


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

