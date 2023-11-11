from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from kitchen.models import DishType, Dish, Cook
from django.contrib.auth.forms import AuthenticationForm



class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
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


# class CookRegisterForm(UserCreationForm):
#     class Meta:
#         model = Cook
#         fields = ['username', 'email', 'password1', 'password2']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['placeholder'] = 'Username'
#         self.fields['email'].widget.attrs['placeholder'] = 'Email'
#         self.fields['password1'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password2'].widget.attrs['placeholder'] = 'Password confirm'


# class CookLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['placeholder'] = 'Username'
#         self.fields['password'].widget.attrs['placeholder'] = 'Password'


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
