export interface Nutrient {
  id: number;
  name: string;
  amount: number;
}

export interface Recipe {
  id: number;
  name: string;

  is_favorite: boolean;
  is_pinned: boolean;

  summary: string;
  description: string;
  instructions: string;

  cooking_time: number;
  portions: number;

  last_used_at: string | null;
  created_at: string;
  updated_at: string;

  tags: number[];

  nutrients: Nutrient[];
}

export interface RecipeCreate {
  name: string;
  summary: string;
  description: string;
  instructions: string;
  cooking_time: number;
  portions: number;
  tags: number[];

  is_favorite?: boolean;
  is_pinned?: boolean;
}