import { useEffect, useRef, useState } from "react";
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
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div
      ref={dropdownRef}
      className="dropdown position-relative ms-auto"
      onClick={(event) => event.stopPropagation()}
    >
      <button
        type="button"
        className="btn btn-sm border-0 bg-transparent p-1 text-dark"
        aria-label="Open food actions"
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen((previous) => !previous)}
      >
        <i className="bi bi-three-dots"></i>
      </button>

      {open && (
        <div
          className="dropdown-menu show text-end"
          role="menu"
          style={{
            minWidth: "max-content",
            right: "100%",
            left: "auto",
            top: 0,
            marginRight: "0.25rem",
          }}
        >
          <button
            type="button"
            className="dropdown-item text-end food-action-item"
            role="menuitem"
            onClick={() => {
              navigate(`/foods/${food.id}/edit`);
              setOpen(false);
            }}
          >
            Edit
          </button>

          <button
            type="button"
            className="dropdown-item text-end food-action-item"
            role="menuitem"
            onClick={() => {
              onToggleFavorite?.(food.id);
              setOpen(false);
            }}
          >
            {food.is_favorite ? "Favorited" : "Add favorite"}
          </button>

          <button
            type="button"
            className="dropdown-item text-danger text-end food-action-item"
            role="menuitem"
            onClick={() => {
              const confirmed = window.confirm(
                `Are you sure you want to delete "${food.name}"?`
              );

              if (confirmed) {
                onDelete?.(food.id);
              }

              setOpen(false);
            }}
          >
            Delete
          </button>
        </div>
      )}

      <style>
        {`
          .food-action-item:active,
          .food-action-item:focus {
            background-color: var(--bs-dropdown-link-hover-bg);
            color: var(--bs-dropdown-link-hover-color);
          }
        `}
      </style>
    </div>
  );
}