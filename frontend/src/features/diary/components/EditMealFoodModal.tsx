import { useState } from "react";
import { useUpdateMealFood } from "@/api/MealAPI";
import type { MealFood } from "@/types/MealTypes";

type Props = {
  item: MealFood;
  onClose: () => void;
};

export default function EditMealFoodModal({ item, onClose }: Props) {
  const updateMealFood = useUpdateMealFood();

  const [servingSize, setServingSize] = useState(String(item.serving_size));
  const [servings, setServings] = useState(String(item.number_of_servings));

  async function handleSave() {
    const parsedSize = parseFloat(servingSize);
    const parsedServings = parseFloat(servings);

    if (parsedSize <= 0 || parsedServings <= 0) return;

    await updateMealFood.mutateAsync({
      id: item.id,
      data: {
        serving_size: parsedSize,
        number_of_servings: parsedServings,
      },
    });

    onClose();
  }

  return (
    <div
      onClick={onClose}
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
          width: "360px",
          borderRadius: "8px",
          display: "flex",
          flexDirection: "column",
          gap: "16px",
          maxHeight: "80vh",
        }}
      >
        <h2>Edit {item.food.name}</h2>

        <div>
          <label className="form-label">Serving size (g)</label>
          <input
            type="number"
            min={0}
            step="any"
            value={servingSize}
            onChange={(e) => setServingSize(e.target.value)}
            style={{ width: "100%" }}
          />
        </div>

        <div>
          <label className="form-label">Number of servings</label>
          <input
            type="number"
            min={0}
            step="any"
            value={servings}
            onChange={(e) => setServings(e.target.value)}
            style={{ width: "100%" }}
          />
        </div>

        <div
          style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}
        >
          <button className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button className="btn btn-primary" onClick={handleSave}>
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
