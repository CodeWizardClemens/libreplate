import axios from "axios";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import type {
  Food,
  FoodCreate,
  FoodUpdate,
} from "./types";


function getCsrfToken() {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));

  return cookie?.split("=")[1];
}


const api = axios.create({
  baseURL: "/api/foods/",
  withCredentials: true,
});


api.interceptors.request.use((config) => {
  const csrfToken = getCsrfToken();

  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }

  return config;
});


export const foodKeys = {
  all: ["foods"] as const,

  detail: (id: number) => ["foods", id] as const,
};


// ========================
// Foods
// ========================

export function useFoods() {
  return useQuery({
    queryKey: foodKeys.all,

    queryFn: async () => {
      const { data } = await api.get<Food[]>("");

      return data;
    },
  });
}


export function useFood(id: number) {
  return useQuery({
    queryKey: foodKeys.detail(id),

    queryFn: async () => {
      const { data } = await api.get<Food>(`${id}/`);

      return data;
    },
  });
}


export function useCreateFood() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (food: FoodCreate) => {
      const { data } = await api.post<Food>("", food);

      return data;
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: foodKeys.all,
      });
    },
  });
}


export function useUpdateFood() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      id,
      data,
    }: {
      id: number;
      data: FoodUpdate;
    }) => {
      const { data: result } = await api.patch<Food>(
        `${id}/`,
        data,
      );

      return result;
    },

    onSuccess(_, variables) {
      queryClient.invalidateQueries({
        queryKey: foodKeys.all,
      });

      queryClient.invalidateQueries({
        queryKey: foodKeys.detail(variables.id),
      });
    },
  });
}


export function useDeleteFood() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`${id}/`);
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: foodKeys.all,
      });
    },
  });
}