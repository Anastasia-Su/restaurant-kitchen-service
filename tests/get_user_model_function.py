import datetime

from django.contrib.auth import get_user_model


def get_user_model_function():
    return get_user_model().objects.create_user(
        username="test",
        password="password1",
        hire_date=datetime.date(2022, 9, 1),
    )
