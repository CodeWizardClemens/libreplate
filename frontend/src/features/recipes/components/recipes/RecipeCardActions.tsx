import { useNavigate } from "react-router-dom";

import type { Recipe } from "../../types";

interface Props {
  recipe: Recipe;
  onCopy: () => void;
  onDelete?: (id: number) => void;
  onToggleFavorite?: (id: number) => void;
  onTogglePinned?: (id: number) => void;
}

export default function RecipeCardActions({
  recipe,
  onCopy,
  onDelete,
  onToggleFavorite,
  onTogglePinned,
}: Props) {
  const navigate = useNavigate();

  const stopCardClick = (
    e: React.MouseEvent<HTMLButtonElement>
  ) => {
    e.stopPropagation();
  };

  const handleDelete = () => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${recipe.name}"? This cannot be undone.`,
    );

    if (confirmed) {
      onDelete?.(recipe.id);
    }
  };

  const actions = (
    <>
      <button
        className={
          recipe.is_pinned
            ? "btn btn-primary"
            : "btn btn-outline-secondary"
        }
        onClick={(e) => {
          stopCardClick(e);
          onTogglePinned?.(recipe.id);
        }}
        title="Pin"
      >
        <i
          className={
            recipe.is_pinned
              ? "bi bi-pin-fill"
              : "bi bi-pin"
          }
        />
      </button>

      <button
        className={
          recipe.is_favorite
            ? "btn btn-primary"
            : "btn btn-outline-secondary"
        }
        onClick={(e) => {
          stopCardClick(e);
          onToggleFavorite?.(recipe.id);
        }}
        title="Favorite"
      >
        <i
          className={
            recipe.is_favorite
              ? "bi bi-heart-fill"
              : "bi bi-heart"
          }
        />
      </button>

      <button
        className="btn btn-outline-secondary"
        onClick={(e) => {
          stopCardClick(e);
          navigate(`/recipes/${recipe.id}/edit`);
        }}
        title="Edit"
      >
        <i className="bi bi-pencil" />
      </button>

      <button
        className="btn btn-outline-secondary"
        onClick={(e) => {
          stopCardClick(e);
          onCopy();
        }}
        title="Copy"
      >
        <i className="bi bi-copy" />
      </button>

      <button
        className="btn btn-outline-secondary"
        onClick={(e) => {
          stopCardClick(e);
          handleDelete();
        }}
        title="Delete"
      >
        <i className="bi bi-trash" />
      </button>
    </>
  );

  return (
    <>
      {/* Desktop */}
      <div
        className="col-12 col-md-auto d-none d-md-flex gap-2 order-3"
        onClick={(e) => e.stopPropagation()}
      >
        {actions}
      </div>

      {/* Mobile */}
      <div
        className="d-flex d-md-none justify-content-end gap-2 mt-3 order-3 flex-wrap"
        onClick={(e) => e.stopPropagation()}
      >
        {actions}
      </div>
    </>
  );
}