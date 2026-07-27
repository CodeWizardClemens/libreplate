import { useNavigate } from "react-router-dom";

import type { Food } from "@/api/generated";

interface Props {
  food: Food;
  onDelete?: (id: number) => void;
  onToggleFavorite?: (id: number) => void;
}

export default function FoodCardActions({
  food,
  onDelete,
  onToggleFavorite,
}: Props) {
  const navigate = useNavigate();

  const stopCardClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
  };

  const handleDelete = () => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${food.name}"? This cannot be undone.`,
    );

    if (confirmed) {
      onDelete?.(food.id);
    }
  };

  const actions = (
    <>
      <button
        className={
          food.is_favorite ? "btn btn-primary" : "btn btn-outline-secondary"
        }
        onClick={(e) => {
          stopCardClick(e);
          onToggleFavorite?.(food.id);
        }}
        title="Favorite"
      >
        <i className={food.is_favorite ? "bi bi-heart-fill" : "bi bi-heart"} />
      </button>

      <button
        className="btn btn-outline-secondary"
        onClick={(e) => {
          stopCardClick(e);
          navigate(`/foods/${food.id}/edit`);
        }}
        title="Edit"
      >
        <i className="bi bi-pencil" />
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
