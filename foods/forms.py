from django import forms
from .models import Food, FoodNutrient
from nutrients.models import Nutrient


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            "name",
            "serving",
            "unit",
            "thumbnail_path",
            "barcode",
            "brand",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 3,
                "style": "resize: vertical;"
            }),
        }

    def __init__(self, *args, **kwargs):
        show_all = kwargs.pop("show_all", False)  # <-- remove it first

        super().__init__(*args, **kwargs)

        self.nutrient_fields = []

        if show_all:
            nutrients = Nutrient.objects.all().order_by("order")
        else:
            nutrients = Nutrient.objects.filter(show_in_food_edit=True).order_by("order")

        for nutrient in nutrients:
            field_name = f"nutrient_{nutrient.id}"
            self.nutrient_fields.append((field_name, nutrient))

            initial = None

            if self.instance.pk:
                existing = FoodNutrient.objects.filter(
                    food=self.instance,
                    nutrient=nutrient,
                ).first()

                if existing:
                    initial = existing.amount

            self.fields[field_name] = forms.DecimalField(
                required=False,
                label=nutrient.name,
                initial=initial,
            )

    def save(self, commit=True):
        food = super().save(commit=commit)

        # only runs when commit=True (edit flow)
        if commit:
            self.save_nutrients(food)

        return food

    def save_nutrients(self, food):
        for key, value in self.cleaned_data.items():
            if not key.startswith("nutrient_"):
                continue

            if value is None:
                continue

            nutrient_id = int(key.split("_")[1])

            FoodNutrient.objects.update_or_create(
                food=food, nutrient_id=nutrient_id, defaults={"amount": value}
            )
