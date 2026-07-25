import type { DayMeal } from "../types";

import MealFoodItem from "./MealFoodItem";

type Props = {
  meals: DayMeal[];
  onAddFood: (meal: DayMeal) => void;
  onAddRecipe: (meal: DayMeal) => void;
};

export default function MealList({ meals, onAddFood, onAddRecipe }: Props) {
  return (
    <div className="row g-3">
      {meals.map((meal) => (
        <div key={meal.default_meal.id} className="col-12">
          <div className="card shadow-sm">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h2 className="h5 mb-1">{meal.name}</h2>

                  {meal.meal_id === null && (
                    <span className="badge bg-light text-dark">Empty</span>
                  )}
                </div>

                <div className="d-flex gap-2">
                  <button
                    className="btn btn-sm btn-outline-primary"
                    onClick={() => onAddRecipe(meal)}
                  >
                    + Add recipe
                  </button>

                  <button
                    className="btn btn-sm btn-primary"
                    onClick={() => onAddFood(meal)}
                  >
                    + Add food
                  </button>
                </div>
              </div>

              {meal.meal_foods.length === 0 ? (
                <div className="text-muted">No foods added.</div>
              ) : (
                <ul className="list-group list-group-flush">
                  {meal.meal_foods.map((item) => (
                    <MealFoodItem key={item.id} item={item} />
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}