import { useState } from "react";

import {
  useDayMeals,
  useCreateMeal,
  useCreateMealFood,
} from "./api";

import FoodPickerModal from "../foods/components/FoodPickerModal";

import DiaryHeader from "./components/DiaryHeader";
import MealList from "./components/MealList";

import type { DayMeal } from "./types";
import type { Food } from "../foods/types";

function formatDate(date: Date) {
  return date.toISOString().split("T")[0];
}

export default function DiaryPage() {
  const todayString = formatDate(new Date());

  const [selectedDate, setSelectedDate] = useState(todayString);
  const [isFoodPickerOpen, setIsFoodPickerOpen] = useState(false);
  const [selectedMeal, setSelectedMeal] = useState<DayMeal | null>(null);

  const {
    data: meals = [],
    isLoading,
    isError,
  } = useDayMeals(selectedDate);

  const createMeal = useCreateMeal();
  const createMealFood = useCreateMealFood();

  function changeDay(amount: number) {
    const date = new Date(selectedDate);
    date.setDate(date.getDate() + amount);

    setSelectedDate(formatDate(date));
  }

  function openFoodPicker(meal: DayMeal) {
    setSelectedMeal(meal);
    setIsFoodPickerOpen(true);
  }

  async function handleFoodSelect(food: Food) {
    if (!selectedMeal) {
      return;
    }

    let mealId = selectedMeal.meal_id;

    if (mealId === null) {
      const newMeal = await createMeal.mutateAsync({
        default_meal: selectedMeal.default_meal.id,
        name: selectedMeal.name,
        date: selectedMeal.date,
        note: selectedMeal.note,
        order: selectedMeal.order,
        meal_foods: [],
      });

      mealId = newMeal.id;
    }

    await createMealFood.mutateAsync({
      meal_id: mealId,
      food_id: food.id,
      serving_size: food.serving_size ?? 1,
      number_of_servings: 1,
    });

    setIsFoodPickerOpen(false);
    setSelectedMeal(null);
  }

  function closeFoodPicker() {
    setIsFoodPickerOpen(false);
    setSelectedMeal(null);
  }

  return (
    <div className="container py-4">
      <FoodPickerModal
        isOpen={isFoodPickerOpen}
        onClose={closeFoodPicker}
        onSelect={handleFoodSelect}
      />

      <DiaryHeader
        selectedDate={selectedDate}
        todayString={todayString}
        onChangeDate={setSelectedDate}
        onPrevious={() => changeDay(-1)}
        onNext={() => changeDay(1)}
        onToday={() => setSelectedDate(todayString)}
      />

      {isLoading && (
        <div className="alert alert-info">
          Loading meals...
        </div>
      )}

      {isError && (
        <div className="alert alert-danger">
          Failed to load diary.
        </div>
      )}

      {!isLoading && meals.length === 0 && (
        <div className="alert alert-secondary">
          No meal slots configured.
        </div>
      )}

      <MealList
        meals={meals}
        onAddFood={openFoodPicker}
      />
    </div>
  );
}