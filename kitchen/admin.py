from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DishType, Dish, Cook


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("hire_date",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("hire_date",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "hire_date",
                    )
                },
            ),
        )
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("dish_type",)


admin.site.register(DishType)
