import axios from "axios";

import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import type {
    Recipe,
    RecipeCreate,
    RecipeUpdate,
    RecipeTag,
    ToggleFavoriteResponse,
    TogglePinResponse,
} from "./types";


function getCsrfToken() {
    const cookie = document.cookie
        .split("; ")
        .find((row) =>
            row.startsWith("csrftoken=")
        );

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

    detail: (id: number) =>
        ["recipes", id] as const,

    tags: ["recipe-tags"] as const,
};


// --------------------
// Recipes
// --------------------

export function useRecipes() {
    return useQuery({
        queryKey: recipeKeys.all,

        queryFn: async () => {
            const { data } =
                await api.get<Recipe[]>("");

            return data;
        },
    });
}


export function useRecipe(id: number) {
    return useQuery({
        queryKey: recipeKeys.detail(id),

        queryFn: async () => {
            const { data } =
                await api.get<Recipe>(
                    `${id}/`
                );

            return data;
        },
    });
}


export function useCreateRecipe() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (
            recipe: RecipeCreate
        ) => {
            const { data } =
                await api.post<Recipe>(
                    "",
                    recipe
                );

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
        mutationFn: async ({
            id,
            data,
        }: {
            id: number;
            data: RecipeUpdate;
        }) => {
            const response =
                await api.patch<Recipe>(
                    `${id}/`,
                    data
                );

            return response.data;
        },

        onSuccess(_, variables) {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });

            queryClient.invalidateQueries({
                queryKey: recipeKeys.detail(
                    variables.id
                ),
            });
        },
    });
}


export function useDeleteRecipe() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (
            id: number
        ) => {
            await api.delete(
                `${id}/`
            );
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}


// --------------------
// Favorite / Pin
// --------------------

export function useToggleFavorite() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (
            id: number
        ) => {
            const { data } =
                await api.post<ToggleFavoriteResponse>(
                    `${id}/toggle-favorite/`
                );

            return data;
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}


export function useTogglePin() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (
            id: number
        ) => {
            const { data } =
                await api.post<TogglePinResponse>(
                    `${id}/toggle-pin/`
                );

            return data;
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}


// --------------------
// Copy Recipe
// --------------------

export function useCopyRecipe() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({
            id,
            name,
        }: {
            id: number;
            name: string;
        }) => {
            const { data } =
                await api.post<Recipe>(
                    `${id}/copy/`,
                    {
                        name,
                    }
                );

            return data;
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.all,
            });
        },
    });
}


// --------------------
// Tags
// --------------------

export function useRecipeTags() {
    return useQuery({
        queryKey: recipeKeys.tags,

        queryFn: async () => {
            const { data } =
                await api.get<RecipeTag[]>(
                    "tags/"
                );

            return data;
        },
    });
}


export function useCreateRecipeTag() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (
            name: string
        ) => {
            const { data } =
                await api.post<RecipeTag>(
                    "tags/",
                    {
                        name,
                    }
                );

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
        mutationFn: async (
            id: number
        ) => {
            await api.delete(
                `tags/${id}/delete/`
            );
        },

        onSuccess() {
            queryClient.invalidateQueries({
                queryKey: recipeKeys.tags,
            });
        },
    });
}