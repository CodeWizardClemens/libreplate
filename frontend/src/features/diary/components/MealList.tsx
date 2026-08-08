import type { DayMeal } from "@/api/generated";

import MealCard from "@/features/diary/components/MealCard";

type Props = {
  meals: DayMeal[];
  onAdd: (meal: DayMeal) => void;
  onDiaryChanged: () => Promise<void>;
};

export default function MealList({ meals, onAdd, onDiaryChanged }: Props) {
  return (
    <div className="row g-2">
      {meals.map((meal) => (
        <MealCard
          key={meal.default_meal.id}
          meal={meal}
          onAdd={onAdd}
          onDiaryChanged={onDiaryChanged}
        />
      ))}
    </div>
  );
}
