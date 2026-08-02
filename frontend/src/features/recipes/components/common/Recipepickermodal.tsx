import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import type { Recipe } from "@/api/generated/types.gen";
import { recipesList } from "@/api/generated";

interface RecipePickerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (recipe: Recipe, servings: number) => void;
}

export default function RecipePickerModal({
  isOpen,
  onClose,
  onSelect,
}: RecipePickerModalProps) {
  const [search, setSearch] = useState("");

  const {
    data: recipesResponse,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["recipes"],
    queryFn: () => recipesList(),
  });

  const recipes = recipesResponse?.data ?? [];

  if (!isOpen) {
    return null;
  }

  const filteredRecipes = recipes.filter((recipe) =>
    recipe.name.toLowerCase().includes(search.toLowerCase()),
  );

  function reset() {
    setSearch("");
  }

  function handleClose() {
    reset();
    onClose();
  }

  function handleAdd(recipe: Recipe) {
    onSelect(recipe, 1);
    reset();
  }

  return (
    <div
      onClick={handleClose}
      className="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center"
      style={{
        background: "rgba(0,0,0,0.4)",
        zIndex: 1050,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-white p-4 rounded-4 shadow-lg d-flex flex-column"
        style={{
          width: "460px",
          maxHeight: "80vh",
        }}
      >
        <h2 className="mb-3">Select recipe</h2>

        <div className="mb-3">
          <input
            type="text"
            className="form-control rounded-2"
            placeholder="Search recipes..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {isError && <p className="text-danger">Failed to load recipes.</p>}

        <div
          className="list-group overflow-auto flex-grow-1"
          style={{
            minHeight: 0,
          }}
        >
          {filteredRecipes.map((recipe) => (
            <button
              key={recipe.id}
              type="button"
              className="list-group-item list-group-item-action d-flex align-items-center"
              onClick={() => handleAdd(recipe)}
              style={{
                textAlign: "left",
              }}
            >
              <div
                className="text-truncate"
                style={{
                  maxWidth: "38ch",
                }}
              >
                {recipe.name}
              </div>
            </button>
          ))}

          {!isLoading && filteredRecipes.length === 0 && (
            <p className="text-muted mt-3">No recipes found.</p>
          )}
        </div>

        <div className="mt-3 d-flex justify-content-end">
          <button className="btn btn-secondary" onClick={handleClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
