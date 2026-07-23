import type { Recipe } from "../../types";

interface Props {
  nutrients: Recipe["nutrients"];
}

export default function RecipeCardNutrients({ nutrients }: Props) {
  if (nutrients.length === 0) {
    return null;
  }

  return (
    <div
      className="
                row
                g-2
                mb-3
            "
    >
      {nutrients.map((nutrient) => (
        <div
          key={nutrient.id}
          className="
                                col-6
                                col-md-auto
                            "
        >
          <span
            className="
                                    badge
                                    text-bg-light
                                    border
                                "
          >
            {nutrient.name}

            {": "}

            {nutrient.amount}
          </span>
        </div>
      ))}
    </div>
  );
}
