import { useState } from "react";
import DailyTotalsBar from "./components//DailyTotalsBar";

import { useDayMeals, useCreateMeal, useCreateMealFood } from "@/api/MealAPI";

import FoodPickerModal from "../foods/components/FoodPickerModal";
import RecipePickerModal from "../recipes/components/common/Recipepickermodal";
import AddToMealModal from "./components/AddToMealModal";

import DiaryHeader from "./components/DiaryHeader";
import MealList from "./components/MealList";

import type { DayMeal } from "@/types/MealTypes";
import type { Food } from "@/types/FoodTypes";
import type { Recipe } from "@/types/RecipeTypes";

function formatDate(date: Date) {
  return date.toISOString().split("T")[0];
}

export default function DiaryPage() {
  const todayString = formatDate(new Date());

  const [selectedDate, setSelectedDate] = useState(todayString);

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isFoodPickerOpen, setIsFoodPickerOpen] = useState(false);
  const [isRecipePickerOpen, setIsRecipePickerOpen] = useState(false);

  const [selectedMeal, setSelectedMeal] = useState<DayMeal | null>(null);

  const { data: meals = [], isLoading, isError } = useDayMeals(selectedDate);

  const createMeal = useCreateMeal();
  const createMealFood = useCreateMealFood();

  function changeDay(amount: number) {
    const date = new Date(selectedDate);
    date.setDate(date.getDate() + amount);

    setSelectedDate(formatDate(date));
  }

  function openAddModal(meal: DayMeal) {
    setSelectedMeal(meal);
    setIsAddModalOpen(true);
  }

  function openFoodPicker() {
    setIsAddModalOpen(false);
    setIsFoodPickerOpen(true);
  }

  function openRecipePicker() {
    setIsAddModalOpen(false);
    setIsRecipePickerOpen(true);
  }

  async function ensureMealId(meal: DayMeal) {
    if (meal.meal_id !== null) {
      return meal.meal_id;
    }

    const newMeal = await createMeal.mutateAsync({
      default_meal: meal.default_meal.id,
      name: meal.name,
      date: meal.date,
      note: meal.note,
      order: meal.order,
      meal_foods: [],
    });

    return newMeal.id;
  }

  async function handleFoodSelect(foods: Food[]) {
    if (!selectedMeal || foods.length === 0) {
      return;
    }

    const mealId = await ensureMealId(selectedMeal);

    for (const food of foods) {
      await createMealFood.mutateAsync({
        meal_id: mealId,
        food_id: food.id,
        serving_size: food.serving ?? 1,
        number_of_servings: 1,
      });
    }

    setIsFoodPickerOpen(false);
    setSelectedMeal(null);
  }

  async function handleRecipeSelect(recipe: Recipe, servings: number) {
    if (!selectedMeal) {
      return;
    }

    const mealId = await ensureMealId(selectedMeal);

    for (const ingredient of recipe.ingredients) {
      await createMealFood.mutateAsync({
        meal_id: mealId,
        food_id: ingredient.food,
        serving_size: ingredient.serving_amount,
        number_of_servings: ingredient.number_of_servings * servings,
      });
    }

    setIsRecipePickerOpen(false);
    setSelectedMeal(null);
  }

  function closeAddModal() {
    setIsAddModalOpen(false);
    setSelectedMeal(null);
  }

  function closeFoodPicker() {
    setIsFoodPickerOpen(false);
    setSelectedMeal(null);
  }

  function closeRecipePicker() {
    setIsRecipePickerOpen(false);
    setSelectedMeal(null);
  }

  return (
    <div className="container">
      <AddToMealModal
        isOpen={isAddModalOpen}
        onClose={closeAddModal}
        onFood={openFoodPicker}
        onRecipe={openRecipePicker}
      />

      <FoodPickerModal
        isOpen={isFoodPickerOpen}
        onClose={closeFoodPicker}
        onSelect={handleFoodSelect}
      />

      <RecipePickerModal
        isOpen={isRecipePickerOpen}
        onClose={closeRecipePicker}
        onSelect={handleRecipeSelect}
      />

      <DiaryHeader
        selectedDate={selectedDate}
        todayString={todayString}
        onChangeDate={setSelectedDate}
        onPrevious={() => changeDay(-1)}
        onNext={() => changeDay(1)}
        onToday={() => setSelectedDate(todayString)}
      />

      {isError && (
        <div className="alert alert-danger">Failed to load diary.</div>
      )}

      {!isLoading && meals.length === 0 && (
        <div className="alert alert-secondary">No meal slots configured.</div>
      )}

      <DailyTotalsBar meals={meals} />

      <MealList meals={meals} onAdd={openAddModal} />
    </div>
  );
}
