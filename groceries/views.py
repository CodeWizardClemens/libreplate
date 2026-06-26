from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import GroceryList, GroceryListFood
from .forms import GroceryListCreateForm

from diary.models import MealFood, Meal
from .services import generate_grocery_items
from common.food_selection import get_user_foods


@login_required
def grocery_lists(request):

    lists = GroceryList.objects.filter(user=request.user)

    return render(request, "groceries/list.html", {"lists": lists})


@login_required
def grocery_create(request):

    if request.method == "POST":

        form = GroceryListCreateForm(request.POST)

        if form.is_valid():

            grocery = form.save(commit=False)

            grocery.user = request.user

            grocery.save()

            if grocery.generate_from_diary:

                generate_grocery_items(grocery)

            return redirect("grocery_detail", pk=grocery.pk)

    else:

        form = GroceryListCreateForm()

    return render(request, "groceries/create.html", {"form": form})


@login_required
def grocery_detail(request, pk):

    grocery = get_object_or_404(GroceryList, pk=pk, user=request.user)

    return render(request, "groceries/detail.html", {"grocery": grocery})


@login_required
def toggle_item(request, pk):

    item = get_object_or_404(GroceryListFood, pk=pk, grocery_list__user=request.user)

    item.has_item = not item.has_item
    item.save()

    return redirect("grocery_detail", pk=item.grocery_list.pk)


@login_required
def grocery_delete(request, pk):

    grocery = get_object_or_404(GroceryList, pk=pk, user=request.user)

    if request.method == "POST":
        grocery.delete()
        return redirect("groceries")

    return render(request, "groceries/delete.html", {"grocery": grocery})


def add_item(request, pk):

    grocery = get_object_or_404(GroceryList, pk=pk, user=request.user)

    foods = get_user_foods(request.user)

    return render(
        request,
        "groceries/add_item.html",
        {
            "grocery": grocery,
            "foods": foods,
        },
    )
