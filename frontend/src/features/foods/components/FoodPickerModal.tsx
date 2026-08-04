import { useEffect, useState } from "react";

import type { Food } from "@/api/generated";
import {
  foodsList,
  integrationsUsdaSearchRetrieve,
  integrationsUsdaSaveCreate,
} from "@/api/generated";
import Modal from "@/components/ui/Modal";

interface FoodPickerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (foods: Food[]) => void;
}

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

  const [localFoods, setLocalFoods] = useState<Food[]>([]);
  const [usdaFoods, setUsdaFoods] = useState<any[]>([]);

  const [selectedLocalIds, setSelectedLocalIds] = useState<Set<number>>(
    new Set(),
  );
  const [selectedUsdaIds, setSelectedUsdaIds] = useState<Set<string>>(
    new Set(),
  );

  const [isUsdaSearch, setIsUsdaSearch] = useState(false);

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
        setLocalFoods(response.data ?? []);
      } catch {
        setIsError(true);
      } finally {
        setIsLoading(false);
      }
    }

    loadFoods();
  }, [isOpen]);

  const filteredLocalFoods = localFoods.filter((food) =>
    food.name.toLowerCase().includes(search.toLowerCase()),
  );

  async function handleSearchKeyDown(
    event: React.KeyboardEvent<HTMLInputElement>,
  ) {
    if (event.key !== "Enter") {
      setIsUsdaSearch(false);
      return;
    }

    if (!search.trim()) {
      return;
    }

    setIsLoading(true);
    setIsError(false);
    setIsUsdaSearch(true);

    try {
      const response = await integrationsUsdaSearchRetrieve({
        query: {
          term: search.trim(),
        },
      });

      setUsdaFoods(
        (response.data?.foods ?? []).map((food: any) => ({
          ...food,
          selectionId: crypto.randomUUID(),
        })),
      );

      setSelectedLocalIds(new Set());
      setSelectedUsdaIds(new Set());
    } catch {
      setIsError(true);
      setUsdaFoods([]);
    } finally {
      setIsLoading(false);
    }
  }

  function toggleLocalFood(id: number) {
    setSelectedLocalIds((prev) => {
      const next = new Set(prev);

      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }

      return next;
    });
  }

  function toggleUsdaFood(id: string) {
    setSelectedUsdaIds((prev) => {
      const next = new Set(prev);

      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }

      return next;
    });
  }

  async function saveUsdaFood(usdaFood: any): Promise<Food | null> {
    try {
      const response = await integrationsUsdaSaveCreate({
        body: {
          fdc_id: usdaFood.usda_fdc_id,
        },
      });

      return response.data ? (response.data as Food) : null;
    } catch {
      return null;
    }
  }

  function reset() {
    setSearch("");
    setSelectedLocalIds(new Set());
    setSelectedUsdaIds(new Set());
    setUsdaFoods([]);
    setIsUsdaSearch(false);
  }

  function handleClose() {
    reset();
    onClose();
  }

  async function handleConfirm() {
    const selectedFoods: Food[] = [];

    if (isUsdaSearch) {
      for (const food of usdaFoods) {
        if (!selectedUsdaIds.has(food.selectionId)) {
          continue;
        }

        const savedFood = await saveUsdaFood(food);

        if (savedFood) {
          selectedFoods.push(savedFood);
        }
      }
    } else {
      selectedFoods.push(
        ...localFoods.filter((food) => selectedLocalIds.has(food.id)),
      );
    }

    if (selectedFoods.length === 0) {
      return;
    }

    onSelect(selectedFoods);
    reset();
  }

  const selectedCount = isUsdaSearch
    ? selectedUsdaIds.size
    : selectedLocalIds.size;

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
            disabled={selectedCount === 0}
          >
            Add {selectedCount > 0 ? selectedCount : ""} food
            {selectedCount === 1 ? "" : "s"}
          </button>
        </div>
      }
    >
      <div className="mb-3">
        <input
          className="form-control"
          placeholder="Search food..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setIsUsdaSearch(false);
          }}
          onKeyDown={handleSearchKeyDown}
        />
      </div>

      {isLoading && <p>Loading foods...</p>}

      {isError && <p className="text-danger">Failed to load foods.</p>}

      <div className="overflow-auto">
        {!isUsdaSearch &&
          filteredLocalFoods.map((food) => {
            const calories = getCalories(food);
            const isChecked = selectedLocalIds.has(food.id);

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
                    onChange={() => toggleLocalFood(food.id)}
                  />

                  <span>{food.name}</span>
                </span>

                <span className="text-muted small">
                  {calories !== null ? `${Math.round(calories)} kcal` : "—"}
                </span>
              </label>
            );
          })}

        {isUsdaSearch &&
          usdaFoods.map((food) => {
            const isChecked = selectedUsdaIds.has(food.selectionId);

            return (
              <label
                key={food.selectionId}
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
                    onChange={() => toggleUsdaFood(food.selectionId)}
                  />

                  <span>{food.description}</span>
                </span>

                <span className="text-muted small">USDA</span>
              </label>
            );
          })}

        {!isLoading && !isUsdaSearch && filteredLocalFoods.length === 0 && (
          <p className="text-muted">No foods found.</p>
        )}

        {!isLoading && isUsdaSearch && usdaFoods.length === 0 && (
          <p className="text-muted">No USDA foods found.</p>
        )}
      </div>
    </Modal>
  );
}
