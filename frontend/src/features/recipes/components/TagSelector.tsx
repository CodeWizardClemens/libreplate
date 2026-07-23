import type {
    RecipeTag,
} from "../types";


interface Props {
    tags: RecipeTag[];
    selectedTags: number[];
    onChange: (tags: number[]) => void;
}


export default function TagSelector({
    tags,
    selectedTags,
    onChange,
}: Props) {

    function toggleTag(id: number) {
        if (selectedTags.includes(id)) {
            onChange(
                selectedTags.filter(
                    (tagId) => tagId !== id
                )
            );
        } else {
            onChange([
                ...selectedTags,
                id,
            ]);
        }
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
            {tags.map((tag) => {
                const isSelected = selectedTags.includes(tag.id);

                return (
                    <button
                        key={tag.id}
                        type="button"
                        onClick={() => toggleTag(tag.id)}
                        className={`
                            border
                            rounded
                            px-3
                            py-1
                            text-sm
                            transition
                            ${
                                isSelected
                                    ? "bg-blue-500 text-white border-blue-500"
                                    : "bg-white text-gray-700"
                            }
                        `}
                    >
                        {tag.name}
                    </button>
                );
            })}
        </div>
    );
}