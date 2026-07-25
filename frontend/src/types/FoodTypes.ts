export interface FoodNutrient {
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

export interface CreateFoodPayload {
  name: string;
  serving?: number | null;
  unit: string;
  barcode?: string | null;
  brand?: string | null;
  description?: string | null;
  is_favorite?: boolean;
  usda_fdc_id?: number | null;
}

export type UpdateFoodPayload = Partial<CreateFoodPayload>;