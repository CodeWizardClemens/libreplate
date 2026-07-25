import type { DayMeal } from "../types";

type Props = {
  meals: DayMeal[];
  onAddFood: (meal: DayMeal) => void;
};

export default function MealList({
  meals,
  onAddFood,
}: Props) {
  return (
    <div className="row g-3">
      {meals.map((meal) => (
        <div
          key={meal.default_meal.id}
          className="col-12"
        >
          <div className="card shadow-sm">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h2 className="h5 mb-1">
                    {meal.name}
                  </h2>

                  {meal.meal_id === null && (
                    <span className="badge bg-light text-dark">
                      Empty
                    </span>
                  )}
                </div>

                <button
                  className="btn btn-sm btn-primary"
                  onClick={() => onAddFood(meal)}
                >
                  + Add food
                </button>
              </div>

              {meal.meal_foods.length === 0 ? (
                <div className="text-muted">
                  No foods added.
                </div>
              ) : (
                <ul className="list-group list-group-flush">
                  {meal.meal_foods.map((item) => (
                    <li
                      key={item.id}
                      className="list-group-item d-flex justify-content-between px-0"
                    >
                      <span>
                        {item.food.name}
                      </span>

                      <span className="text-muted">
                        {item.number_of_servings}
                        {" × "}
                        {item.serving_size}
                      </span>
                    </li>
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