import { useState } from "react";
import type { Recipe } from "../../types";
import { useRecipes } from "../../api";

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
  const [servingsById, setServingsById] = useState<Record<number, string>>({});

  const { data: recipes, isLoading, isError } = useRecipes();

  if (!isOpen) {
    return null;
  }

  const filteredRecipes =
    recipes?.filter((recipe) =>
      recipe.name.toLowerCase().includes(search.toLowerCase()),
    ) ?? [];

  function reset() {
    setSearch("");
    setServingsById({});
  }

  function handleClose() {
    reset();
    onClose();
  }

  function getServings(recipeId: number) {
    return servingsById[recipeId] ?? "1";
  }

  function setServings(recipeId: number, value: string) {
    setServingsById((prev) => ({ ...prev, [recipeId]: value }));
  }

  function handleAdd(recipe: Recipe) {
    const parsed = parseFloat(getServings(recipe.id));
    const servings = Number.isNaN(parsed) || parsed <= 0 ? 1 : parsed;

    onSelect(recipe, servings);
    reset();
  }

  return (
    <div
      onClick={handleClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.4)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1050,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "white",
          padding: "20px",
          width: "460px",
          maxHeight: "80vh",
          borderRadius: "8px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <h2>Select recipe</h2>

        <input
          placeholder="Search recipes..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            width: "100%",
            marginBottom: "15px",
          }}
        />

        {isLoading && <p>Loading recipes...</p>}

        {isError && <p>Failed to load recipes.</p>}

        <div style={{ overflowY: "auto", flex: 1 }}>
          {filteredRecipes.map((recipe) => (
            <div
              key={recipe.id}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                width: "100%",
                padding: "6px 4px",
                marginBottom: "4px",
                borderRadius: "4px",
                gap: "8px",
              }}
            >
              <div style={{ minWidth: 0 }}>
                <div
                  style={{
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {recipe.name}
                </div>

                <div style={{ color: "#666", fontSize: "0.85em" }}>
                  {recipe.ingredients.length} ingredient
                  {recipe.ingredients.length === 1 ? "" : "s"}
                </div>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: "6px", flexShrink: 0 }}>
                <input
                  type="number"
                  min={0}
                  step="any"
                  value={getServings(recipe.id)}
                  onChange={(e) => setServings(recipe.id, e.target.value)}
                  style={{ width: "3.5rem", textAlign: "center" }}
                  aria-label={`Servings of ${recipe.name} to add`}
                />

                <span style={{ color: "#666", fontSize: "0.85em" }}>servings</span>

                <button onClick={() => handleAdd(recipe)}>Add</button>
              </div>
            </div>
          ))}

          {!isLoading && filteredRecipes.length === 0 && (
            <p style={{ color: "#666" }}>No recipes found.</p>
          )}
        </div>

        <div style={{ marginTop: "15px" }}>
          <button onClick={handleClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
}