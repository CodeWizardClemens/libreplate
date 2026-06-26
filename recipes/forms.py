from django import forms

from .models import Recipe, RecipeIngredient

from common.food_selection import get_user_foods


class RecipeForm(forms.ModelForm):

    class Meta:

        model = Recipe

        fields = [
            "name",
            "description",
            "thumbnail_path",
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


class AddRecipeToDiaryForm(forms.Form):

    meal = forms.ModelChoiceField(queryset=None)

    portions = forms.FloatField(initial=1, min_value=0.1)

    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        from diary.models import Meal

        if user:

            self.fields["meal"].queryset = Meal.objects.filter(user=user).order_by(
                "-date", "order"
            )
