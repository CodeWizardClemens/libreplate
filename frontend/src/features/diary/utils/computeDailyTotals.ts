import type { DayMeal } from "@/types/MealTypes";
import { computeMealTotals } from "./MealFormulas";

export interface DailyTotals {
  energy: number;
  protein: number;
  fat: number;
  carbs: number;
}

export function computeDailyTotals(meals: DayMeal[]): DailyTotals {
  const totals: DailyTotals = {
    energy: 0,
    protein: 0,
    fat: 0,
    carbs: 0,
  };

  for (const meal of meals) {
    const mealTotals = computeMealTotals(meal.meal_foods);

    totals.energy += mealTotals.energy;
    totals.protein += mealTotals.protein;
    totals.fat += mealTotals.fat;
    totals.carbs += mealTotals.carbs;
  }

  return totals;
}
