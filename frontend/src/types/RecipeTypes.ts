import type { RecipeNutrient } from "./NutrientTypes";
import type { Tag } from "./TagTypes";

export interface RecipeTag extends Tag {}

export interface RecipeIngredient {
  id: number;
  food: number;
  food_name: string;
  number_of_servings: number;
  serving_amount: number;
  order: number;
}

export interface RecipePicture {
  id: number;
  image: string;
}

interface RecipeFields {
  name: string;
  summary: string;
  description: string;
  instructions: string;
  cooking_time: number;
  prepping_time: number;
  portions: number;
}

export interface Recipe extends RecipeFields {
  id: number;
  is_favorite: boolean;
  is_pinned: boolean;
  last_used_at: string | null;
  created_at: string;
  updated_at: string;

  tags: RecipeTag[];
  picture: RecipePicture | null;
  ingredients: RecipeIngredient[];
  nutrients: RecipeNutrient[];
}

export interface RecipeCreate extends RecipeFields {
  tag_ids?: number[];
}

export type RecipeUpdate = Partial<RecipeFields> & {
  tag_ids?: number[];
};

interface RecipeIngredientFields {
  food: number;
  number_of_servings: number;
  serving_amount: number;
  order: number;
}

export interface RecipeIngredientCreate extends RecipeIngredientFields {}

export type RecipeIngredientUpdate = Partial<RecipeIngredientFields>;

export interface ToggleFavoriteResponse {
  id: number;
  is_favorite: boolean;
}

export interface TogglePinResponse {
  id: number;
  is_pinned: boolean;
}