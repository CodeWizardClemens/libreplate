import GroceryItem from "./GroceryItem";

import type {
    GroceryList as GroceryListType,
    GroceryItem as GroceryItemType,
} from "../types";


interface Props {

    grocery: GroceryListType;

    items: GroceryItemType[];

    onToggle: (
        id: number
    ) => void;

    onDelete: (
        id: number
    ) => void;
}



export default function GroceryList({
    grocery,
    items,
    onToggle,
    onDelete,
}: Props) {


    return (
        <section>


            <h2>
                {grocery.name}
            </h2>



            <ul>

                {items.map(item => (

                    <GroceryItem
                        key={item.id}
                        item={item}
                        onToggle={onToggle}
                        onDelete={onDelete}
                    />

                ))}

            </ul>


        </section>
    );
}