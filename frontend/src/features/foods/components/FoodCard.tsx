import { useState } from "react";

import type { Food } from "@/types/FoodTypes";

import { useUpdateFood } from "@/api/FoodAPI";

import FoodCardActions from "./FoodCardActions";
import FoodCardHeader from "./FoodCardHeader";
import FoodCardNutrients from "./FoodCardNutrients";

interface Props {
  food: Food;

  onDelete?: (id: number) => void;
  onToggleFavorite?: (id: number) => void;
}

export default function FoodCard({ food, onDelete, onToggleFavorite }: Props) {
  const updateFood = useUpdateFood();

  const [editingName, setEditingName] = useState(false);
  const [editingDescription, setEditingDescription] = useState(false);

  if (!food) {
    return null;
  }

  function updateFoodData(data: { name?: string; description?: string }) {
    updateFood.mutate({
      id: food.id,
      data,
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
                  <i className="bi bi-egg-fried ms-2 me-1"></i>
                  {food.serving} {food.unit}
                </>
              )}

              {food.barcode && (
                <>
                  <i className="bi bi-upc-scan ms-2 me-1"></i>
                  {food.barcode}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
