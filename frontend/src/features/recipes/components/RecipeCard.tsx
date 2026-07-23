import type { Recipe } from "../types";

interface Props {
    recipe?: Recipe;
    onDelete?: (id: number) => void;
    onToggleFavorite?: (id: number, value: boolean) => void;
    onTogglePinned?: (id: number, value: boolean) => void;
}

export default function RecipeCard({
    recipe,
    onDelete,
    onToggleFavorite,
    onTogglePinned,
}: Props) {
    if (!recipe) {
        return null;
    }

    return (
        <div className="border rounded p-4 space-y-2">
            <div className="flex justify-between items-start">
                <h2 className="text-lg font-semibold">
                    {recipe.name}
                </h2>

                <div className="flex gap-2">
                    <button
                        onClick={() =>
                            onTogglePinned?.(
                                recipe.id,
                                !recipe.is_pinned
                            )
                        }
                    >
                        {recipe.is_pinned ? "📌" : "📍"}
                    </button>

                    <button
                        onClick={() =>
                            onToggleFavorite?.(
                                recipe.id,
                                !recipe.is_favorite
                            )
                        }
                    >
                        {recipe.is_favorite ? "⭐" : "☆"}
                    </button>
                </div>
            </div>

            <p>{recipe.summary}</p>

            <div className="text-sm text-gray-500">
                {recipe.portions} portions • {recipe.cooking_time} min
            </div>

            <button
                onClick={() => onDelete?.(recipe.id)}
                className="text-red-600"
            >
                Delete
            </button>
        </div>
    );
}