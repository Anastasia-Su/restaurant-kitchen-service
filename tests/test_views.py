from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import DishType, Dish
from .get_user_model_function import get_user_model_function

TYPE_URL = reverse("kitchen:dishtype-list")
DISH_URL = reverse("kitchen:dish-list")
COOK_URL = reverse("users:cook-list")


class PublicTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_dishtypes(self):
        DishType.objects.create(
            name="name",
        )
        res = self.client.get(TYPE_URL)
        self.assertEqual(res.status_code, 200)

        dishtypes = DishType.objects.all()
        self.assertEqual(list(res.context["dishtype_list"]), list(dishtypes))

        self.assertTemplateUsed(res, "kitchen/dishtype_list.html")


class PublicDishTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_dishes(self) -> None:
        dishtype = DishType.objects.create(
            name="test_name",
        )
        cook = get_user_model_function()
        dish = Dish.objects.create(
            name="test_dish",
            description="Test12345!",
            price=12.1,
            dish_type=dishtype,
        )
        dish.cooks.set([cook])

        res = self.client.get(DISH_URL)
        self.assertEqual(res.status_code, 200)

        dishes = Dish.objects.all()
        self.assertEqual(list(res.context["dish_list"]), list(dishes))

        self.assertTemplateUsed(res, "kitchen/dish_list.html")


class PublicCookTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(COOK_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_cooks(self) -> None:
        get_user_model_function()

        res = self.client.get(COOK_URL)
        self.assertEqual(res.status_code, 200)

        cooks = get_user_model().objects.all()
        self.assertEqual(list(res.context["cook_list"]), list(cooks))

        self.assertTemplateUsed(res, "users/cook_list.html")
