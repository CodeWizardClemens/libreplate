import type { Food } from "../foods/types";

/* ===========================
 * Meal Foods
 * =========================== */

export interface MealFood {
  id: number;
  food_id: number;
  food: Food;
  serving_size: number;
  number_of_servings: number;
}

export interface MealFoodCreate {
  meal_id: number;
  food_id: number;
  serving_size: number;
  number_of_servings: number;
}

export type MealFoodUpdate = Partial<
  Omit<MealFoodCreate, "meal_id" | "food_id">
>;

/* ===========================
 * Persisted Meals
 * =========================== */

export interface Meal {
  id: number;
  default_meal: number | null;
  name: string;
  date: string;
  note: string;
  order: number;
  meal_foods: MealFood[];
}

export interface MealCreate {
  default_meal: number;
  name: string;
  date: string;
  note?: string;
  order?: number;
  meal_foods?: Omit<MealFoodCreate, "meal_id">[];
}

export type MealUpdate = Partial<MealCreate>;

/* ===========================
 * Default Meals
 * =========================== */

export interface DefaultMeal {
  id: number;
  name: string;
  description: string;
  order: number;
}

export interface DefaultMealCreate {
  name: string;
  description: string;
  order?: number;
}

export type DefaultMealUpdate = Partial<DefaultMealCreate>;

/* ===========================
 * Day Meals
 * =========================== */

export interface DayMeal {
  /**
   * Null means this meal slot
   * has not yet been persisted.
   */
  meal_id: number | null;
  default_meal: DefaultMeal;
  name: string;
  date: string;
  note: string;
  order: number;
  meal_foods: MealFood[];
}
