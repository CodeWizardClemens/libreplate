import { useState } from "react";

import type { DayMeal } from "@/api/generated";

import MealFoodItem from "./MealFoodItem";

import { computeMealTotals } from "@/features/diary/utils/MealFormulas";

type Props = {
  meals: DayMeal[];
  onAdd: (meal: DayMeal) => void;
  onDiaryChanged: () => Promise<void>;
};

export default function MealList({ meals, onAdd, onDiaryChanged }: Props) {
  return (
    <div className="row g-3">
      {meals.map((meal) => (
        <MealCard
          key={meal.default_meal.id}
          meal={meal}
          onAdd={onAdd}
          onDiaryChanged={onDiaryChanged}
        />
      ))}
    </div>
  );
}

function MealCard({
  meal,
  onAdd,
  onDiaryChanged,
}: {
  meal: DayMeal;
  onAdd: (meal: DayMeal) => void;
  onDiaryChanged: () => Promise<void>;
}) {
  const [open, setOpen] = useState(true);

  const mealFoods = meal.meal_foods ?? [];
  const totals = computeMealTotals(mealFoods);

  return (
    <div className="col-12">
      <div className="card">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-start mb-1">
            <div className="d-flex align-items-center gap-2">
              <button
                type="button"
                className="btn btn-sm btn-light"
                onClick={() => setOpen((current) => !current)}
              >
                <i
                  className={`bi ${
                    open ? "bi-chevron-down" : "bi-chevron-right"
                  }`}
                />
              </button>

              <div>
                <h2 className="h5 mb-1">{meal.name}</h2>

                <div className="small text-muted d-flex gap-3">
                  <span>Kcal {totals.energy.toFixed(0)}</span>
                  <span>P {totals.protein.toFixed(0)}</span>
                  <span>F {totals.fat.toFixed(0)}</span>
                  <span>C {totals.carbs.toFixed(0)}</span>
                </div>
              </div>
            </div>

            <button
              type="button"
              className="btn btn-sm btn-primary"
              onClick={() => onAdd(meal)}
              aria-label="Add to meal"
            >
              <i className="bi bi-plus-lg" />
            </button>
          </div>

          <div className={`collapse ${open ? "show" : ""}`}>
            {mealFoods.length > 0 && (
              <ul className="list-group list-group-flush">
                {mealFoods.map((item) => (
                  <MealFoodItem
                    key={item.id}
                    item={item}
                    onDiaryChanged={onDiaryChanged}
                  />
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
