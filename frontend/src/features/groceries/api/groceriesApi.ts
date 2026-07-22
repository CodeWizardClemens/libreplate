import type {
    GroceryList,
    GroceryItem,
} from "../types";


const BASE_URL = "/api/groceries";


const fetchOptions: RequestInit = {
    credentials: "include",
    headers: {
        "Content-Type": "application/json",
    },
};



export async function getGroceryLists(): Promise<GroceryList[]> {

    const response = await fetch(
        `${BASE_URL}/`,
        fetchOptions
    );

    console.log("Groceries response:", response.status, response.statusText);

    const body = await response.text();
    console.log("Groceries body:", body);

    if (!response.ok) {
        throw new Error(
            `Failed to fetch grocery lists: ${response.status}`
        );
    }

    return JSON.parse(body);
}



export async function getGroceryItems(
    groceryId: number
): Promise<GroceryItem[]> {


    const response = await fetch(
        `${BASE_URL}/${groceryId}/items/`,
        fetchOptions
    );


    if (!response.ok) {
        throw new Error(
            "Failed to fetch grocery items"
        );
    }


    return response.json();
}




export async function toggleGroceryItem(
    groceryId: number,
    itemId: number
): Promise<GroceryItem> {


    const response = await fetch(
        `${BASE_URL}/${groceryId}/items/${itemId}/toggle/`,
        {
            ...fetchOptions,
            method: "POST",
        }
    );


    if (!response.ok) {
        throw new Error(
            "Failed to toggle item"
        );
    }


    return response.json();
}





export async function deleteGroceryItem(
    groceryId: number,
    itemId: number
): Promise<void> {


    const response = await fetch(
        `${BASE_URL}/${groceryId}/items/${itemId}/`,
        {
            ...fetchOptions,
            method: "DELETE",
        }
    );


    if (!response.ok) {
        throw new Error(
            "Failed to delete item"
        );
    }
}