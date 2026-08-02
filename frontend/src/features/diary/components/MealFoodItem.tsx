import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { mealsMealFoodsDestroy } from "@/api/generated";

import type { MealFood } from "@/api/generated";

import EditMealFoodModal from "./EditMealFoodModal";

type Props = {
  item: MealFood;
};

export default function MealFoodItem({ item }: Props) {
  const [isEditOpen, setIsEditOpen] = useState(false);

  const deleteMealFood = useMutation({
    mutationFn: async (id: number) => {
      await mealsMealFoodsDestroy({
        path: {
          id,
        },
      });
    },
  });

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
            {item.serving_size ?? 0}g × {item.number_of_servings ?? 0}
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
            <i className="bi bi-trash" aria-hidden="true" />
          </button>
        </span>
      </li>

      {isEditOpen && (
        <EditMealFoodModal item={item} onClose={() => setIsEditOpen(false)} />
      )}
    </>
  );
}
