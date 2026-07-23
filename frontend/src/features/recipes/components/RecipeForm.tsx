import { useState } from "react";
import type { RecipeCreate } from "../types";

interface Props {
    onSubmit(recipe: RecipeCreate): void;
}

export default function RecipeForm({
    onSubmit,
}: Props) {
    const [recipe, setRecipe] = useState<RecipeCreate>({
        name: "",
        summary: "",
        description: "",
        instructions: "",
        cooking_time: 30,
        portions: 1,
        tags: [],
    });

    return (
        <form
            className="space-y-4"
            onSubmit={(e) => {
                e.preventDefault();
                onSubmit(recipe);
            }}
        >
            <input
                placeholder="Recipe name"
                value={recipe.name}
                onChange={(e) =>
                    setRecipe({
                        ...recipe,
                        name: e.target.value,
                    })
                }
            />

            <textarea
                placeholder="Summary"
                value={recipe.summary}
                onChange={(e) =>
                    setRecipe({
                        ...recipe,
                        summary: e.target.value,
                    })
                }
            />

            <button type="submit">
                Create Recipe
            </button>
        </form>
    );
}