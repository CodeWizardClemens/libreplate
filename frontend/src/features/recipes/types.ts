export interface Nutrient {
    id: number;
    name: string;
    amount: number;
}


export interface RecipeTag {
    id: number;
    name: string;
}


export interface RecipeIngredient {
    id: number;

    food: number;
    food_name: string;

    default_servings: number;
    serving_amount: number;

    min_servings: number;
    max_servings: number;

    order: number;
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

    tags: RecipeTag[];

    nutrients: Nutrient[];
}


export interface RecipeCreate {
    name: string;

    summary: string;
    description: string;
    instructions: string;

    cooking_time: number;
    portions: number;

    tag_ids?: number[];
}


export interface RecipeUpdate {
    name?: string;

    summary?: string;
    description?: string;
    instructions?: string;

    cooking_time?: number;
    portions?: number;

    tag_ids?: number[];
}


export interface RecipeIngredientCreate {
    food: number;

    default_servings: number;
    serving_amount: number;

    min_servings: number;
    max_servings: number;

    order: number;
}


export interface RecipeIngredientUpdate {
    food?: number;

    default_servings?: number;
    serving_amount?: number;

    min_servings?: number;
    max_servings?: number;

    order?: number;
}


export interface ToggleFavoriteResponse {
    id: number;
    is_favorite: boolean;
}


export interface TogglePinResponse {
    id: number;
    is_pinned: boolean;
}