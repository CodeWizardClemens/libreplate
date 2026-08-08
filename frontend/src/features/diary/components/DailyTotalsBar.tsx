import { useState } from "react";

import type { DayMeal } from "@/api/generated";

import TotalsModal from "@/components/ui/NutrientsTotalsModal";

import { computeDailyTotals } from "../utils/computeDailyTotals";

type Props = {
  meals: DayMeal[];
};

export default function DailyTotalsBar({ meals }: Props) {
  const [isOpen, setIsOpen] = useState(false);

  const totals = computeDailyTotals(meals);

  return (
    <>
      <div
        className="card mb-2"
        onClick={() => setIsOpen(true)}
        style={{ cursor: "pointer" }}
      >
        <div className="card-body d-flex justify-content-between align-items-center">
          <h5 className="mb-0">Totals</h5>

          {/* TODO query these nutrients, don't hardcode them!!! */}
          <div className="d-flex gap-4 text-muted">
            <span>Kcal {totals.energy.toFixed(0)}</span>
            <span>P {totals.protein.toFixed(0)}</span>
            <span>F {totals.fat.toFixed(0)}</span>
            <span>C {totals.carbs.toFixed(0)}</span>
          </div>
        </div>
      </div>

      <TotalsModal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Daily Total"
        totals={totals}
      />
    </>
  );
}
