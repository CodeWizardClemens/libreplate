import { useEffect, useState } from "react";

import type { Food } from "@/api/generated";
import { foodsList } from "@/api/generated";
import Modal from "@/components/ui/Modal";

interface FoodPickerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (foods: Food[]) => void;
}

/**
 * Foods store nutrients as a flat list (name/unit/amount) rather than
 * fixed columns, so we look up calories by unit ("kcal") first, falling
 * back to a name match ("energy"/"calorie") for data that's tagged
 * differently. Returns null if no matching nutrient is found.
 */
function getCalories(food: Food): number | null {
  const nutrients = food.nutrients ?? [];

  const byUnit = nutrients.find(
    (n) => n.nutrient_unit?.toLowerCase() === "kcal",
  );

  if (byUnit) {
    return byUnit.amount;
  }

  const byName = nutrients.find(
    (n) => n.nutrient_name && /energy|calorie/i.test(n.nutrient_name),
  );

  return byName ? byName.amount : null;
}

export default function FoodPickerModal({
  isOpen,
  onClose,
  onSelect,
}: FoodPickerModalProps) {
  const [search, setSearch] = useState("");
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());

  const [foods, setFoods] = useState<Food[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    async function loadFoods() {
      setIsLoading(true);
      setIsError(false);

      try {
        const response = await foodsList();
        setFoods(response.data ?? []);
      } catch {
        setIsError(true);
      } finally {
        setIsLoading(false);
      }
    }

    loadFoods();
  }, [isOpen]);

  const filteredFoods = foods.filter((food) =>
    food.name.toLowerCase().includes(search.toLowerCase()),
  );

  function toggleFood(id: number) {
    setSelectedIds((prev) => {
      const next = new Set(prev);

      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }

      return next;
    });
  }

  function reset() {
    setSearch("");
    setSelectedIds(new Set());
  }

  function handleClose() {
    reset();
    onClose();
  }

  function handleConfirm() {
    const selectedFoods = foods.filter((food) => selectedIds.has(food.id));

    if (selectedFoods.length === 0) {
      return;
    }

    onSelect(selectedFoods);
    reset();
  }

  return (
    <Modal
      isOpen={isOpen}
      title="Select foods"
      onClose={handleClose}
      footer={
        <div className="d-flex justify-content-between align-items-center">
          <button className="btn btn-secondary" onClick={handleClose}>
            Cancel
          </button>

          <button
            className="btn btn-primary"
            onClick={handleConfirm}
            disabled={selectedIds.size === 0}
          >
            Add {selectedIds.size > 0 ? selectedIds.size : ""} food
            {selectedIds.size === 1 ? "" : "s"}
          </button>
        </div>
      }
    >
      <div className="mb-3">
        <input
          className="form-control"
          placeholder="Search food..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {isLoading && <p>Loading foods...</p>}

      {isError && <p className="text-danger">Failed to load foods.</p>}

      <div className="overflow-auto">
        {filteredFoods.map((food) => {
          const calories = getCalories(food);
          const isChecked = selectedIds.has(food.id);

          return (
            <label
              key={food.id}
              className="d-flex justify-content-between align-items-center rounded px-2 py-1 mb-1"
              style={{
                cursor: "pointer",
                background: isChecked ? "#f0f6ff" : "transparent",
              }}
            >
              <span className="d-flex align-items-center gap-2">
                <input
                  type="checkbox"
                  checked={isChecked}
                  onChange={() => toggleFood(food.id)}
                />

                <span>{food.name}</span>
              </span>

              <span className="text-muted small">
                {calories !== null ? `${Math.round(calories)} kcal` : "—"}
              </span>
            </label>
          );
        })}

        {!isLoading && filteredFoods.length === 0 && (
          <p className="text-muted">No foods found.</p>
        )}
      </div>
    </Modal>
  );
}
