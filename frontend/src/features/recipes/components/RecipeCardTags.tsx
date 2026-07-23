import type {
    Recipe,
} from "../types";


interface Props {

    recipe: Recipe;

    availableTags: Recipe["tags"];

    update: (
        data: {
            tag_ids: number[];
        }
    ) => void;

}



export default function RecipeCardTags({
    recipe,
    availableTags,
    update,
}: Props) {


    const unusedTags =
        availableTags.filter(
            (tag) =>
                !recipe.tags.some(
                    (recipeTag) =>
                        recipeTag.id === tag.id
                )
        );



    function addTag(
        tagId: number
    ) {

        update({
            tag_ids: [
                ...recipe.tags.map(
                    (tag) =>
                        tag.id
                ),

                tagId,
            ],
        });

    }



    function removeTag(
        tagId: number
    ) {

        update({
            tag_ids:
                recipe.tags
                    .filter(
                        (tag) =>
                            tag.id !== tagId
                    )
                    .map(
                        (tag) =>
                            tag.id
                    ),
        });

    }



    return (

        <div
            className="
                d-flex
                flex-wrap
                align-items-center
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
                                d-flex
                                align-items-center
                                gap-1
                            "
                        >

                            {tag.name}



                            <button
                                type="button"
                                className="
                                    btn
                                    btn-sm
                                    p-0
                                    text-white
                                    border-0
                                    lh-1
                                "
                                onClick={() =>
                                    removeTag(
                                        tag.id
                                    )
                                }
                                title="Remove tag"
                            >

                                <i
                                    className="
                                        bi
                                        bi-x
                                    "
                                />

                            </button>


                        </span>

                    )
                )
            }



            {
                unusedTags.length > 0 && (

                    <div
                        className="
                            dropdown
                        "
                    >

                        <button
                            className="
                                btn
                                btn-sm
                                btn-outline-secondary
                            "
                            type="button"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                            title="Add tag"
                        >

                            <i
                                className="
                                    bi
                                    bi-plus
                                "
                            />

                        </button>



                        <ul
                            className="
                                dropdown-menu
                            "
                        >

                            {
                                unusedTags.map(
                                    (tag) => (

                                        <li
                                            key={
                                                tag.id
                                            }
                                        >

                                            <button
                                                className="
                                                    dropdown-item
                                                "
                                                type="button"
                                                onClick={() =>
                                                    addTag(
                                                        tag.id
                                                    )
                                                }
                                            >

                                                {tag.name}

                                            </button>

                                        </li>

                                    )
                                )
                            }

                        </ul>

                    </div>

                )
            }


        </div>

    );

}