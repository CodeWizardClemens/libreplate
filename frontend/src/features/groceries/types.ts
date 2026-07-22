export interface GroceryList {
    id: number;
    name: string;
    date_start: string;
    date_end: string;
    created_at: string;
    updated_at: string;
}


export interface GroceryItem {
    id: number;
    food: number;
    food_name: string;
    amount: number;
    on_hand: boolean;
}