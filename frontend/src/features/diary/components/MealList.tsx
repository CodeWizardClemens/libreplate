import { useState } from "react";
import type { DayMeal } from "@/types/MealTypes";
import MealFoodItem from "./MealFoodItem";
import { computeMealTotals } from "@/features/diary/utils/MealFormulas";

type Props = {
  meals: DayMeal[];
  onAddFood: (meal: DayMeal) => void;
  onAddRecipe: (meal: DayMeal) => void;
};

export default function MealList({ meals, onAddFood, onAddRecipe }: Props) {
  return (
    <div className="row g-3">
      {meals.map((meal) => (
        <MealCard
          key={meal.default_meal.id}
          meal={meal}
          onAddFood={onAddFood}
          onAddRecipe={onAddRecipe}
        />
      ))}
    </div>
  );
}

function MealCard({
  meal,
  onAddFood,
  onAddRecipe,
}) {
  const [open, setOpen] = useState(true);

  const totals = computeMealTotals(meal.meal_foods);

  return (
    <div className="col-12">
      <div className="card shadow-sm">
        <div className="card-body">

          {/* Header */}
          <div className="d-flex justify-content-between align-items-start mb-3">

            <div className="d-flex align-items-center gap-2">
              <button
                className="btn btn-sm btn-light"
                onClick={() => setOpen(o => !o)}
              >
                <i className={`bi ${open ? "bi-chevron-down" : "bi-chevron-right"}`} />
              </button>

              <div>
                <h2 className="h5 mb-1">{meal.name}</h2>

                <div className="small text-muted d-flex gap-3">
                  <span>Kcal {totals.energy.toFixed(0)}</span>
                  <span>P {totals.protein.toFixed(0)}</span>
                  <span>F {totals.fat.toFixed(0)}</span>
                  <span>C {totals.carbs.toFixed(0)}</span>
                </div>

                {meal.meal_id === null && (
                  <span className="badge bg-light text-dark">Empty</span>
                )}
              </div>
            </div>

            <div className="d-flex gap-2">
              <button
                className="btn btn-sm btn-primary"
                onClick={() => onAddRecipe(meal)}
              >
                + Recipe
              </button>

              <button
                className="btn btn-sm btn-primary"
                onClick={() => onAddFood(meal)}
              >
                + Food
              </button>
            </div>
          </div>

          {/* Collapsible content */}
          <div className={`collapse ${open ? "show" : ""}`}>
            {meal.meal_foods.length === 0 ? (
              <div className="text-muted">No foods added.</div>
            ) : (
              <ul className="list-group list-group-flush">
                {meal.meal_foods.map(item => (
                  <MealFoodItem key={item.id} item={item} />
                ))}
              </ul>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}