from django.urls import path

from .views import (
    CookListView,
    CookDetailView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    RememberMeLoginView,
    SignUpView,
)

urlpatterns = [
    # path("", index, name="index"),
    path("accounts/login/", RememberMeLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),

    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path(
        "cooks/<int:pk>/update/",
        CookUpdateView.as_view(),
        name="cook-update",
    ),
    path(
        "cooks/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cook-delete",
    ),
]

app_name = "users"
