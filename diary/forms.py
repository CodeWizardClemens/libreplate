from django import forms

from .models import Meal, MealFood


class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = [
            "name",
        ]


class MealFoodForm(forms.ModelForm):

    class Meta:
        model = MealFood

        fields = [
            "food",
            "serving_size",
            "number_of_servings",
        ]


class AddMealFoodForm(forms.ModelForm):

    class Meta:
        model = MealFood
        fields = [
            "serving_size",
            "number_of_servings",
        ]
