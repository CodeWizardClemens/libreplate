import RecipeCard from "./RecipeCard";
import type { Recipe } from "../types";


interface Props {
    recipes: Recipe[];
    onDelete?: (id: number) => void;
    onToggleFavorite?: (
        id: number,
        value: boolean
    ) => void;
    onTogglePinned?: (
        id: number,
        value: boolean
    ) => void;
}


export default function RecipeList({
    recipes,
    onDelete,
    onToggleFavorite,
    onTogglePinned,
}: Props) {
    return (
        <div className="space-y-4">
            {recipes.map((recipe) => (
                <RecipeCard
                    key={recipe.id}
                    recipe={recipe}
                    onDelete={onDelete}
                    onToggleFavorite={onToggleFavorite}
                    onTogglePinned={onTogglePinned}
                />
            ))}
        </div>
    );
}