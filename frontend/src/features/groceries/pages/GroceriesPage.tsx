import { useEffect, useState } from "react";
import type { GroceryList, GroceryItem } from "../types";

import {
    getGroceryLists,
    getGroceryItems,
    toggleGroceryItem,
    deleteGroceryItem,
} from "../api/groceriesApi";

import GroceryListSidebar from "../components/GroceryListSidebar";
import GroceryItems from "../components/GroceryItems";

export default function GroceryPage() {
    const [lists, setLists] = useState<GroceryList[]>([]);
    const [selectedList, setSelectedList] = useState<GroceryList | null>(null);
    const [items, setItems] = useState<GroceryItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadLists() {
            try {
                const data = await getGroceryLists();
                setLists(data);

                if (data.length > 0) {
                    setSelectedList(data[0]);
                }
            } finally {
                setLoading(false);
            }
        }

        loadLists();
    }, []);

    useEffect(() => {
        if (!selectedList) return;

        getGroceryItems(selectedList.id).then(setItems);
    }, [selectedList]);

    async function handleToggle(item: GroceryItem) {
        if (!selectedList) return;

        const updated = await toggleGroceryItem(
            selectedList.id,
            item.id
        );

        setItems((prev) =>
            prev.map((i) =>
                i.id === updated.id ? updated : i
            )
        );
    }

    async function handleDelete(itemId: number) {
        if (!selectedList) return;

        await deleteGroceryItem(selectedList.id, itemId);

        setItems((prev) =>
            prev.filter((i) => i.id !== itemId)
        );
    }

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <div
            style={{
                display: "grid",
                gridTemplateColumns: "250px 1fr",
                gap: 24,
            }}
        >
            <GroceryListSidebar
                lists={lists}
                selected={selectedList}
                onSelect={setSelectedList}
            />

            {selectedList && (
                <GroceryItems
                    list={selectedList}
                    items={items}
                    onToggle={handleToggle}
                    onDelete={handleDelete}
                />
            )}
        </div>
    );
}