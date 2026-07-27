import FoodCard from "./FoodCard";

import type { Food } from "@/api/generated";

interface Props {
  foods: Food[];

  onDelete?: (id: number) => void;

  onToggleFavorite?: (id: number) => void;
}

export default function FoodList({ foods, onDelete, onToggleFavorite }: Props) {
  return (
    <div className="d-flex flex-column gap-3">
      {foods.map((food) => (
        <FoodCard
          key={food.id}

          food={food}

          onDelete={onDelete}

          onToggleFavorite={onToggleFavorite}
        />
      ))}
    </div>
  );
}
