from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from kitchen.models import DishType, Dish, Cook, Ingredient
from django.contrib.auth.forms import AuthenticationForm


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
        self.fields['ingredients'].label = format_html(
            '<a href="#" class="field-link" '
            'data-target="ingred-menu">'
            'Ingredients'
            '<i class="my-arrow fas fa-arrow-right text-sm ms-1"></i>'
            '</a>'
        )

    class Meta:
        model = Dish
        fields = "__all__"


class CookForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ["username", "first_name", "last_name", "email", "hire_date"]


class CookCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove password hints
        for field_name in ['password1', 'password2', 'username']:
            self.fields[field_name].help_text = ''

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "hire_date",
            "first_name",
            "last_name",
        )


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


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
