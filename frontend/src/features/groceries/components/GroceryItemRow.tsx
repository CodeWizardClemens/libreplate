import type { GroceryItem } from "../types";

interface Props {
    item: GroceryItem;
    onToggle(item: GroceryItem): void;
    onDelete(id: number): void;
}

export default function GroceryItemRow({
    item,
    onToggle,
    onDelete,
}: Props) {
    return (
        <div
            style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "12px 0",
                borderBottom: "1px solid #eee",
            }}
        >
            <div>
                <strong>{item.food_name}</strong>

                <div>
                    Amount: {item.amount}
                </div>
            </div>

            <div
                style={{
                    display: "flex",
                    gap: 8,
                }}
            >
                <button
                    onClick={() => onToggle(item)}
                >
                    {item.on_hand
                        ? "On Hand"
                        : "Need"}
                </button>

                <button
                    onClick={() =>
                        onDelete(item.id)
                    }
                >
                    Delete
                </button>
            </div>
        </div>
    );
}