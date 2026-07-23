import type { GroceryItem, GroceryList } from "../types";
import GroceryItemRow from "./GroceryItemRow";

interface Props {
    list: GroceryList;
    items: GroceryItem[];
    onToggle(item: GroceryItem): void;
    onDelete(id: number): void;
}

export default function GroceryItems({
    list,
    items,
    onToggle,
    onDelete,
}: Props) {
    return (
        <section>
            <h2>{list.name}</h2>

            {items.length === 0 && <p>No items.</p>}

            {items.map((item) => (
                <GroceryItemRow
                    key={item.id}
                    item={item}
                    onToggle={onToggle}
                    onDelete={onDelete}
                />
            ))}
        </section>
    );
}