import { useState } from "react";
import { useDeleteMealFood } from "@/api/MealAPI";
import type { MealFood } from "@/types/MealTypes";
import EditMealFoodModal from "./EditMealFoodModal";

type Props = {
  item: MealFood;
};

export default function MealFoodItem({ item }: Props) {
  const deleteMealFood = useDeleteMealFood();

  const [isEditOpen, setIsEditOpen] = useState(false);

  return (
    <>
      <li
        className="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
        role="button"
        tabIndex={0}
        onClick={() => setIsEditOpen(true)}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            setIsEditOpen(true);
          }
        }}
        style={{ cursor: "pointer" }}
      >
        <span>{item.food.name}</span>

        <span className="d-flex align-items-center gap-3 text-muted">
          <span>
            {item.serving_size}g × {item.number_of_servings}
          </span>

          <button
            type="button"
            className="btn btn-sm btn-outline-danger border-0"
            onClick={(e) => {
              e.stopPropagation();
              deleteMealFood.mutate(item.id);
            }}
            disabled={deleteMealFood.isPending}
            aria-label={`Remove ${item.food.name}`}
            title="Remove"
          >
            <i className="bi bi-trash" aria-hidden="true"></i>
          </button>
        </span>
      </li>

      {isEditOpen && (
        <EditMealFoodModal
          item={item}
          onClose={() => setIsEditOpen(false)}
        />
      )}
    </>
  );
}