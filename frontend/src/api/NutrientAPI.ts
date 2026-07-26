import axios from "axios";

import { useQuery } from "@tanstack/react-query";

import type { Nutrient } from "@/types/NutrientTypes";

const api = axios.create({
  baseURL: "/api/nutrients/",
  withCredentials: true,
});

export const nutrientKeys = {
  all: ["nutrients"] as const,
};

// ========================
// Nutrients
// ========================

export function useNutrients() {
  return useQuery({
    queryKey: nutrientKeys.all,

    queryFn: async () => {
      const { data } = await api.get<Nutrient[]>("");

      return data;
    },
  });
}
