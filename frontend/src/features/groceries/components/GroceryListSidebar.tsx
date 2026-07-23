import type { GroceryList } from "../types";

interface Props {
    lists: GroceryList[];
    selected: GroceryList | null;
    onSelect(list: GroceryList): void;
}

export default function GroceryListSidebar({
    lists,
    selected,
    onSelect,
}: Props) {
    return (
        <aside>
            <h2>Lists</h2>

            {lists.map((list) => (
                <button
                    key={list.id}
                    onClick={() => onSelect(list)}
                    style={{
                        display: "block",
                        width: "100%",
                        marginBottom: 8,
                        padding: 12,
                        background:
                            selected?.id === list.id
                                ? "#ddd"
                                : "#fff",
                    }}
                >
                    <strong>{list.name}</strong>

                    <br />

                    <small>
                        {list.date_start} → {list.date_end}
                    </small>
                </button>
            ))}
        </aside>
    );
}