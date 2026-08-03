import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { mealsMealFoodsPartialUpdate } from "@/api/generated";
import type { MealFood } from "@/api/generated";

import Modal from "@/components/ui/Modal";

type Props = {
  item: MealFood;
  onClose: () => void;
};

export default function EditMealFoodModal({ item, onClose }: Props) {
  const [servingSize, setServingSize] = useState(
    String(item.serving_size ?? 0),
  );

  const [servings, setServings] = useState(
    String(item.number_of_servings ?? 0),
  );

  const updateMealFood = useMutation({
    mutationFn: async ({
      id,
      serving_size,
      number_of_servings,
    }: {
      id: number;
      serving_size: number;
      number_of_servings: number;
    }) => {
      const response = await mealsMealFoodsPartialUpdate({
        path: {
          id,
        },
        body: {
          serving_size,
          number_of_servings,
        },
      });

      return response.data;
    },
  });

  async function handleSave() {
    const parsedSize = parseFloat(servingSize);
    const parsedServings = parseFloat(servings);

    if (
      Number.isNaN(parsedSize) ||
      Number.isNaN(parsedServings) ||
      parsedSize <= 0 ||
      parsedServings <= 0
    ) {
      return;
    }

    await updateMealFood.mutateAsync({
      id: item.id,
      serving_size: parsedSize,
      number_of_servings: parsedServings,
    });

    onClose();
  }

  return (
    <Modal
      isOpen={true}
      title={`Edit ${item.food.name}`}
      onClose={onClose}
      footer={
        <div className="d-flex justify-content-end gap-2">
          <button className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>

          <button
            className="btn btn-primary"
            onClick={handleSave}
            disabled={updateMealFood.isPending}
          >
            Save
          </button>
        </div>
      }
    >
      <div className="d-flex flex-column gap-3">
        <div>
          <label className="form-label">Serving size (g)</label>

          <input
            type="number"
            min={0}
            step="any"
            className="form-control"
            value={servingSize}
            onChange={(e) => setServingSize(e.target.value)}
          />
        </div>

        <div>
          <label className="form-label">Number of servings</label>

          <input
            type="number"
            min={0}
            step="any"
            className="form-control"
            value={servings}
            onChange={(e) => setServings(e.target.value)}
          />
        </div>
      </div>
    </Modal>
  );
}
