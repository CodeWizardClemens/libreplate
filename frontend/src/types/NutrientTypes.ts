export interface Nutrient {
  id: number;
  name: string;
  description: string | null;
  abbreviation: string | null;
  unit: string | null;
  usda_nutrient_number: string | null;
  order: number;
  show_in_diary_total: boolean | null;
  show_in_diary_meal: boolean | null;
  show_in_food_edit: boolean | null;
  show_in_recipe: boolean | null;
  show_in_recipes: boolean | null;
  show_in_foods: boolean | null;
  show_in_goal_edit: boolean | null;
}

export interface RecipeNutrient {
  id: number;
  name: string;
  amount: number;
}