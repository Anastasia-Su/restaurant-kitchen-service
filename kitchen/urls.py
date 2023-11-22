from django.urls import path

from .views import (
    index,
    DishTypeListView,
    DishListView,
    DishDetailView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "dishtypes/",
        DishTypeListView.as_view(),
        name="dishtype-list",
    ),
    path(
        "dishtypes/create/",
        DishTypeCreateView.as_view(),
        name="dishtype-create",
    ),
    path(
        "dishtypes/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dishtype-update",
    ),
    path(
        "dishtypes/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dishtype-delete",
    ),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
]

app_name = "kitchen"
