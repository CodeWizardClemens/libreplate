import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import type { FoodNutrient } from "@/types/FoodTypes";

import { useDeleteFood, useFood, useUpdateFood } from "@/api/FoodAPI";
import { useNutrients } from "@/api/NutrientAPI";

export default function FoodEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const foodId = Number(id);

  const foodQuery = useFood(foodId);
  const nutrientsQuery = useNutrients();
  const updateFood = useUpdateFood();
  const deleteFood = useDeleteFood();

  const [name, setName] = useState("");
  const [brand, setBrand] = useState("");
  const [description, setDescription] = useState("");
  const [serving, setServing] = useState<number | "">("");
  const [unitID, setUnit] = useState("");
  const [barcode, setBarcode] = useState("");
  const [isFavorite, setIsFavorite] = useState(false);
  const [nutrients, setNutrients] = useState<FoodNutrient[]>([]);

  useEffect(() => {
    if (!foodQuery.data) {
      return;
    }

    const food = foodQuery.data;

    setName(food.name);
    setBrand(food.brand ?? "");
    setDescription(food.description ?? "");
    setServing(food.serving ?? "");
    setUnit(food.unit);
    setBarcode(food.barcode ?? "");
    setIsFavorite(food.is_favorite);
  }, [foodQuery.data]);

  useEffect(() => {
    if (!foodQuery.data || !nutrientsQuery.data) {
      return;
    }

    const food = foodQuery.data;

    // Show every nutrient meant for the food-edit screen, plus any
    // nutrient already on this food even if it's since been hidden there.
    const relevantNutrients = nutrientsQuery.data.filter(
      (nutrient) =>
        nutrient.show_in_food_edit ||
        food.nutrients.some((n) => n.nutrient_id === nutrient.id),
    );

    const merged: FoodNutrient[] = relevantNutrients.map((nutrient) => {
      const existing = food.nutrients.find(
        (n) => n.nutrient_id === nutrient.id,
      );

      return {
        nutrient_id: nutrient.id,
        nutrient_name: nutrient.name,
        nutrient_unit: nutrient.unit ?? "",
        amount: existing?.amount ?? 0,
      };
    });

    setNutrients(merged);
  }, [foodQuery.data, nutrientsQuery.data]);

  if (foodQuery.isPending || nutrientsQuery.isPending) {
    return <div className="container py-3">Loading...</div>;
  }

  if (foodQuery.isError || nutrientsQuery.isError) {
    return <div className="container py-3">Failed to load food.</div>;
  }

  function updateNutrientAmount(index: number, amount: number) {
    setNutrients((prev) =>
      prev.map((n, i) => (i === index ? { ...n, amount } : n)),
    );
  }

  function handleSave() {
    updateFood.mutate(
      {
        id: foodId,
        data: {
          name,
          brand: brand || null,
          description: description || null,
          serving: serving === "" ? 0 : Number(serving),
          unitID,
          barcode: barcode || null,
          is_favorite: isFavorite,
          nutrients: nutrients.map((n) => ({
            nutrient_id: n.nutrient_id!,
            amount: n.amount,
          })),
        },
      },
      {
        onSuccess: () => navigate("/foods"),
      },
    );
  }

  function handleDelete() {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${name}"? This cannot be undone.`,
    );

    if (confirmed) {
      deleteFood.mutate(foodId, {
        onSuccess: () => navigate("/foods"),
      });
    }
  }

  return (
    <div className="container py-3">
      <div className="d-flex align-items-center justify-content-between mb-3">
        <button
          type="button"
          className="btn btn-outline-secondary"
          onClick={() => navigate("/foods")}
        >
          <i className="bi bi-arrow-left me-1" />
          Back
        </button>

        <button
          type="button"
          className="btn btn-outline-danger"
          onClick={handleDelete}
          disabled={deleteFood.isPending}
        >
          <i className="bi bi-trash me-1" />
          Delete
        </button>
      </div>

      <div className="card shadow-sm">
        <div className="card-body">
          <div className="row g-3">
            <div className="col-12 col-md-6">
              <label className="form-label">Name</label>
              <input
                className="form-control"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Brand</label>
              <input
                className="form-control"
                value={brand}
                onChange={(e) => setBrand(e.target.value)}
              />
            </div>

            <div className="col-12">
              <label className="form-label">Description</label>
              <textarea
                className="form-control"
                rows={3}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <div className="col-6 col-md-3">
              <label className="form-label">Serving</label>
              <input
                type="number"
                className="form-control"
                value={serving}
                onChange={(e) =>
                  setServing(
                    e.target.value === "" ? "" : Number(e.target.value),
                  )
                }
              />
            </div>

            <div className="col-6 col-md-3">
              <label className="form-label">Unit</label>
              <input
                className="form-control"
                value={unitID}
                onChange={(e) => setUnit(e.target.value)}
              />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Barcode</label>
              <input
                className="form-control"
                value={barcode}
                onChange={(e) => setBarcode(e.target.value)}
              />
            </div>

            <div className="col-12">
              <div className="form-check">
                <input
                  type="checkbox"
                  className="form-check-input"
                  id="isFavorite"
                  checked={isFavorite}
                  onChange={(e) => setIsFavorite(e.target.checked)}
                />
                <label className="form-check-label" htmlFor="isFavorite">
                  Favorite
                </label>
              </div>
            </div>
          </div>

          <hr className="my-4" />

          <h5 className="mb-3">Nutrients</h5>

          {nutrients.length === 0 && (
            <p className="text-muted">No nutrients configured.</p>
          )}

          {nutrients.map((nutrient, index) => (
            <div
              key={nutrient.nutrient_id ?? index}
              className="row g-2 align-items-center mb-2"
            >
              <div className="col-12 col-md-6">
                <span className="form-control-plaintext">
                  {nutrient.nutrient_name}
                </span>
              </div>

              <div className="col-8 col-md-4">
                <input
                  type="number"
                  className="form-control"
                  value={nutrient.amount}
                  onChange={(e) =>
                    updateNutrientAmount(index, Number(e.target.value))
                  }
                />
              </div>

              <div className="col-4 col-md-2">
                <span className="form-control-plaintext text-muted">
                  {nutrient.nutrient_unit}
                </span>
              </div>
            </div>
          ))}

          <div className="text-end mt-4">
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleSave}
              disabled={updateFood.isPending}
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
