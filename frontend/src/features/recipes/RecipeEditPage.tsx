import { useNavigate, useParams } from "react-router-dom";

import {
  useRecipe,
  useRecipeIngredients,
  useRecipePicture,
} from "./api";

import BackButton from "./components/edit/BackButton";
import RecipeHeaderCard from "./components/edit/RecipeHeaderCard";
import InstructionsCard from "./components/edit/InstructionsCard";
import IngredientsCard from "./components/edit/IngredientsCard";
import RecipeCardPicture from "./components/common/RecipeCardPicture";

export default function RecipeEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const recipeId = Number(id);

  const { data: recipe, isLoading } = useRecipe(recipeId);
  const { data: picture } = useRecipePicture(recipeId);
  const { data: ingredients } = useRecipeIngredients(recipeId);

  if (isLoading || !recipe) {
    return <div className="container py-4">Loading...</div>;
  }

  return (
    <div className="container">
      <div className="mx-auto" style={{ maxWidth: "550px" }}>
        <div className="mb-3">
          <BackButton onClick={() => navigate("/recipes")} />
        </div>

        <div className="text-center">
          <h1 className="display-5 text-break mb-2">
            {recipe.name}
          </h1>

          <hr className="mt-0" />

          <p className="text-muted mb-0">
            {recipe.summary}
          </p>
        </div>

        <div className="d-flex justify-content-center align-items-center py-4">
          <RecipeCardPicture
            recipeId={recipe.id}
            width={550}
            height={350}
          />
        </div>
      </div>
      <RecipeHeaderCard recipe={recipe} picture={picture} />

        <div className="text-center mb-4">
          <strong>Tags:</strong>{" "}
          {recipe?.tags?.map((tag: any) => (
            <span
              key={tag.name}
              className="badge bg-secondary me-1"
            >
              {tag.name}
            </span>
          ))}
        </div>


      <InstructionsCard recipe={recipe} />

      <IngredientsCard ingredients={ingredients} />
    </div>
  );
}