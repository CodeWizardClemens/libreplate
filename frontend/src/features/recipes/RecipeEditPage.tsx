import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  useRecipe,
  useRecipeIngredients,
  useRecipeTags,
} from "./api";

import BackButton from "./components/edit/BackButton";
import RecipeInfoBar from "./components/edit/RecipeInfoBar";
import InstructionsCard from "./components/edit/InstructionsCard";
import IngredientsCard from "./components/edit/IngredientsCard";
import RecipeCardPicture from "./components/common/RecipePicture";
import TagModal from "./components/common/TagModal";
import RecipeCardTags from "./components/common/RecipeTags"
import TitleInfo from "./components/edit/TitleInfo";

export default function RecipeEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const recipeId = Number(id);

  const { data: recipe, isLoading } = useRecipe(recipeId);
  const { data: ingredients } = useRecipeIngredients(recipeId);
  const { data: tags } = useRecipeTags();

  const [showTagModal, setShowTagModal] = useState(false);

  if (isLoading || !recipe) {
    return (
      <div className="container py-4">
        Loading...
      </div>
    );
  }

  return (
    <div className="container">
      <div
        className="mx-auto"
        style={{
          maxWidth: "550px",
        }}
      >
        <div className="mb-3">
          <BackButton
            onClick={() => navigate("/recipes")}
          />
        </div>

        <TitleInfo recipe={recipe} />

        <div className="d-flex justify-content-center align-items-center py-2">
          <RecipeCardPicture
            recipeId={recipe.id}
            width={550}
            height={350}
          />
        </div>

        <div className="d-flex justify-content-center mb-2">
          <RecipeInfoBar recipe={recipe} />
        </div>

        <div className="d-flex justify-content-center mb-2">
          <button
            className="btn btn-outline-secondary btn-sm m-1"
            onClick={() => setShowTagModal(true)}
          >
            Tags
          </button>
          <RecipeCardTags recipe={recipe} />
        </div>
      </div>

      <InstructionsCard recipe={recipe} />

      <IngredientsCard ingredients={ingredients} />

      {tags && (
        <TagModal
          open={showTagModal}
          onClose={() => setShowTagModal(false)}
          tags={tags}
        />
      )}
    </div>
  );
}