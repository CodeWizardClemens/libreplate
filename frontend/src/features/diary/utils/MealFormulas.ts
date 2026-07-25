export function computeMealTotals(mealFoods) {
  const totals = {
    energy: 0,
    protein: 0,
    fat: 0,
    carbs: 0,
  };

  for (const mf of mealFoods) {
    const multiplier = mf.serving_size * mf.number_of_servings / 100;

    for (const n of mf.food.nutrients) {
      const amount = n.amount * multiplier;

      switch (n.nutrient_name.toLowerCase()) {
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
