import { useEffect, useRef, useState } from "react";

import { useDeleteMealFood, useUpdateMealFood } from "../api";

import type { MealFood } from "../types";

type Props = {
  item: MealFood;
};

const DEBOUNCE_MS = 600;

export default function MealFoodItem({ item }: Props) {
  const updateMealFood = useUpdateMealFood();
  const deleteMealFood = useDeleteMealFood();

  const [numberOfServings, setNumberOfServings] = useState(
    String(item.number_of_servings),
  );
  const [servingSize, setServingSize] = useState(String(item.serving_size));

  // Track the last value we successfully sent (or the initial value),
  // so we know what to diff against and never re-send an unchanged value.
  const lastSentServings = useRef(item.number_of_servings);
  const lastSentSize = useRef(item.serving_size);

  const isFirstServingsRender = useRef(true);
  const isFirstSizeRender = useRef(true);

  useEffect(() => {
    if (isFirstServingsRender.current) {
      isFirstServingsRender.current = false;
      return;
    }

    const parsed = parseFloat(numberOfServings);

    if (Number.isNaN(parsed) || parsed <= 0) {
      return;
    }

    if (parsed === lastSentServings.current) {
      return;
    }

    const timeout = setTimeout(() => {
      lastSentServings.current = parsed;

      updateMealFood.mutate(
        { id: item.id, data: { number_of_servings: parsed } },
        {
          onError: () => {
            // Revert on failure so the UI doesn't lie about what was saved.
            lastSentServings.current = item.number_of_servings;
            setNumberOfServings(String(item.number_of_servings));
          },
        },
      );
    }, DEBOUNCE_MS);

    return () => clearTimeout(timeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [numberOfServings]);

  useEffect(() => {
    if (isFirstSizeRender.current) {
      isFirstSizeRender.current = false;
      return;
    }

    const parsed = parseFloat(servingSize);

    if (Number.isNaN(parsed) || parsed <= 0) {
      return;
    }

    if (parsed === lastSentSize.current) {
      return;
    }

    const timeout = setTimeout(() => {
      lastSentSize.current = parsed;

      updateMealFood.mutate(
        { id: item.id, data: { serving_size: parsed } },
        {
          onError: () => {
            lastSentSize.current = item.serving_size;
            setServingSize(String(item.serving_size));
          },
        },
      );
    }, DEBOUNCE_MS);

    return () => clearTimeout(timeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [servingSize]);

  return (
    <li className="list-group-item d-flex justify-content-between align-items-center px-0">
      <span>{item.food.name}</span>

      <span className="d-flex align-items-center gap-1 text-muted">
        <input
          type="number"
          min={0}
          step="any"
          className="form-control form-control-sm text-end"
          style={{ width: "4.5rem" }}
          value={numberOfServings}
          onChange={(e) => setNumberOfServings(e.target.value)}
          aria-label="Number of servings"
        />

        <span>×</span>

        <input
          type="number"
          min={0}
          step="any"
          className="form-control form-control-sm text-end"
          style={{ width: "5.5rem" }}
          value={servingSize}
          onChange={(e) => setServingSize(e.target.value)}
          aria-label="Serving size"
        />

        <button
          type="button"
          className="btn btn-sm btn-outline-danger border-0"
          onClick={() => deleteMealFood.mutate(item.id)}
          disabled={deleteMealFood.isPending}
          aria-label={`Remove ${item.food.name}`}
          title="Remove"
        >
          <i className="bi bi-trash" aria-hidden="true"></i>
        </button>
      </span>
    </li>
  );
}