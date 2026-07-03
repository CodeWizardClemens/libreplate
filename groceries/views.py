from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from common.food_selection import get_user_foods
from diary.models import Meal, MealFood

from .forms import GroceryListCreateForm
from .models import GroceryList, GroceryListFood
from .services import generate_grocery_items


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
    item = get_object_or_404(
        GroceryListFood,
        pk=pk,
        grocery_list__user=request.user
    )

    item.on_hand = not item.on_hand
    item.save()

    # If HTMX request → return partial
    if request.headers.get("HX-Request"):
        return render(
            request,
            "groceries/partials/item.html",
            {"item": item},
        )

    # fallback (non-HTMX)
    return redirect("grocery_detail", pk=item.grocery_list.pk)


@login_required
def grocery_delete(request, pk):

    grocery = get_object_or_404(GroceryList, pk=pk, user=request.user)

    if request.method == "POST":
        grocery.delete()
        return redirect("groceries")

    return render(request, "groceries/delete.html", {"grocery": grocery})


@login_required
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
