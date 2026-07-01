from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from foods.models import Food
from recipes.models import Recipe, RecipeIngredient


class RecipeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Alice",
            password="password123",
        )

        self.client.login(
            username="Alice",
            password="password123",
        )

        self.food = Food.objects.create(
            name="Chicken",
            serving=1,
            user=self.user,
        )

        self.recipe = Recipe.objects.create(
            user=self.user,
            name="Chicken pasta",
            summary="The best chicken pasta",
            description="Bla bla long text",
            instructions="step1: boil pasta, step2: bake chicken etc.",
            cooking_time="1:00:00",
            portions=1,
        )

        self.ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            food=self.food,
            default_servings=1,
            min_servings=2,
            max_servings=3,
        )

    def test_recipe_create(self):
        response = self.client.post(
            reverse("recipe_create"),
            {
                "name": "Chicken pasta",
                "summary": "The best chicken pasta",
                "description": "Bla bla long text",
                "instructions": "step1: boil pasta, step2: bake chicken etc.",
                "cooking_time": "1:00:00",
                "portions": 1,
            },
        )

        self.assertRedirects(response, reverse("recipes"))

        recipe = (
            Recipe.objects
            .filter(user=self.user, name="Chicken pasta")
            .order_by("-id")
            .first()
        )

        self.assertIsNotNone(recipe)

        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.summary, "The best chicken pasta")
        self.assertEqual(recipe.description, "Bla bla long text")
        self.assertEqual(recipe.instructions, "step1: boil pasta, step2: bake chicken etc.")
        self.assertEqual(recipe.portions, 1)

    def test_recipe_copy(self):
        
        before_count = Recipe.objects.count()

        response = self.client.post(
            reverse("recipe_copy", args=[self.recipe.pk]),
        )

        self.assertEqual(Recipe.objects.count(), before_count + 1)

        copy = Recipe.objects.exclude(pk=self.recipe.pk).latest("id")

        self.assertRedirects(
            response,
            reverse("recipe_edit", args=[copy.pk]),
        )

        self.assertEqual(copy.user, self.user)
        self.assertEqual(copy.summary, self.recipe.summary)
        self.assertEqual(copy.description, self.recipe.description)
        self.assertEqual(copy.instructions, self.recipe.instructions)
        self.assertEqual(copy.cooking_time, self.recipe.cooking_time)
        self.assertEqual(copy.portions, self.recipe.portions)

        self.assertTrue(copy.name.startswith(self.recipe.name))
        self.assertIn("Copy", copy.name)

        self.assertEqual(copy.ingredients.count(), 1)

        ingredient = copy.ingredients.first()
        self.assertEqual(ingredient.food, self.food)
        self.assertEqual(ingredient.default_servings, 1)
        self.assertEqual(ingredient.min_servings, 2)
        self.assertEqual(ingredient.max_servings, 3)

    def test_recipe_delete(self):
        response = self.client.post(
            reverse("recipe_delete", args=[self.recipe.pk]),
        )

        self.assertRedirects(response, reverse("recipes"))

        self.assertFalse(
            Recipe.objects.filter(pk=self.recipe.pk).exists()
        )