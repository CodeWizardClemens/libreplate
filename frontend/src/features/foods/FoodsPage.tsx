import { useState } from "react";

import FoodList from "@/features/foods/components/FoodList";
import FoodSearchBar, {
  type FoodSortMethod,
} from "@/features/foods/components/FoodSearchBar";

import {
  useCreateFood,
  useDeleteFood,
  useFoods,
  useUpdateFood,
} from "@/api/FoodAPI";

export default function FoodsPage() {
  const foodsQuery = useFoods();

  const deleteFood = useDeleteFood();
  const updateFood = useUpdateFood();
  const createFood = useCreateFood();

  const [search, setSearch] = useState("");
  const [showFavorites, setShowFavorites] = useState(false);
  const [sortMethod, setSortMethod] = useState<FoodSortMethod>("name");

  if (foodsQuery.isPending) {
    return <div className="container py-3">Loading...</div>;
  }

  if (foodsQuery.isError) {
    return <div className="container py-3">Failed to load foods.</div>;
  }

  const foods = foodsQuery.data;

  function handleAddFood() {
    createFood.mutate({
      name: "New food",
      unitID: "g",
      serving: null,
      barcode: null,
      brand: null,
      description: "",
      is_favorite: false,
      usda_fdc_id: null,
      nutrients: [],
    });
  }

  function handleToggleFavorite(id: number) {
    const food = foods.find((f) => f.id === id);

    if (!food) {
      return;
    }

    updateFood.mutate({
      id,
      data: { is_favorite: !food.is_favorite },
    });
  }

  const filteredFoods = foods
    .filter((food) => {
      const searchTerm = search.toLowerCase();

      const matchesSearch =
        food.name.toLowerCase().includes(searchTerm) ||
        (food.brand?.toLowerCase().includes(searchTerm) ?? false) ||
        (food.description?.toLowerCase().includes(searchTerm) ?? false);

      const matchesFavorite = !showFavorites || food.is_favorite;

      return matchesSearch && matchesFavorite;
    })
    .sort((a, b) => {
      switch (sortMethod) {
        case "name":
          return a.name.localeCompare(b.name);

        case "brand":
          return (a.brand ?? "").localeCompare(b.brand ?? "");

        default:
          return 0;
      }
    });

  return (
    <div className="container">

      <div className="text-start mb-2">
        <button
          type="button"
          className="btn btn-outline-primary"
          onClick={handleAddFood}
          disabled={createFood.isPending}
        >
          New food
        </button>
      </div>

      <div className="mb-3">
        <FoodSearchBar
          search={search}
          onSearchChange={setSearch}
          foodCount={filteredFoods.length}
          showFavorites={showFavorites}
          onToggleFavorites={() => setShowFavorites(!showFavorites)}
          sortMethod={sortMethod}
          onSortChange={setSortMethod}
        />
      </div>

      <div className="mt-2">
        <FoodList
          foods={filteredFoods}
          onDelete={(id) => deleteFood.mutate(id)}
          onToggleFavorite={handleToggleFavorite}
        />
      </div>
    </div>
  );
}