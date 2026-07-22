import type { GroceryItem as GroceryItemType } from "../types";


interface Props {
    item: GroceryItemType;
    onToggle: (id: number) => void;
    onDelete: (id: number) => void;
}



export default function GroceryItem({
    item,
    onToggle,
    onDelete,
}: Props) {


    return (
        <li>

            <input
                type="checkbox"
                checked={item.on_hand}
                onChange={() =>
                    onToggle(item.id)
                }
            />


            <span>
                {item.food_name}
            </span>


            <span>
                {" "}
                ({item.amount})
            </span>



            <button
                onClick={() =>
                    onDelete(item.id)
                }
            >
                Delete
            </button>

        </li>
    );
}