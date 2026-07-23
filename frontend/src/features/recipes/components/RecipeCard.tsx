import { useState } from "react";

import type { Recipe } from "../types";

import { useRecipeTags, useUpdateRecipe } from "../api";

import RecipeCardActions from "./RecipeCardActions";
import RecipeCardHeader from "./RecipeCardHeader";
import RecipeCardNutrients from "./RecipeCardNutrients";
import RecipeCardTags from "./RecipeCardTags";
import RecipeCardPicture from "./RecipeCardPicture";

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
  const { data: availableTags = [] } = useRecipeTags();

  const updateRecipe = useUpdateRecipe();

  const [editingName, setEditingName] = useState(false);

  const [editingSummary, setEditingSummary] = useState(false);

  if (!recipe) {
    return null;
  }

  function updateRecipeData(data: { name?: string; summary?: string; tag_ids?: number[] }) {
    updateRecipe.mutate({
      id: recipe.id,

      data,
    });
  }

  function handleCopy() {
    const name = window.prompt("New recipe name:", `${recipe.name} Copy`);

    if (name) {
      onCopy?.(recipe.id, name);
    }
  }

  return (
    <div
      className="
                card
                shadow-sm
            "
    >
      <div
        className="
                    card-body
                "
      >
        <div
          className="
    row
    g-3
    align-items-start
  "
        >
          <div
            className="
      col-auto
      order-1
    "
          >
            <RecipeCardPicture recipeId={recipe.id} />
          </div>

          <RecipeCardActions
            recipe={recipe}

            onCopy={handleCopy}

            onDelete={onDelete}

            onToggleFavorite={onToggleFavorite}

            onTogglePinned={onTogglePinned}
          />

          <div
            className="
      col
      order-2
    "
          >
            <RecipeCardHeader
              recipe={recipe}

              update={updateRecipeData}

              editingName={editingName}

              setEditingName={setEditingName}

              editingSummary={editingSummary}

              setEditingSummary={setEditingSummary}
            />

            <RecipeCardNutrients nutrients={recipe.nutrients} />

            <RecipeCardTags
              recipe={recipe}

              availableTags={availableTags}

              update={updateRecipeData}
            />

            <div
              className="
                                text-muted
                                small
                                mt-3
                            "
            >
              {recipe.portions}

              {" portions • "}

              {recipe.cooking_time}

              {" min"}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
