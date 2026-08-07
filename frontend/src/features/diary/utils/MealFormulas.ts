import type { MealFood } from "@/api/generated";

export function computeMealTotals(mealFoods: MealFood[]) {
  const totals = {
    energy: 0,
    protein: 0,
    fat: 0,
    carbs: 0,
  };

  for (const mf of mealFoods) {
    const servingSize = mf.serving_size ?? 0;
    const numberOfServings = mf.number_of_servings ?? 0;

    const multiplier = (servingSize * numberOfServings) / 100;

    for (const nutrient of mf.food?.nutrients ?? []) {
      const amount = (nutrient.amount ?? 0) * multiplier;

      switch (nutrient.nutrient.name?.toLowerCase()) {
        case "energy":
        case "calories":
        case "kcal":
          totals.energy += amount;
          break;

        case "protein":
          totals.protein += amount;
          break;

        case "fat":
        case "total lipid (fat)":
          totals.fat += amount;
          break;

        case "carbohydrates":
        case "carbs":
        case "carbohydrate, by difference":
          totals.carbs += amount;
          break;
      }
    }
  }

  return totals;
}
