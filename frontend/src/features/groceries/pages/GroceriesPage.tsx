import { useEffect, useState, useCallback } from "react";

import GroceryList from "../components/GroceryList";

import type { GroceryList as GroceryListType, GroceryItem } from "../types";

import {
    getGroceryLists,
    getGroceryItems,
    toggleGroceryItem,
    deleteGroceryItem,
} from "../api/groceriesApi";

export default function GroceriesPage() {
    const [groceries, setGroceries] = useState<GroceryListType[]>([]);
    const [selectedGrocery, setSelectedGrocery] = useState<GroceryListType | null>(null);
    const [items, setItems] = useState<GroceryItem[]>([]);
    const [error, setError] = useState<string | null>(null);

    const selectGrocery = useCallback(
        async (grocery: GroceryListType) => {
            try {
                setError(null);
                setSelectedGrocery(grocery);

                const data = await getGroceryItems(grocery.id);

                setItems(data);
            } catch (err) {
                console.error(err);
                setError("Failed to load grocery items");
            }
        },
        []
    );

    useEffect(() => {
        async function load() {
            try {
                setError(null);

                const data = await getGroceryLists();

                setGroceries(data);

                if (data.length > 0) {
                    await selectGrocery(data[0]);
                }
            } catch (err) {
                console.error(err);
                setError("Failed to load groceries");
            }
        }

        load();
    }, [selectGrocery]);

    async function handleToggle(itemId: number) {
        if (!selectedGrocery) {
            return;
        }

        try {
            const updatedItem = await toggleGroceryItem(
                selectedGrocery.id,
                itemId
            );

            setItems(current =>
                current.map(item =>
                    item.id === updatedItem.id ? updatedItem : item
                )
            );
        } catch (err) {
            console.error(err);
            setError("Failed to toggle item");
        }
    }

    async function handleDelete(itemId: number) {
        if (!selectedGrocery) {
            return;
        }

        try {
            await deleteGroceryItem(
                selectedGrocery.id,
                itemId
            );

            setItems(current =>
                current.filter(item => item.id !== itemId)
            );
        } catch (err) {
            console.error(err);
            setError("Failed to delete item");
        }
    }

    return (
        <main>
            <h1>Groceries</h1>

            {error && <p>{error}</p>}

            <nav>
                {groceries.map(grocery => (
                    <button
                        key={grocery.id}
                        onClick={() => selectGrocery(grocery)}
                    >
                        {grocery.name}
                    </button>
                ))}
            </nav>

            {selectedGrocery && (
                <GroceryList
                    grocery={selectedGrocery}
                    items={items}
                    onToggle={handleToggle}
                    onDelete={handleDelete}
                />
            )}
        </main>
    );
}