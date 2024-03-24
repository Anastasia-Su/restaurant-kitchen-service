from django import forms
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from kitchen.models import DishType, Dish, Ingredient


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ingredients"].label = format_html(
            '<a href="#" class="field-link" '
            'data-target="ingred-menu">'
            "Ingredients"
            '<i class="my-arrow fas fa-arrow-right text-sm ms-1"></i>'
            "</a>"
        )

    class Meta:
        model = Dish
        fields = "__all__"


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by dish type"}),
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )
