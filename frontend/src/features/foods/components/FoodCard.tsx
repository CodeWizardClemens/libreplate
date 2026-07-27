import { useState } from "react";

import type { Food } from "@/api/generated";
import { foodsPartialUpdate } from "@/api/generated";

import FoodCardActions from "./FoodCardActions";
import FoodCardHeader from "./FoodCardHeader";
import FoodCardNutrients from "./FoodCardNutrients";

interface Props {
  food: Food;

  onDelete?: (id: number) => void;
  onToggleFavorite?: (id: number) => void;
}

export default function FoodCard({ food, onDelete, onToggleFavorite }: Props) {
  const [editingName, setEditingName] = useState(false);
  const [editingDescription, setEditingDescription] = useState(false);

  if (!food) {
    return null;
  }

  async function updateFoodData(data: {
    name?: string;
    description?: string;
  }) {
    await foodsPartialUpdate({
      path: {
        id: food.id,
      },
      body: data,
    });
  }

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <div className="row g-3 align-items-start">
          <div className="col-auto order-2 ms-auto">
            <FoodCardActions
              food={food}
              onDelete={onDelete}
              onToggleFavorite={onToggleFavorite}
            />
          </div>

          <div className="col order-1">
            <FoodCardHeader
              food={food}
              update={updateFoodData}
              editingName={editingName}
              setEditingName={setEditingName}
              editingDescription={editingDescription}
              setEditingDescription={setEditingDescription}
            />

            <FoodCardNutrients nutrients={food.nutrients} />

            <div className="text-muted small mt-3">
              {food.brand && (
                <>
                  <i className="bi bi-tag me-1"></i>
                  {food.brand}
                </>
              )}

              {food.serving != null && (
                <>
                  {food.serving} {food.unit_name}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}