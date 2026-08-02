import { useState } from "react";
import { useNavigate } from "react-router-dom";

import FoodList from "@/features/foods/components/FoodList";
import FoodSearchBar, {
  type FoodSortMethod,
} from "@/features/foods/components/FoodSearchBar";

import {
  foodsCreate,
  foodsDestroy,
  foodsList,
  foodsPartialUpdate,
} from "@/api/generated/sdk.gen";

import type { FoodWritable } from "@/api/generated/types.gen";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export default function FoodsPage() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const foodsQuery = useQuery({
    queryKey: ["foods"],
    queryFn: async () => {
      const response = await foodsList();

      return response.data;
    },
  });

  const createFood = useMutation({
    mutationFn: (data: FoodWritable) =>
      foodsCreate({
        body: data,
      }),
    onSuccess: (response) => {
      queryClient.invalidateQueries({
        queryKey: ["foods"],
      });

      const food = response.data;

      if (food?.id) {
        navigate(`/foods/${food.id}/edit`);
      }
    },
  });

  const deleteFood = useMutation({
    mutationFn: (id: number) =>
      foodsDestroy({
        path: {
          id,
        },
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["foods"],
      });
    },
  });

  const updateFood = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<FoodWritable> }) =>
      foodsPartialUpdate({
        path: {
          id,
        },
        body: data,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["foods"],
      });
    },
  });

  const [search, setSearch] = useState("");
  const [showFavorites, setShowFavorites] = useState(false);
  const [sortMethod, setSortMethod] = useState<FoodSortMethod>("name");

  if (foodsQuery.isPending) {
    return <div className="container py-3">Loading...</div>;
  }

  if (foodsQuery.isError) {
    return <div className="container py-3">Failed to load foods.</div>;
  }

  const foods = foodsQuery.data ?? [];

  function handleAddFood() {
    createFood.mutate({
      name: "New food",
      unit_id: 1,
      serving: 100,
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
      data: {
        is_favorite: !food.is_favorite,
      },
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