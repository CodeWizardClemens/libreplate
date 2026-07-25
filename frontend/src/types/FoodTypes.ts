export interface FoodNutrient {
  nutrient_id?: number;
  nutrient_name: string;
  nutrient_unit: string;
  amount: number;
}

export interface Food {
  id: number;
  name: string;
  serving: number | null;
  unit: string;
  barcode: string | null;
  brand: string | null;
  description: string | null;
  is_favorite: boolean;
  usda_fdc_id: number | null;
  nutrients: FoodNutrient[];
}

export interface FoodCreate {
  name: string;
  serving?: number | null;
  unit_id: string;
  barcode?: string | null;
  brand?: string | null;
  description?: string | null;
  is_favorite?: boolean;
  usda_fdc_id?: number | null;
  nutrients?: FoodNutrientCreate[];
}

export interface FoodNutrientCreate {
  nutrient_id: number;
  amount: number;
}

export type FoodUpdate = Partial<FoodCreate>;