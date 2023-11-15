import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from kitchen.forms import CookCreationForm


class FormTests(TestCase):
    def test_cook_creation_form_with_all_fields_is_valid(self) -> None:
        form_data = {
            "username": "username",
            "password1": "123password321",
            "password2": "123password321",
            "hire_date": datetime.date(2022, 9, 1),
            "first_name": "first_name",
            "last_name": "last_name",
        }

        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
