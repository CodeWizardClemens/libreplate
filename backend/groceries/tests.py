from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from foods.models import Food
from groceries.models import GroceryList, GroceryListFood


class GroceryViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Alice",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            username="Bob",
            password="password123",
        )

        self.client.login(username="Alice", password="password123")

        self.food = Food.objects.create(name="Chicken", serving=1, user_id=self.user.id)
        self.grocery = GroceryList.objects.create(
            user=self.user,
            name="Weekly Shop",
            date_start=date.today(),
            date_end=date.today() + timedelta(days=7),
        )

        self.item = GroceryListFood.objects.create(
            grocery_list=self.grocery,
            food=self.food,
            amount=2,
            on_hand=False,
        )

    def test_grocery_lists(self):
        response = self.client.get(reverse("groceries"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.grocery, response.context["lists"])

    def test_grocery_create_post(self):
        response = self.client.post(
            reverse("grocery_create"),
            {
                "name": "New Grocery List",
                "date_start": date.today(),
                "date_end": date.today() + timedelta(days=5),
            },
        )
        grocery = GroceryList.objects.get(name="New Grocery List")
        self.assertRedirects(
            response,
            reverse("grocery_detail", args=[grocery.pk]),
        )
        self.assertEqual(grocery.user, self.user)

    def test_grocery_detail(self):
        response = self.client.get(reverse("grocery_detail", args=[self.grocery.pk]))
        self.assertEqual(response.status_code, 200)

    def test_toggle_item(self):
        self.assertFalse(self.item.on_hand)
        response = self.client.get(reverse("toggle_item", args=[self.item.pk]))
        self.assertRedirects(
            response,
            reverse("grocery_detail", args=[self.grocery.pk]),
        )

        self.item.refresh_from_db()
        self.assertTrue(self.item.on_hand)

        self.client.get(reverse("toggle_item", args=[self.item.pk]))

        self.item.refresh_from_db()
        self.assertFalse(self.item.on_hand)

    def test_user_cannot_access_other_users_grocery(self):
        other_list = GroceryList.objects.create(
            user=self.other_user,
            name="Private",
        )
        response = self.client.get(reverse("grocery_detail", args=[other_list.pk]))
        self.assertEqual(response.status_code, 404)
        other_item = GroceryListFood.objects.create(
            grocery_list=other_list,
            food=self.food,
            amount=1,
        )
        response = self.client.get(reverse("toggle_item", args=[other_item.pk]))

        self.assertEqual(response.status_code, 404)

    def test_grocery_delete_post(self):
        response = self.client.post(reverse("grocery_delete", args=[self.grocery.pk]))
        self.assertRedirects(response, reverse("groceries"))
        self.assertFalse(GroceryList.objects.filter(pk=self.grocery.pk).exists())
