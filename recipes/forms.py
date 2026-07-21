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


class RecipeFilterForm(forms.Form):
    meal_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )

    favorites = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
    )

    edit = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
    )

    search = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    sort = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.HiddenInput(),
    )

    tags = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=forms.MultipleHiddenInput(),
    )

    def __init__(self, *args, sort_choices=None, tag_choices=None, **kwargs):
        super().__init__(*args, **kwargs)

        if sort_choices:
            self.fields["sort"].choices = sort_choices

        if tag_choices:
            self.fields["tags"].choices = tag_choices
