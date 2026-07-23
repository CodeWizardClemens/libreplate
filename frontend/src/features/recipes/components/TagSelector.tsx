import type {
    RecipeTag,
} from "../types";


interface Props {

    tags: RecipeTag[];

    selectedTags: number[];

    onChange: (
        tags: number[]
    ) => void;

}


export default function TagSelector({
    tags,
    selectedTags,
    onChange,
}: Props) {


    function toggleTag(
        id: number
    ) {

        if (
            selectedTags.includes(id)
        ) {

            onChange(
                selectedTags.filter(
                    (tagId) =>
                        tagId !== id
                )
            );

            return;
        }


        onChange([
            ...selectedTags,
            id,
        ]);
    }



    return (
        <div
            className="
                flex
                flex-wrap
                gap-2
                p-3
                border-t
            "
        >

            {
                tags.map((tag) => (

                    <button
                        key={tag.id}
                        type="button"
                        onClick={() =>
                            toggleTag(
                                tag.id
                            )
                        }
                        className={`
                            border
                            rounded
                            px-3
                            py-1
                            text-sm
                            ${
                                selectedTags.includes(
                                    tag.id
                                )
                                    ? "bg-gray-200"
                                    : ""
                            }
                        `}
                    >
                        {
                            tag.name
                        }
                    </button>

                ))
            }

        </div>
    );
}