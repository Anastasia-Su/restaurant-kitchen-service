import math
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Cook(AbstractUser):
    hire_date = models.DateField(default=date.today)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("users:cook-detail", kwargs={"pk": self.pk})

    def get_years_of_experience(self):
        return math.floor((date.today().year - self.hire_date.year))
