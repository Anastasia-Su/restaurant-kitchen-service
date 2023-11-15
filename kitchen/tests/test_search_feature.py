from django.test import TestCase
from parameterized import parameterized
from django.contrib.auth import get_user_model
from kitchen.models import DishType, Dish, Cook
from kitchen.forms import DishTypeSearchForm, DishSearchForm, CookSearchForm


class SearchFeatureTest(TestCase):
    def setUp(self) -> None:
        self.items = ["Test something", "Test anything", "Test"]

        for name in self.items:
            dishtype = DishType.objects.create(
                name=name,
            )
            Dish.objects.create(
                name=name,
                description="Test12345!",
                price=12.1,
                dish_type=dishtype,
            )
            get_user_model().objects.create_user(
                username=name, first_name="test1", last_name="test2", password="test123"
            )

    @parameterized.expand(
        [
            (Dish, DishSearchForm, "name"),
            (DishType, DishTypeSearchForm, "name"),
            (Cook, CookSearchForm, "username"),
        ]
    )
    def test_partial_search(
        self,
        model: (Dish, DishType, Cook),
        form: (DishSearchForm, DishTypeSearchForm, CookSearchForm),
        field_name: str,
    ) -> None:
        form_data = {
            field_name: "ing",
        }

        form = form(data=form_data)
        self.assertTrue(form.is_valid())

        results = model.objects.filter(
            **{f"{field_name}__icontains": form.cleaned_data[field_name]}
        )

        expected_names = ["Test something", "Test anything"]

        self.assertCountEqual(
            [getattr(item, field_name) for item in results], expected_names
        )
