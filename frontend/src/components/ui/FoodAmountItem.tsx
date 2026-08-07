import { useState } from "react";

import type { Food } from "@/api/generated";
import EditFoodAmountsModal from "@/components/ui/EditFoodAmountsModal";

type Props = {
  item: {
    id: number;
    food: Food;
    serving_size?: number | null;
    number_of_servings?: number | null;
  };
  onSave: (values: {
    id: number;
    serving_size: number;
    number_of_servings: number;
  }) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
};

export default function FoodItem({ item, onSave, onDelete }: Props) {
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  async function handleDelete() {
    setIsDeleting(true);

    try {
      await onDelete(item.id);
    } finally {
      setIsDeleting(false);
    }
  }

  return (
    <>
      <li
        className="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
        role="button"
        tabIndex={0}
        onClick={() => setIsEditOpen(true)}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            setIsEditOpen(true);
          }
        }}
        style={{ cursor: "pointer" }}
      >
        {item.food.name}

        <span className="d-flex align-items-center gap-3 text-muted">
          <span>
            {item.serving_size ?? 0}g × {item.number_of_servings ?? 0}
          </span>

          <button
            type="button"
            className="btn btn-sm btn-outline-danger border-0"
            onClick={(event) => {
              event.stopPropagation();
              void handleDelete();
            }}
            disabled={isDeleting}
            aria-label={`Remove ${item.food.name}`}
            title="Remove"
          >
            <i className="bi bi-trash" aria-hidden="true" />
          </button>
        </span>
      </li>

      {isEditOpen && (
        <EditFoodAmountsModal
          food={item.food}
          servingSize={item.serving_size ?? 0}
          numberOfServings={item.number_of_servings ?? 0}
          onClose={() => setIsEditOpen(false)}
          onSave={async (values) => {
            await onSave({
              id: item.id,
              ...values,
            });
          }}
        />
      )}
    </>
  );
}
