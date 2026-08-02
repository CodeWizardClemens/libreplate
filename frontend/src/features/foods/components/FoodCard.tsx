import { useNavigate } from "react-router-dom";
import type { Food } from "@/api/generated";

import FoodCardActions from "./FoodCardActions";
import FoodCardNutrients from "./FoodCardNutrients.tsx";

interface Props {
  food: Food;
  onDelete?: (id: number) => void;
  onToggleFavorite?: (id: number) => void;
}

export default function FoodCard({ food, onDelete, onToggleFavorite }: Props) {
  const navigate = useNavigate();

  if (!food) {
    return null;
  }

  return (
    <div
      className="card shadow-sm rounded-2"
      role="button"
      onClick={() => navigate(`/foods/${food.id}/edit`)}
    >
      <div className="card-body p-2">
        <div className="d-flex align-items-start">
          <div className="flex-grow-1">
            <h5 className="card-title mb-0">{food.name}</h5>
          </div>

          <div className="ms-2" onClick={(e) => e.stopPropagation()}>
            <FoodCardActions
              food={food}
              onDelete={onDelete}
              onToggleFavorite={onToggleFavorite}
            />
          </div>
        </div>

        <p className="card-text mb-0 text-muted">{food.brand || "No brand"}</p>

        <div className="text-muted small mt-0">
          {food.serving != null && (
            <>
              {food.serving} {food.unit_name}
              <span className="mx-1">•</span>
              <FoodCardNutrients nutrients={food.nutrients} />
            </>
          )}
        </div>
      </div>
    </div>
  );
}
