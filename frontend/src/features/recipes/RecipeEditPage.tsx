import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import type { RecipeTag } from "@/api/generated/types.gen";
import { recipesRetrieve, recipesTagsList } from "@/api/generated";

import RecipeDetailsForm from "./components/edit/RecipeDetailsForm";
import IngredientsCard from "./components/edit/IngredientsCard";
import TagModal from "./components/common/TagModal";
import RecipeCardTags from "./components/common/RecipeTags";

export default function RecipeEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const recipeId = Number(id);

  const [showTagModal, setShowTagModal] = useState(false);

  const { data: recipeResponse, isLoading } = useQuery({
    queryKey: ["recipe", recipeId],
    queryFn: () =>
      recipesRetrieve({
        path: {
          id: recipeId,
        },
      }),
    enabled: Number.isFinite(recipeId),
  });

  const { data: tagsResponse } = useQuery({
    queryKey: ["recipe-tags"],
    queryFn: () => recipesTagsList(),
  });

  const recipe = recipeResponse?.data;

  const tags: RecipeTag[] = Array.isArray(tagsResponse)
    ? tagsResponse
    : Array.isArray(tagsResponse?.data)
      ? tagsResponse.data
      : [];

  if (isLoading || !recipe) {
    return <div className="container py-4">Loading...</div>;
  }

  return (
    <div className="container">
      <div>
        <div className="mb-2">
          <button
            className="btn btn-outline-secondary"
            onClick={() => navigate(-1)}
          >
            <i className="bi bi-arrow-left me-2" />
            Back
          </button>
        </div>

        <RecipeDetailsForm recipe={recipe} />

        <div className="d-flex align-items-center gap-2">
          <button
            className="btn btn-outline-secondary btn-sm"
            onClick={() => setShowTagModal(true)}
          >
            <i className="bi bi-tags" />
          </button>

          <RecipeCardTags recipe={recipe} />
        </div>
      </div>

      <IngredientsCard recipe={recipe} />

      {tags.length > 0 && (
        <TagModal
          open={showTagModal}
          onClose={() => setShowTagModal(false)}
          tags={tags}
        />
      )}
    </div>
  );
}
