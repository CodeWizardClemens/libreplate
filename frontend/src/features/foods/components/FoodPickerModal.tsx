import { useState } from "react";
import type { Food } from "@/api/generated";
import { useFoods } from "@/api/FoodAPI";

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

  const { data: foods, isLoading, isError } = useFoods();

  if (!isOpen) {
    return null;
  }

  const filteredFoods =
    foods?.filter((food) =>
      food.name.toLowerCase().includes(search.toLowerCase()),
    ) ?? [];

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
    const selectedFoods = (foods ?? []).filter((food) =>
      selectedIds.has(food.id),
    );

    if (selectedFoods.length === 0) {
      return;
    }

    onSelect(selectedFoods);
    reset();
  }

  return (
    <div
      onClick={handleClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.4)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1050,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "white",
          padding: "20px",
          width: "420px",
          maxHeight: "80vh",
          borderRadius: "8px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <h2>Select food</h2>

        <input
          placeholder="Search food..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            width: "100%",
            marginBottom: "15px",
          }}
        />

        {/* {isLoading && <p>Loading foods...</p>} */}

        {isError && <p>Failed to load foods.</p>}

        <div style={{ overflowY: "auto", flex: 1 }}>
          {filteredFoods.map((food) => {
            const calories = getCalories(food);
            const isChecked = selectedIds.has(food.id);

            return (
              <label
                key={food.id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  width: "100%",
                  padding: "6px 4px",
                  marginBottom: "4px",
                  borderRadius: "4px",
                  cursor: "pointer",
                  background: isChecked ? "#f0f6ff" : "transparent",
                }}
              >
                <span
                  style={{ display: "flex", alignItems: "center", gap: "8px" }}
                >
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() => toggleFood(food.id)}
                  />
                  <span>{food.name}</span>
                </span>

                <span style={{ color: "#666", fontSize: "0.9em" }}>
                  {calories !== null ? `${Math.round(calories)} kcal` : "—"}
                </span>
              </label>
            );
          })}

          {!isLoading && filteredFoods.length === 0 && (
            <p style={{ color: "#666" }}>No foods found.</p>
          )}
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginTop: "15px",
          }}
        >
          <button onClick={handleClose}>Cancel</button>

          <button
            onClick={handleConfirm}
            disabled={selectedIds.size === 0}
            style={{ fontWeight: "bold" }}
          >
            Add {selectedIds.size > 0 ? selectedIds.size : ""} food
            {selectedIds.size === 1 ? "" : "s"}
          </button>
        </div>
      </div>
    </div>
  );
}
