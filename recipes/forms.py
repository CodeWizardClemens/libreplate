from django import forms

from common.food_selection import get_user_foods

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe

        fields = [
            "name",
            "summary",
            "description",
            "instructions",
            "cooking_time",
            "portions",
        ]


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient

        fields = [
            "food",
            "default_servings",
            "min_servings",
            "max_servings",
        ]

    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        if user:

            self.fields["food"].queryset = get_user_foods(user)
