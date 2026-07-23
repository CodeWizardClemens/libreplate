import axios from "axios";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import type {
  Recipe,
  RecipeCreate,
  RecipeUpdate,
  RecipeTag,
  RecipeIngredient,
  RecipeIngredientCreate,
  RecipeIngredientUpdate,
  RecipePicture,
  ToggleFavoriteResponse,
  TogglePinResponse,
} from "./types";

function getCsrfToken() {
  const cookie = document.cookie.split("; ").find((row) => row.startsWith("csrftoken="));

  return cookie?.split("=")[1];
}

const api = axios.create({
  baseURL: "/api/recipes/",

  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const csrfToken = getCsrfToken();

  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }

  return config;
});

export const recipeKeys = {
  all: ["recipes"] as const,

  detail: (id: number) => ["recipes", id] as const,

  tags: ["recipe-tags"] as const,
};

export const ingredientKeys = {
  all: (recipeId: number) => ["recipe-ingredients", recipeId] as const,
};

export const pictureKeys = {
  detail: (recipeId: number) => ["recipe-picture", recipeId] as const,
};

// ========================
// Recipes
// ========================

export function useRecipes() {
  return useQuery({
    queryKey: recipeKeys.all,

    queryFn: async () => {
      const { data } = await api.get<Recipe[]>("");

      return data;
    },
  });
}

export function useRecipe(id: number) {
  return useQuery({
    queryKey: recipeKeys.detail(id),

    queryFn: async () => {
      const { data } = await api.get<Recipe>(`${id}/`);

      return data;
    },
  });
}

export function useCreateRecipe() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (recipe: RecipeCreate) => {
      const { data } = await api.post<Recipe>("", recipe);

      return data;
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: recipeKeys.all,
      });
    },
  });
}

export function useUpdateRecipe() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: RecipeUpdate }) => {
      const { data: result } = await api.patch<Recipe>(`${id}/`, data);

      return result;
    },

    onSuccess(_, variables) {
      queryClient.invalidateQueries({
        queryKey: recipeKeys.all,
      });

      queryClient.invalidateQueries({
        queryKey: recipeKeys.detail(variables.id),
      });
    },
  });
}

export function useDeleteRecipe() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`${id}/`);
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: recipeKeys.all,
      });
    },
  });
}

// ========================
// Favorite / Pin
// ========================

export function useToggleFavorite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const { data } = await api.post<ToggleFavoriteResponse>(`${id}/toggle-favorite/`);

      return data;
    },

    onSuccess(_, id) {
      queryClient.invalidateQueries({
        queryKey: recipeKeys.all,
      });

      queryClient.invalidateQueries({
        queryKey: recipeKeys.detail(id),
      });
    },
  });
}

export function useTogglePin() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const { data } = await api.post<TogglePinResponse>(`${id}/toggle-pin/`);

      return data;
    },

    onSuccess(_, id) {
      queryClient.invalidateQueries({
        queryKey: recipeKeys.all,
      });

      queryClient.invalidateQueries({
        queryKey: recipeKeys.detail(id),
      });
    },
  });
}

// ========================
// Copy Recipe
// ========================

export function useCopyRecipe() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, name }: { id: number; name: string }) => {
      const { data } = await api.post<Recipe>(`${id}/copy/`, {
        name,
      });

      return data;
    },

    onSuccess(data) {
      queryClient.invalidateQueries({
        queryKey: recipeKeys.all,
      });

      queryClient.invalidateQueries({
        queryKey: recipeKeys.detail(data.id),
      });
    },
  });
}

// ========================
// Tags
// ========================

export function useRecipeTags() {
  return useQuery({
    queryKey: recipeKeys.tags,

    queryFn: async () => {
      const { data } = await api.get<RecipeTag[]>("tags/");

      return data;
    },
  });
}

export function useCreateRecipeTag() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (name: string) => {
      const { data } = await api.post<RecipeTag>("tags/", {
        name,
      });

      return data;
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: recipeKeys.tags,
      });
    },
  });
}

export function useDeleteRecipeTag() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`tags/${id}/delete/`);
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: recipeKeys.tags,
      });
    },
  });
}

// ========================
// Ingredients
// ========================

export function useRecipeIngredients(recipeId: number) {
  return useQuery({
    queryKey: ingredientKeys.all(recipeId),

    queryFn: async () => {
      const { data } = await api.get<RecipeIngredient[]>(`${recipeId}/ingredients/`);

      return data;
    },
  });
}

export function useRecipeIngredient(recipeId: number, ingredientId: number) {
  return useQuery({
    queryKey: [...ingredientKeys.all(recipeId), ingredientId],

    queryFn: async () => {
      const { data } = await api.get<RecipeIngredient>(`${recipeId}/ingredients/${ingredientId}/`);

      return data;
    },
  });
}

export function useCreateRecipeIngredient() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ recipeId, data }: { recipeId: number; data: RecipeIngredientCreate }) => {
      const { data: result } = await api.post<RecipeIngredient>(`${recipeId}/ingredients/`, data);

      return result;
    },

    onSuccess(_, variables) {
      queryClient.invalidateQueries({
        queryKey: ingredientKeys.all(variables.recipeId),
      });
    },
  });
}

export function useUpdateRecipeIngredient() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      recipeId,
      ingredientId,
      data,
    }: {
      recipeId: number;
      ingredientId: number;
      data: RecipeIngredientUpdate;
    }) => {
      const { data: result } = await api.patch<RecipeIngredient>(
        `${recipeId}/ingredients/${ingredientId}/`,
        data,
      );

      return result;
    },

    onSuccess(_, variables) {
      queryClient.invalidateQueries({
        queryKey: ingredientKeys.all(variables.recipeId),
      });
    },
  });
}

export function useDeleteRecipeIngredient() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ recipeId, ingredientId }: { recipeId: number; ingredientId: number }) => {
      await api.delete(`${recipeId}/ingredients/${ingredientId}/`);
    },

    onSuccess(_, variables) {
      queryClient.invalidateQueries({
        queryKey: ingredientKeys.all(variables.recipeId),
      });
    },
  });
}

// ========================
// Recipe Picture
// ========================

export function useRecipePicture(recipeId: number) {
  return useQuery({
    queryKey: pictureKeys.detail(recipeId),

    queryFn: async () => {
      const { data } = await api.get<RecipePicture>(`${recipeId}/picture/`);

      return data;
    },
  });
}

export function useUploadRecipePicture() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ recipeId, file }: { recipeId: number; file: File }) => {
      const formData = new FormData();

      formData.append("image", file);

      const { data } = await api.post<RecipePicture>(`${recipeId}/picture/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      return data;
    },

    onSuccess(_, variables) {
      queryClient.invalidateQueries({
        queryKey: pictureKeys.detail(variables.recipeId),
      });
    },
  });
}

export function useDeleteRecipePicture() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (recipeId: number) => {
      await api.delete(`${recipeId}/picture/`);
    },

    onSuccess(_, recipeId) {
      queryClient.invalidateQueries({
        queryKey: pictureKeys.detail(recipeId),
      });
    },
  });
}
