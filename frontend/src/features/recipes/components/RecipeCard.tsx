import type { Recipe } from "../types";

interface Props {
    recipe?: Recipe;
    onDelete?: (id: number) => void;
    onToggleFavorite?: (id: number) => void;
    onTogglePinned?: (id: number) => void;
    onCopy?: (id: number, name: string) => void;
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
        const name = window.prompt(
            "New recipe name:",
            `${recipe.name} Copy`
        );

        if (name) {
            onCopy?.(recipe.id, name);
        }
    }

    return (
        <div className="border rounded p-4 space-y-3">
            <div className="flex justify-between">
                <h2 className="text-lg font-semibold">
                    {recipe.name}
                </h2>

                <div className="flex gap-3">
                    <button
                        onClick={() =>
                            onTogglePinned?.(recipe.id)
                        }
                    >
                        {recipe.is_pinned ? "📌" : "📍"}
                    </button>

                    <button
                        onClick={() =>
                            onToggleFavorite?.(recipe.id)
                        }
                    >
                        {recipe.is_favorite ? "⭐" : "☆"}
                    </button>
                </div>
            </div>

            <p>
                {recipe.summary}
            </p>

            {recipe.nutrients.length > 0 && (
                <div className="border-t pt-3">
                    <h3 className="text-sm font-semibold mb-2">
                        Nutrients
                    </h3>

                    <div className="grid grid-cols-2 gap-2 text-sm">
                        {recipe.nutrients.map((nutrient) => (
                            <div key={nutrient.id}>
                                <span className="font-medium">
                                    {nutrient.name}
                                </span>
                                : {nutrient.amount}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <div className="text-sm text-gray-500">
                {recipe.portions}
                {" portions • "}
                {recipe.cooking_time}
                {" min"}
            </div>

            <div className="flex gap-4">
                <button
                    onClick={handleCopy}
                    className="text-blue-600"
                >
                    Copy
                </button>

                <button
                    onClick={() =>
                        onDelete?.(recipe.id)
                    }
                    className="text-red-600"
                >
                    Delete
                </button>
            </div>
        </div>
    );
}