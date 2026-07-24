import type { Recipe } from "../../types";

import {
  useRecipeTags,
  useUpdateRecipe,
} from "../../api";

interface Props {
  recipe: Recipe;
}

export default function RecipeCardTags({
  recipe,
}: Props) {
  const { data: availableTags = [] } = useRecipeTags();
  const updateRecipe = useUpdateRecipe();

  const unusedTags = availableTags.filter(
    (tag) =>
      !recipe.tags.some(
        (recipeTag) => recipeTag.id === tag.id,
      ),
  );

  function stopCardClick(
    event: React.MouseEvent,
  ) {
    event.stopPropagation();
  }

  function updateRecipeData(tagIds: number[]) {
    updateRecipe.mutate({
      id: recipe.id,
      data: {
        tag_ids: tagIds,
      },
    });
  }

  function addTag(tagId: number) {
    updateRecipeData([
      ...recipe.tags.map((tag) => tag.id),
      tagId,
    ]);
  }

  function removeTag(tagId: number) {
    updateRecipeData(
      recipe.tags
        .filter((tag) => tag.id !== tagId)
        .map((tag) => tag.id),
    );
  }

  return (
    <div
      className="
        d-flex
        flex-wrap
        align-items-center
        gap-2
      "
      onClick={stopCardClick}
    >
      {recipe.tags.map((tag) => (
        <span
          key={tag.id}
          className="
            badge
            text-bg-primary
            d-flex
            align-items-center
            gap-1
          "
        >
          {tag.name}

          <button
            type="button"
            className="
              btn
              btn-sm
              p-0
              text-white
              border-0
              lh-1
            "
            onClick={(event) => {
              stopCardClick(event);
              removeTag(tag.id);
            }}
            title="Remove tag"
          >
            <i className="bi bi-x" />
          </button>
        </span>
      ))}

      {unusedTags.length > 0 && (
        <div className="dropdown">
          <button
            className="
              btn
              btn-sm
              btn-outline-secondary
              d-flex
              align-items-center
              justify-content-center
              p-0
            "
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
            title="Add tag"
            onClick={stopCardClick}
          >
            <i className="bi bi-plus" />
          </button>

          <ul className="dropdown-menu">
            {unusedTags.map((tag) => (
              <li key={tag.id}>
                <button
                  className="dropdown-item"
                  type="button"
                  onClick={(event) => {
                    stopCardClick(event);
                    addTag(tag.id);
                  }}
                >
                  {tag.name}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}