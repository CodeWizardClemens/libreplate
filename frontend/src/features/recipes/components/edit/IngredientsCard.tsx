import { useEffect, useMemo, useState } from "react";

import type { Recipe, RecipeIngredient } from "../../types";
import type { Food } from "../../../foods/types";

import {
  useCreateRecipeIngredient,
  useDeleteRecipeIngredient,
  useUpdateRecipeIngredient,
} from "../../api";

import { useFood } from "../../../foods/api";
import FoodPickerModal from "../../../foods/components/FoodPickerModal";


interface IngredientsCardProps {
  recipe: Recipe;
}


const nutrientNames = {
  energy: ["energy", "calories"],
  protein: ["protein"],
  fat: ["fat", "total lipid"],
  carbohydrates: ["carbohydrate", "carbs"],
};


const headers = [
  "Food",
  "Servings",
  "Amount",
  "Energy",
  "Protein",
  "Fat",
  "Carbs",
  "",
];


function getNutrient(food: Food, names: string[]) {
  return (
    food.nutrients.find((n) =>
      names.some((name) =>
        n.nutrient_name.toLowerCase().includes(name),
      ),
    )?.amount ?? 0
  );
}


function getIngredientMultiplier(
  food: Food,
  ingredient: RecipeIngredient,
) {
  return (
    ingredient.number_of_servings *
    (ingredient.serving_amount / (food.serving ?? 1))
  );
}


function NumberInput({
  value,
  onChange,
}: {
  value: number;
  onChange: (value: number) => void;
}) {
  return (
    <input
      className="form-control form-control-sm text-center"
      style={{ width: 90 }}
      type="number"
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
    />
  );
}


function NutrientCell({ value }: { value: number }) {
  return (
    <td className="text-start text-muted">
      {Math.round(value)}
    </td>
  );
}


function IngredientRow({
  recipeId,
  ingredient,
  onDelete,
  onUpdate,
}: {
  recipeId: number;
  ingredient: RecipeIngredient;
  onDelete: (id: number) => void;
  onUpdate: (
    id: number,
    data: Partial<RecipeIngredient>,
  ) => void;
}) {
  const { data: food } = useFood(ingredient.food);
  const updateMutation = useUpdateRecipeIngredient();


  if (!food) {
    return (
      <tr>
        <td colSpan={8} className="text-center py-3 text-muted">
          Loading...
        </td>
      </tr>
    );
  }


  const update = (data: Partial<RecipeIngredient>) => {
    onUpdate(ingredient.id, data);

    updateMutation.mutate({
      recipeId,
      ingredientId: ingredient.id,
      data,
    });
  };


  const nutrients = useMemo(() => {
    const multiplier = getIngredientMultiplier(
      food,
      ingredient,
    );

    return {
      energy:
        getNutrient(food, nutrientNames.energy) *
        multiplier,

      protein:
        getNutrient(food, nutrientNames.protein) *
        multiplier,

      fat:
        getNutrient(food, nutrientNames.fat) *
        multiplier,

      carbohydrates:
        getNutrient(food, nutrientNames.carbohydrates) *
        multiplier,
    };
  }, [
    food,
    ingredient.number_of_servings,
    ingredient.serving_amount,
  ]);


  return (
    <tr>
      <td className="fw-semibold">{food.name}</td>

      <td>
        <NumberInput
          value={ingredient.number_of_servings}
          onChange={(value) =>
            update({
              number_of_servings: value,
            })
          }
        />
      </td>

      <td>
        <NumberInput
          value={ingredient.serving_amount}
          onChange={(value) =>
            update({
              serving_amount: value,
            })
          }
        />
      </td>

      <NutrientCell value={nutrients.energy} />
      <NutrientCell value={nutrients.protein} />
      <NutrientCell value={nutrients.fat} />
      <NutrientCell value={nutrients.carbohydrates} />

      <td className="text-end">
        <button
          className="btn btn-sm btn-outline-danger"
          onClick={() => onDelete(ingredient.id)}
        >
          Delete
        </button>
      </td>
    </tr>
  );
}

function TotalsRow({
  totals,
}: {
  totals: {
    energy: number;
    protein: number;
    fat: number;
    carbohydrates: number;
  };
}) {
  return (
    <tfoot className="table-light fw-semibold">
      <tr>
        <td>Totals</td>
        <td colSpan={2}></td>
        <td>{Math.round(totals.energy)}</td>
        <td>{Math.round(totals.protein)}</td>
        <td>{Math.round(totals.fat)}</td>
        <td>{Math.round(totals.carbohydrates)}</td>
        <td></td>
      </tr>
    </tfoot>
  );
}


function IngredientTotals({
  ingredients,
}: {
  ingredients: RecipeIngredient[];
}) {
  const [totals, setTotals] = useState({
    energy: 0,
    protein: 0,
    fat: 0,
    carbohydrates: 0,
  });


  useEffect(() => {
    setTotals({
      energy: 0,
      protein: 0,
      fat: 0,
      carbohydrates: 0,
    });
  }, [ingredients]);


  const addTotals = (
    values: {
      energy: number;
      protein: number;
      fat: number;
      carbohydrates: number;
    },
  ) => {
    setTotals((current) => ({
      energy: current.energy + values.energy,
      protein: current.protein + values.protein,
      fat: current.fat + values.fat,
      carbohydrates:
        current.carbohydrates + values.carbohydrates,
    }));
  };


  return (
    <>
      {ingredients.map((ingredient) => (
        <IngredientTotalCalculator
          key={ingredient.id}
          ingredient={ingredient}
          onCalculated={addTotals}
        />
      ))}

      <TotalsRow totals={totals} />
    </>
  );
}


function IngredientTotalCalculator({
  ingredient,
  onCalculated,
}: {
  ingredient: RecipeIngredient;
  onCalculated: (values: {
    energy: number;
    protein: number;
    fat: number;
    carbohydrates: number;
  }) => void;
}) {
  const { data: food } = useFood(ingredient.food);


  useEffect(() => {
    if (!food) return;


    const multiplier = getIngredientMultiplier(
      food,
      ingredient,
    );


    onCalculated({
      energy:
        getNutrient(food, nutrientNames.energy) *
        multiplier,

      protein:
        getNutrient(food, nutrientNames.protein) *
        multiplier,

      fat:
        getNutrient(food, nutrientNames.fat) *
        multiplier,

      carbohydrates:
        getNutrient(food, nutrientNames.carbohydrates) *
        multiplier,
    });
  }, [
    food,
    ingredient.number_of_servings,
    ingredient.serving_amount,
  ]);


  return null;
}


export default function IngredientsCard({
  recipe,
}: IngredientsCardProps) {
  const [ingredients, setIngredients] = useState(
    recipe.ingredients,
  );

  const [pickerOpen, setPickerOpen] = useState(false);


  const createMutation = useCreateRecipeIngredient();
  const deleteMutation = useDeleteRecipeIngredient();


  useEffect(() => {
    setIngredients(recipe.ingredients);
  }, [recipe.ingredients]);


  const updateIngredient = (
    id: number,
    data: Partial<RecipeIngredient>,
  ) => {
    setIngredients((items) =>
      items.map((item) =>
        item.id === id
          ? {
              ...item,
              ...data,
            }
          : item,
      ),
    );
  };


  const addFood = (food: Food) => {
    createMutation.mutate(
      {
        recipeId: recipe.id,
        data: {
          food: food.id,
          number_of_servings: 1,
          serving_amount: food.serving ?? 1,
          order: ingredients.length,
        },
      },
      {
        onSuccess: (ingredient) =>
          setIngredients((items) => [
            ...items,
            ingredient,
          ]),
      },
    );

    setPickerOpen(false);
  };


  const removeIngredient = (id: number) => {
    setIngredients((items) =>
      items.filter((item) => item.id !== id),
    );

    deleteMutation.mutate({
      recipeId: recipe.id,
      ingredientId: id,
    });
  };


  return (
    <div className="card shadow-sm border-0">
      <div className="card-body">

        <div className="d-flex justify-content-between mb-4">
          <h4 className="card-title mb-0">
            Ingredients
          </h4>

          <button
            className="btn btn-primary"
            onClick={() => setPickerOpen(true)}
          >
            Add ingredient
          </button>
        </div>


        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead className="table-light">
              <tr>
                {headers.map((header) => (
                  <th key={header}>
                    {header}
                  </th>
                ))}
              </tr>
            </thead>


            <tbody>
              {ingredients.length ? (
                ingredients.map((ingredient) => (
                  <IngredientRow
                    key={ingredient.id}
                    recipeId={recipe.id}
                    ingredient={ingredient}
                    onDelete={removeIngredient}
                    onUpdate={updateIngredient}
                  />
                ))
              ) : (
                <tr>
                  <td
                    colSpan={8}
                    className="text-center py-5 text-muted"
                  >
                    No ingredients added yet
                  </td>
                </tr>
              )}
            </tbody>


            {ingredients.length > 0 && (
              <IngredientTotals ingredients={ingredients} />
            )}

          </table>
        </div>

      </div>


      <FoodPickerModal
        isOpen={pickerOpen}
        onClose={() => setPickerOpen(false)}
        onSelect={addFood}
      />

    </div>
  );
}