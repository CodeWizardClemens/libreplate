from django.urls import path

from . import views

urlpatterns = [
    path("", views.grocery_lists, name="groceries"),
    path("create/", views.grocery_create, name="grocery_create"),
    path("<int:pk>/", views.grocery_detail, name="grocery_detail"),
    path("item/<int:pk>/toggle/", views.toggle_item, name="toggle_item"),
    path("<int:pk>/delete/", views.grocery_delete, name="grocery_delete"),
]
