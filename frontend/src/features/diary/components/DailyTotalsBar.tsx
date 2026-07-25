import type { DayMeal } from "@/types/MealTypes";
import { computeDailyTotals } from "../utils/computeDailyTotals";

type Props = {
  meals: DayMeal[];
};

export default function DailyTotalsBar({ meals }: Props) {
  const totals = computeDailyTotals(meals);

  return (
    <div className="card mb-3">
      <div className="card-body d-flex justify-content-between align-items-center">
        <h5 className="mb-0">Daily Total</h5>

        <div className="d-flex gap-4 text-muted">
          <span>Kcal {totals.energy.toFixed(0)}</span>
          <span>P {totals.protein.toFixed(0)}</span>
          <span>F {totals.fat.toFixed(0)}</span>
          <span>C {totals.carbs.toFixed(0)}</span>
        </div>
      </div>
    </div>
  );
}
