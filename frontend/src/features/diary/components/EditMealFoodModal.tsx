import { useMemo, useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { mealsMealFoodsPartialUpdate } from "@/api/generated";
import type { MealFood } from "@/api/generated";

import Modal from "@/components/ui/Modal";

type Props = {
  item: MealFood;
  onClose: () => void;
  onSaved: () => Promise<void>;
};

type NutrientTotals = {
  energy: number;
  protein: number;
  fat: number;
  carbs: number;
};

function computeItemNutrients(
  item: MealFood,
  servingSize: number,
  numberOfServings: number,
): NutrientTotals {
  const totals: NutrientTotals = {
    energy: 0,
    protein: 0,
    fat: 0,
    carbs: 0,
  };

  const multiplier = (servingSize * numberOfServings) / 100;

  for (const nutrient of item.food?.nutrients ?? []) {
    const amount = (nutrient.amount ?? 0) * multiplier;

    switch (nutrient.nutrient_name?.toLowerCase()) {
      case "energy":
      case "calories":
      case "kcal":
        totals.energy += amount;
        break;

      case "protein":
        totals.protein += amount;
        break;

      case "fat":
      case "total lipid (fat)":
        totals.fat += amount;
        break;

      case "carbohydrates":
      case "carbs":
      case "carbohydrate, by difference":
        totals.carbs += amount;
        break;
    }
  }

  return totals;
}

function formatAmount(value: number) {
  return Number.isFinite(value) ? value.toFixed(0) : "—";
}

export default function EditMealFoodModal({ item, onClose, onSaved }: Props) {
  const [servingSize, setServingSize] = useState(
    String(item.serving_size ?? 0),
  );

  const [servings, setServings] = useState(
    String(item.number_of_servings ?? 0),
  );

  const parsedSize = Number.parseFloat(servingSize);
  const parsedServings = Number.parseFloat(servings);

  const hasValidInputs =
    !Number.isNaN(parsedSize) &&
    !Number.isNaN(parsedServings) &&
    parsedSize > 0 &&
    parsedServings > 0;

  const nutrients = useMemo(() => {
    if (!hasValidInputs) {
      return computeItemNutrients(item, 0, 0);
    }

    return computeItemNutrients(item, parsedSize, parsedServings);
  }, [item, parsedSize, parsedServings, hasValidInputs]);

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
    if (!hasValidInputs) {
      return;
    }

    await updateMealFood.mutateAsync({
      id: item.id,
      serving_size: parsedSize,
      number_of_servings: parsedServings,
    });

    await onSaved();
    onClose();
  }

  return (
    <Modal
      isOpen
      title={`${item.food.name}`}
      onClose={onClose}
      footer={
        <div className="d-flex justify-content-end gap-2">
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>

          <button
            type="button"
            className="btn btn-primary"
            onClick={() => void handleSave()}
            disabled={updateMealFood.isPending || !hasValidInputs}
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
            onChange={(event) => setServingSize(event.target.value)}
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
            onChange={(event) => setServings(event.target.value)}
          />
        </div>

        <div className="border rounded p-3 bg-light">
          <div className="fw-semibold mb-2">Nutrients</div>

          {/* TODO don't hardcode nutrients, query them from backend. */}
          <div className="d-flex flex-column gap-1 small">
            <div className="d-flex justify-content-between">
              <span>Energy (kcals)</span>
              <span>{formatAmount(nutrients.energy)}</span>
            </div>

            <div className="d-flex justify-content-between">
              <span>Protein (g)</span>
              <span>{formatAmount(nutrients.protein)}</span>
            </div>

            <div className="d-flex justify-content-between">
              <span>Fat (g)</span>
              <span>{formatAmount(nutrients.fat)}</span>
            </div>

            <div className="d-flex justify-content-between">
              <span>Carbohydrates (g)</span>
              <span>{formatAmount(nutrients.carbs)}</span>
            </div>
          </div>

          {!hasValidInputs && (
            <div className="text-danger small mt-2">
              Enter a valid serving size and number of servings to see
              nutrients.
            </div>
          )}
        </div>
      </div>
    </Modal>
  );
}
