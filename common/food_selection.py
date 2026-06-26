# common/food_selection/py

from django.db.models import Max

from foods.models import Food


def get_user_foods(user):
    """
    Returns foods available for this user.
    Used by diary, groceries, etc.
    """

    return (
        Food.objects.filter(user=user)
        .annotate(last_used=Max("mealfood__meal__date"))
        .order_by("-last_used", "name")
    )
