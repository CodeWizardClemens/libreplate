from django.contrib.auth.models import User
from django.db import models

from foods.models import Food


class GroceryList(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="grocery_lists"
    )

    date_start = models.DateField()
    date_end = models.DateField()

    generate_from_diary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):

        name = f"Grocery list #{self.id}"

        if self.generate_from_diary:
            name += f" " f"({self.date_start} - {self.date_end})"

        return name


class GroceryListFood(models.Model):

    grocery_list = models.ForeignKey(
        GroceryList, on_delete=models.CASCADE, related_name="items"
    )

    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    has_item = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food.name
