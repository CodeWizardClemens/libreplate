import { useState } from "react";
import type { Food } from "../types";
import { useFoods } from "../api";

interface FoodPickerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (food: Food) => void;
}

export default function FoodPickerModal({
  isOpen,
  onClose,
  onSelect,
}: FoodPickerModalProps) {
  const [search, setSearch] = useState("");

  const {
    data: foods,
    isLoading,
    isError,
  } = useFoods();

  if (!isOpen) {
    return null;
  }

  const filteredFoods =
    foods?.filter((food) =>
      food.name
        .toLowerCase()
        .includes(search.toLowerCase()),
    ) ?? [];


  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.4)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "20px",
          width: "400px",
          borderRadius: "8px",
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


        {isLoading && <p>Loading foods...</p>}

        {isError && (
          <p>Failed to load foods.</p>
        )}


        <div>
          {filteredFoods.map((food) => (
            <button
              key={food.id}
              onClick={() => {
                onSelect(food);
                onClose();
              }}
              style={{
                display: "block",
                width: "100%",
                textAlign: "left",
                marginBottom: "5px",
              }}
            >
              {food.name}
            </button>
          ))}
        </div>


        <button onClick={onClose}>
          Cancel
        </button>
      </div>
    </div>
  );
}