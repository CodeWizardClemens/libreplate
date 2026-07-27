//  TODO this file should be deleted, generated API has to be used instead.
// 
import axios from "axios";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import type {
  Meal,
  MealCreate,
  MealUpdate,
  MealFood,
  MealFoodCreate,
  MealFoodUpdate,
  DefaultMeal,
  DefaultMealCreate,
  DefaultMealUpdate,
  DayMeal,
} from "@/types/MealTypes";

function getCsrfToken() {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));
  return cookie?.split("=")[1];
}

const api = axios.create({
  baseURL: "/api/meals/",
  withCredentials: true,
});

const mealFoodApi = axios.create({
  baseURL: "/api/meals/meal-foods/",
  withCredentials: true,
});

function addCsrfInterceptor(instance: typeof api) {
  instance.interceptors.request.use((config) => {
    const csrfToken = getCsrfToken();
    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }
    return config;
  });
}

addCsrfInterceptor(api);
addCsrfInterceptor(mealFoodApi);

export const mealKeys = {
  all: ["meals"] as const,
  detail: (id: number) => ["meals", id] as const,
  day: (day: string) => ["meals", "day", day] as const,
};

export const mealFoodKeys = {
  all: ["meal-foods"] as const,
};

/* ===========================
 * Meals
 * =========================== */

export function useMeals() {
  return useQuery({
    queryKey: mealKeys.all,
    queryFn: async () => {
      const { data } = await api.get<Meal[]>("");
      return data;
    },
  });
}

export function useMeal(id: number) {
  return useQuery({
    queryKey: mealKeys.detail(id),
    queryFn: async () => {
      const { data } = await api.get<Meal>(`${id}/`);
      return data;
    },
  });
}

export function useCreateMeal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (meal: MealCreate) => {
      const { data } = await api.post<Meal>("", meal);
      return data;
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: mealKeys.all });
    },
  });
}

export function useUpdateMeal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: MealUpdate }) => {
      const { data: result } = await api.patch<Meal>(`${id}/`, data);
      return result;
    },
    onSuccess(_, variables) {
      queryClient.invalidateQueries({ queryKey: mealKeys.all });
      queryClient.invalidateQueries({
        queryKey: mealKeys.detail(variables.id),
      });
    },
  });
}

export function useDeleteMeal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`${id}/`);
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: mealKeys.all });
    },
  });
}

/* ===========================
 * Meal Foods
 * =========================== */

export function useCreateMealFood() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (mealFood: MealFoodCreate) => {
      const { data } = await mealFoodApi.post<MealFood>("", mealFood);
      return data;
    },
    onSuccess(data) {
      queryClient.invalidateQueries({ queryKey: mealFoodKeys.all });
      queryClient.invalidateQueries({ queryKey: mealKeys.detail(data.id) });
      queryClient.invalidateQueries({ queryKey: mealKeys.all });
    },
  });
}

export function useUpdateMealFood() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: MealFoodUpdate }) => {
      const { data: result } = await mealFoodApi.patch<MealFood>(
        `${id}/`,
        data,
      );
      return result;
    },
    onSuccess(data) {
      queryClient.invalidateQueries({ queryKey: mealFoodKeys.all });
      queryClient.invalidateQueries({ queryKey: mealKeys.detail(data.id) });
      queryClient.invalidateQueries({ queryKey: mealKeys.all });
      // Diary page reads from the day-scoped query, so invalidate that too
      queryClient.invalidateQueries({ queryKey: ["meals", "day"] });
    },
  });
}

export function useDeleteMealFood() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await mealFoodApi.delete(`${id}/`);
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: mealFoodKeys.all });
      queryClient.invalidateQueries({ queryKey: mealKeys.all });
      // Diary page reads from the day-scoped query, so invalidate that too
      queryClient.invalidateQueries({ queryKey: ["meals", "day"] });
    },
  });
}

/* ===========================
 * Default Meals
 * =========================== */

export function useDefaultMeals() {
  return useQuery({
    queryKey: ["default-meals"],
    queryFn: async () => {
      const { data } = await api.get<DefaultMeal[]>("defaults/");
      return data;
    },
  });
}

export function useCreateDefaultMeal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (meal: DefaultMealCreate) => {
      const { data } = await api.post<DefaultMeal>("defaults/", meal);
      return data;
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: ["default-meals"] });
    },
  });
}

export function useUpdateDefaultMeal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      id,
      data,
    }: {
      id: number;
      data: DefaultMealUpdate;
    }) => {
      const { data: result } = await api.patch<DefaultMeal>(
        `defaults/${id}/`,
        data,
      );
      return result;
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: ["default-meals"] });
    },
  });
}

export function useDeleteDefaultMeal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`defaults/${id}/`);
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: ["default-meals"] });
    },
  });
}

/* ===========================
 * Day Meals
 * =========================== */

export function useDayMeals(day: string) {
  return useQuery({
    queryKey: mealKeys.day(day),
    queryFn: async () => {
      const { data } = await api.get<DayMeal[]>(`day/${day}/`);
      return data;
    },
  });
}
