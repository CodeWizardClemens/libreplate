import { useState } from "react";
import FoodPickerModal from "./components/FoodPickerModal";
import type { Food } from "./types";


export default function FoodsPage() {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedFood, setSelectedFood] =
    useState<Food | null>(null);


  return (
    <div>
      <h1>
        To display a food press the + button
      </h1>
      <button
        onClick={() => setModalOpen(true)}
      >
        +
      </button>

      {selectedFood && (
        <h2>
          Selected food: {selectedFood.name}
        </h2>
      )}

      <FoodPickerModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onSelect={(food) => {
          setSelectedFood(food);
        }}
      />
    </div>
  );
}