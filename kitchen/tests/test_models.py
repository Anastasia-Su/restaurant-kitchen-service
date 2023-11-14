from django.contrib.auth import get_user_model
from django.test import TestCase
from kitchen.models import DishType, Dish


class ModelTests(TestCase):
    def test_dishtype_str(self) -> None:
        dishtype = DishType.objects.create(
            name="test_name",
        )
        self.assertEqual(
            str(dishtype), dishtype.name
        )

    def test_cook_str(self) -> None:
        cook = get_user_model().objects.create(
            username="test",
            first_name="test1",
            last_name="test2",
            password="test123"
        )
        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_create_cook_with_hire_date(self) -> None:
        cook = get_user_model().objects.create_user(
            username="test",
            password="test123",
            hire_date="2021-10-11",
        )
        self.assertEqual(cook.username, "test")
        self.assertEqual(cook.hire_date, "2021-10-11")
        self.assertTrue(cook.check_password("test123"))

    def test_dish_str(self) -> None:
        dishtype = DishType.objects.create(
            name="test_name",
        )
        cook = get_user_model().objects.create(
            username="test",
            first_name="test1",
            last_name="test2",
            password="test123"
        )
        dish = Dish.objects.create(
            name="test_dish",
            description="Test12345!",
            price=12.1,
            dish_type=dishtype,
        )
        dish.cooks.set([cook])

        self.assertEqual(
            str(dish), dish.name
        )
