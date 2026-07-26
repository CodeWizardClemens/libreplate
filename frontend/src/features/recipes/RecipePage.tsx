import { useState } from "react";
import { useNavigate } from "react-router-dom";

import RecipeList from "./components/recipes/RecipeList";
import RecipeSearchBar, {
  type RecipeSortMethod,
} from "./components/recipes/RecipeSearchBar";

import {
  useCopyRecipe,
  useCreateRecipe,
  useDeleteRecipe,
  useRecipeTags,
  useRecipes,
  useToggleFavorite,
  useTogglePin,
} from "@/api/RecipeAPI";

export default function RecipePage() {
  const navigate = useNavigate();

  const recipesQuery = useRecipes();
  const tagsQuery = useRecipeTags();

  const deleteRecipe = useDeleteRecipe();
  const toggleFavorite = useToggleFavorite();
  const togglePin = useTogglePin();
  const copyRecipe = useCopyRecipe();
  const createRecipe = useCreateRecipe();

  const [search, setSearch] = useState("");
  const [selectedTags, setSelectedTags] = useState<number[]>([]);
  const [showFavorites, setShowFavorites] = useState(false);
  const [sortMethod, setSortMethod] = useState<RecipeSortMethod>("created_at");

  if (recipesQuery.isPending) {
    return <div className="container py-3">Loading...</div>;
  }

  if (recipesQuery.isError) {
    return <div className="container py-3">Failed to load recipes.</div>;
  }

  const recipes = recipesQuery.data;

  function handleAddRecipe() {
    createRecipe.mutate(
      {
        name: "New recipe",
        summary: "",
        description: "",
        instructions: "",
        cooking_time: 0,
        prepping_time: 0,
        portions: 1,
      },
      {
        onSuccess: (recipe) => {
          navigate(`/recipes/${recipe.id}/edit`);
        },
      },
    );
  }

  const filteredRecipes = recipes
    .filter((recipe) => {
      const searchTerm = search.toLowerCase();

      const matchesSearch =
        recipe.name.toLowerCase().includes(searchTerm) ||
        recipe.summary.toLowerCase().includes(searchTerm);

      const matchesFavorite = !showFavorites || recipe.is_favorite;

      const matchesTags =
        selectedTags.length === 0 ||
        selectedTags.every((tagId) =>
          recipe.tags.some((tag) => tag.id === tagId),
        );

      return matchesSearch && matchesFavorite && matchesTags;
    })
    .sort((a, b) => {
      if (a.is_pinned && !b.is_pinned) return -1;
      if (!a.is_pinned && b.is_pinned) return 1;

      switch (sortMethod) {
        case "name":
          return a.name.localeCompare(b.name);

        case "created_at":
          return (
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
          );

        case "updated_at":
          return (
            new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
          );

        case "last_used_at":
          if (!a.last_used_at) return 1;
          if (!b.last_used_at) return -1;

          return (
            new Date(b.last_used_at).getTime() -
            new Date(a.last_used_at).getTime()
          );

        default:
          return 0;
      }
    });

  return (
    <div className="container">
      <div className="text-start mb-2">
        <button
          type="button"
          className="btn btn-outline-primary"
          onClick={handleAddRecipe}
          disabled={createRecipe.isPending}
        >
          New recipe
        </button>
      </div>

      <div className="mb-3">
        <RecipeSearchBar
          search={search}
          onSearchChange={setSearch}
          recipeCount={filteredRecipes.length}
          showFavorites={showFavorites}
          onToggleFavorites={() => setShowFavorites(!showFavorites)}
          sortMethod={sortMethod}
          onSortChange={setSortMethod}
          tags={tagsQuery.data ?? []}
          selectedTags={selectedTags}
          onTagsChange={setSelectedTags}
        />
      </div>

      <div className="mt-2">
        <RecipeList
          recipes={filteredRecipes}
          onDelete={(id) => deleteRecipe.mutate(id)}
          onToggleFavorite={(id) => toggleFavorite.mutate(id)}
          onTogglePinned={(id) => togglePin.mutate(id)}
          onCopy={(id, name) => copyRecipe.mutate({ id, name })}
        />
      </div>
    </div>
  );
}
