from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .get_user_model_function import get_user_model_function
from django.utils import formats


class AdminTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password",
        )
        self.client.force_login(self.admin_user)

        self.cook = get_user_model_function()

    def test_hire_date_listed(self) -> None:
        url = reverse("admin:kitchen_cook_changelist")
        res = self.client.get(url)

        formatted_date = formats.date_format(self.cook.hire_date, "DATE_FORMAT")

        self.assertContains(res, str(formatted_date))

    def test_cook_detail_hire_date_listed(self) -> None:
        url = reverse(
            "admin:kitchen_cook_change", args=[self.cook.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.cook.hire_date)

    def test_cook_add_fieldsets(self) -> None:
        url = reverse("admin:kitchen_cook_add")
        res = self.client.get(url)
        expected_fields = ["first_name", "last_name", "hire_date"]

        for field in expected_fields:
            self.assertContains(res, field)
