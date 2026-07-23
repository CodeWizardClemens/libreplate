import type {
    Recipe,
} from "../types";


interface Props {

    recipe?: Recipe;

    onDelete?: (
        id: number
    ) => void;

    onToggleFavorite?: (
        id: number
    ) => void;

    onTogglePinned?: (
        id: number
    ) => void;

    onCopy?: (
        id: number,
        name: string
    ) => void;

}



export default function RecipeCard({
    recipe,
    onDelete,
    onToggleFavorite,
    onTogglePinned,
    onCopy,
}: Props) {


    if (!recipe) {
        return null;
    }



    function handleCopy() {

        const name =
            window.prompt(
                "New recipe name:",
                `${recipe.name} Copy`
            );


        if (name) {

            onCopy?.(
                recipe.id,
                name
            );

        }

    }



    return (

        <div
            className="
                card
                shadow-sm
            "
        >

            <div
                className="
                    card-body
                "
            >


                <div
                    className="
                        row
                        g-3
                        align-items-start
                    "
                >


                    {/* Pin + Favorite */}
                    <div
                        className="
                            col-12
                            col-md-auto
                            d-flex
                            gap-2
                            order-1
                        "
                    >

                        <button
                            className="
                                btn
                                btn-outline-secondary
                            "
                            onClick={() =>
                                onTogglePinned?.(
                                    recipe.id
                                )
                            }
                            title="Pin"
                        >

                            <i
                                className={
                                    recipe.is_pinned
                                        ? "bi bi-pin-fill"
                                        : "bi bi-pin"
                                }
                            />

                        </button>



                        <button
                            className="
                                btn
                                btn-outline-warning
                            "
                            onClick={() =>
                                onToggleFavorite?.(
                                    recipe.id
                                )
                            }
                            title="Favorite"
                        >

                            <i
                                className={
                                    recipe.is_favorite
                                        ? "bi bi-star-fill"
                                        : "bi bi-star"
                                }
                            />

                        </button>

                    </div>



                    {/* Main content */}
                    <div
                        className="
                            col
                            order-2
                        "
                    >

                        <h5
                            className="
                                card-title
                                mb-2
                            "
                        >
                            {
                                recipe.name
                            }
                        </h5>



                        <p
                            className="
                                card-text
                                mb-3
                            "
                        >
                            {
                                recipe.summary
                            }
                        </p>



                        {
                            recipe.nutrients.length > 0 && (

                                <div
                                    className="
                                        row
                                        g-2
                                        mb-3
                                    "
                                >

                                    {
                                        recipe.nutrients.map(
                                            (nutrient) => (

                                                <div
                                                    key={
                                                        nutrient.id
                                                    }
                                                    className="
                                                        col-6
                                                        col-md-auto
                                                    "
                                                >

                                                    <span
                                                        className="
                                                            badge
                                                            text-bg-light
                                                            border
                                                        "
                                                    >
                                                        {
                                                            nutrient.name
                                                        }

                                                        :
                                                        
                                                        {" "}

                                                        {
                                                            nutrient.amount
                                                        }
                                                    </span>

                                                </div>

                                            )
                                        )
                                    }

                                </div>

                            )
                        }



                        {
                            recipe.tags.length > 0 && (

                                <div
                                    className="
                                        d-flex
                                        flex-wrap
                                        gap-2
                                    "
                                >

                                    {
                                        recipe.tags.map(
                                            (tag) => (

                                                <span
                                                    key={
                                                        tag.id
                                                    }
                                                    className="
                                                        badge
                                                        text-bg-secondary
                                                    "
                                                >
                                                    {
                                                        tag.name
                                                    }
                                                </span>

                                            )
                                        )
                                    }

                                </div>

                            )
                        }



                        <div
                            className="
                                text-muted
                                small
                                mt-3
                            "
                        >

                            {
                                recipe.portions
                            }

                            {" portions • "}

                            {
                                recipe.cooking_time
                            }

                            {" min"}

                        </div>

                    </div>



                    {/* Desktop actions */}
                    <div
                        className="
                            col-12
                            col-md-auto
                            d-none
                            d-md-flex
                            gap-2
                            order-3
                        "
                    >

                        <button
                            className="
                                btn
                                btn-outline-primary
                            "
                            onClick={handleCopy}
                            title="Copy"
                        >

                            <i
                                className="
                                    bi
                                    bi-copy
                                "
                            />

                        </button>



                        <button
                            className="
                                btn
                                btn-outline-danger
                            "
                            onClick={() =>
                                onDelete?.(
                                    recipe.id
                                )
                            }
                            title="Delete"
                        >

                            <i
                                className="
                                    bi
                                    bi-trash
                                "
                            />

                        </button>

                    </div>


                </div>



                {/* Mobile actions */}
                <div
                    className="
                        d-flex
                        d-md-none
                        justify-content-end
                        gap-2
                        mt-3
                    "
                >

                    <button
                        className="
                            btn
                            btn-outline-primary
                        "
                        onClick={handleCopy}
                    >

                        <i
                            className="
                                bi
                                bi-copy
                            "
                        />

                        {" Copy"}

                    </button>



                    <button
                        className="
                            btn
                            btn-outline-danger
                        "
                        onClick={() =>
                            onDelete?.(
                                recipe.id
                            )
                        }
                    >

                        <i
                            className="
                                bi
                                bi-trash
                            "
                        />

                        {" Delete"}

                    </button>


                </div>


            </div>

        </div>

    );
}