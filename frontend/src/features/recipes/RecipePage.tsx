import { useState } from "react";

import RecipeForm from "./components/RecipeForm";
import RecipeList from "./components/RecipeList";

import {
    useCopyRecipe,
    useCreateRecipe,
    useDeleteRecipe,
    useRecipes,
    useToggleFavorite,
    useTogglePin,
} from "./api";

type SortMethod =
    | "created_at"
    | "updated_at"
    | "name"
    | "last_used_at";

export default function RecipePage() {
    const recipesQuery = useRecipes();

    const createRecipe = useCreateRecipe();
    const deleteRecipe = useDeleteRecipe();

    const toggleFavorite = useToggleFavorite();
    const togglePin = useTogglePin();

    const copyRecipe = useCopyRecipe();

    const [search, setSearch] = useState("");
    const [showFavorites, setShowFavorites] = useState(false);
    const [sortMethod, setSortMethod] =
        useState<SortMethod>("created_at");

    if (recipesQuery.isPending) {
        return <div>Loading...</div>;
    }

    if (recipesQuery.isError) {
        return <div>Failed to load recipes.</div>;
    }

    const filteredRecipes = recipesQuery.data
        .filter((recipe) => {
            const searchTerm = search.toLowerCase();

            const matchesSearch =
                recipe.name.toLowerCase().includes(searchTerm) ||
                recipe.summary.toLowerCase().includes(searchTerm);

            const matchesFavorite =
                !showFavorites || recipe.is_favorite;

            return matchesSearch && matchesFavorite;
        })
        .sort((a, b) => {
            switch (sortMethod) {
                case "name":
                    return a.name.localeCompare(b.name);

                case "created_at":
                    return (
                        new Date(b.created_at).getTime() -
                        new Date(a.created_at).getTime()
                    );

                case "updated_at":
                    return (
                        new Date(b.updated_at).getTime() -
                        new Date(a.updated_at).getTime()
                    );

                case "last_used_at":
                    if (!a.last_used_at) {
                        return 1;
                    }

                    if (!b.last_used_at) {
                        return -1;
                    }

                    return (
                        new Date(b.last_used_at).getTime() -
                        new Date(a.last_used_at).getTime()
                    );

                default:
                    return 0;
            }
        });

    return (
        <div className="max-w-5xl mx-auto p-8 space-y-8">
            <h1 className="text-3xl font-bold">
                Recipes
            </h1>

            <RecipeForm
                onSubmit={(recipe) =>
                    createRecipe.mutate(recipe)
                }
            />

            <div className="flex gap-4 items-center">
                <div className="flex flex-1 border rounded overflow-hidden">
                    <input
                        value={search}
                        onChange={(e) =>
                            setSearch(e.target.value)
                        }
                        placeholder="Search recipes..."
                        className="
                            flex-1
                            px-3
                            py-2
                            outline-none
                        "
                    />

                    <button
                        onClick={() =>
                            setShowFavorites(!showFavorites)
                        }
                        className="px-4 text-xl"
                        title="Show favorites"
                    >
                        {showFavorites ? "⭐" : "☆"}
                    </button>
                </div>

                <select
                    value={sortMethod}
                    onChange={(e) =>
                        setSortMethod(
                            e.target.value as SortMethod
                        )
                    }
                    className="
                        border
                        rounded
                        px-3
                        py-2
                    "
                >
                    <option value="created_at">
                        Created at
                    </option>

                    <option value="updated_at">
                        Updated at
                    </option>

                    <option value="name">
                        Name
                    </option>

                    <option value="last_used_at">
                        Last used at
                    </option>
                </select>
            </div>

            <RecipeList
                recipes={filteredRecipes}
                onDelete={(id) =>
                    deleteRecipe.mutate(id)
                }
                onToggleFavorite={(id) =>
                    toggleFavorite.mutate(id)
                }
                onTogglePinned={(id) =>
                    togglePin.mutate(id)
                }
                onCopy={(id, name) =>
                    copyRecipe.mutate({
                        id,
                        name,
                    })
                }
            />
        </div>
    );
}