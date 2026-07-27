import type { Food } from "@/api/generated";

interface Props {
  nutrients: Food["nutrients"];
}

export default function FoodCardNutrients({ nutrients }: Props) {
  const allowedNutrients = nutrients?.filter((nutrient) =>
    ["energy", "protein", "carbohydrates", "fat", "fats"].includes(
      nutrient.nutrient_name.toLowerCase(),
    ),
  );

  return (
    <div
      className="
        row
        g-2
        mb-3
      "
    >
      {allowedNutrients?.map((nutrient, index) => (
        <div
          key={nutrient.nutrient_id ?? index}
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
            {nutrient.nutrient_name.toLowerCase() === "carbohydrates"
              ? "Carbs"
              : nutrient.nutrient_name}
            {": "}
            {nutrient.amount}
            {nutrient.nutrient_unit}
          </span>
        </div>
      ))}
    </div>
  );
}
